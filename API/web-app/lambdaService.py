from flask import request, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
import boto3 ,os
from io import BytesIO
import zipfile
from datetime import datetime, timezone
from time import gmtime, strftime
import time
from tqdm import tqdm
from datetime import datetime, timedelta
import time
from collections import defaultdict

client = MongoClient('mongodb://localhost:27017/')
db = client['cloudPerformace']
userCollection = db['users']
applicationCollection=db['applications']


#Get lambda Client
def get_lambda_client(application,clientType):
    user = userCollection.find_one({'_id': ObjectId(application.get('userId'))})
    if user is None: raise ValueError("User is not attached with application")
    if user.get('cloudConfig') is None:raise ValueError("Please Setup Cloud Configurations first!")
    cloudConfigs=user.get('cloudConfig')
    isLambda=False
    lambdaConfig={}

    for config in cloudConfigs:
        if (config.get('cloudType') =='public') and (config.get('provider') =='lambda') :
            isLambda=True
            lambdaConfig=config
            break
    if(isLambda==False):raise ValueError("Please add Public Lambda configurations through settings !")

    if 'accessKey' not in lambdaConfig or 'secretKey' not in lambdaConfig or 'region' not in lambdaConfig:
        raise ValueError("Pease Update AWS details such as accessKey & secret key & region through settings !")
    
    session = boto3.Session(
        aws_access_key_id="AKIAVU74BCJYBZWGQPEL",
        aws_secret_access_key="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",
        region_name="ap-south-1"
    )
    if clientType=='lambda':return session.client('lambda')
    if clientType=='logs': return session.client('logs')


def deploy_application_in_public_cloud_lambda(application):
    lambda_client = get_lambda_client(application,'lambda')
    function_prefix="cloudPerformers_"+application.get('applicationName')
    lambda_functions_names=[]

    for function_file in os.listdir(application.get('applicationLocation')):
        if function_file.endswith('.py'):
            buf = BytesIO()
            with zipfile.ZipFile(buf, 'w') as z:
                z.write(os.path.abspath(os.path.join(application.get('applicationLocation'), function_file)), 'lambda_function.py')
            buf.seek(0)
            pkg = buf.read()
            FunctionName='{}_{}'.format(function_prefix, os.path.splitext(function_file)[0])                       
            lambda_functions_names.append(FunctionName)

            # Create an New function
            if 'Public_deployed' not in application.get('status'):
                print("Creating New Function - "+FunctionName)
                lambda_client.create_function(
                    FunctionName=FunctionName,
                    Runtime='python3.9',  
                    Role='arn:aws:iam::388686221936:role/lambdaRole',  
                    Handler='lambda_function.lambda_handler',  
                    Description='My Lambda function', 
                    Timeout=30, 
                    MemorySize=128 ,
                    Code={
                    'ZipFile': pkg
                    }
                )   
            #Update Function
            if 'Public_deployed' in application.get('status'):
                print("Updating Existing Function - "+FunctionName)
                lambda_client.update_function_code(FunctionName=FunctionName, ZipFile=pkg)

    #Change Status of the application          
    status = application.get('status', [])  # Get the current status list or initialize it as an empty list
    if 'Pending' in application.get('status'):status.remove('Pending')  # Remove the 'pending' status if present
    if 'Public_deployed' not in application.get('status'): status.append('Public_deployed')  # Append the new status 'Public_deployed'
    application['status'] = status
    application['lambdaFunctionNames']=lambda_functions_names
    
    #set feedbacks
    feedbacks=application.get('feedback')
    feedbacks.append('Deployed in public cloud')
    application['feedback']=feedbacks
    ##end of seting feedbacks
    applicationCollection.update_one({'_id': application.get('_id')}, {'$set': {'lambdaFunctionNames': lambda_functions_names}})
    applicationCollection.update_one({'_id': application.get('_id')}, {'$set': {'status': status}})

def invoke_public__lambda_functions_in_diffrent_mem(application,functions,mem_list,invocations):
    print('lambda Invocation starts')
    lambda_client=get_lambda_client(application,"lambda")
    for mem in mem_list:
        print('Memory: {} Timestamp: {} UTC: {}'.format(mem,time.time(),strftime("%d %b %Y %H:%M:%S +0000", gmtime())))
        for function in functions:
            print('Function: {} Timestamp: {} UTC: {}'.format(function,time.time(),strftime("%d %b %Y %H:%M:%S +0000", gmtime())))
            lambda_client.update_function_configuration(FunctionName=function, MemorySize=mem)
            time.sleep(1)
            for i in tqdm(range(invocations)):
                time.sleep(1)
                lambda_client.invoke(FunctionName=function, InvocationType='Event')
    
    print('lambda Invocation Ends')


def collect_lambda_logs(appliaction,functions):
    print('Lambda Log collection starts')
    logclient=get_lambda_client(appliaction,"logs")

    #setup empty rt times for each functions in the list
    for appliactionFunction in appliaction.get('functions'):
        if appliactionFunction.get('responseTimes') is None:
            appliactionFunction['responseTimes'] =[]

    for function in functions:
        log_group_name="/aws/lambda/"+function
                
        query_f1 = logclient.start_query(
            logGroupName=log_group_name,
            queryString="fields @timestamp, @message| sort @timestamp desc",
            startTime=int((datetime.today() - timedelta(hours=15)).timestamp()),
            endTime=int(datetime.now().timestamp()),
            limit=10000
        )
        query_results_f1 = logclient.get_query_results(queryId=query_f1['queryId'])

        response = None

        while response == None or response['status'] == 'Running':
            print("function - "+ function +'Waiting for query to complete ...')
            time.sleep(1)
            response = logclient.get_query_results(
                queryId=query_f1['queryId']
            )
        print("Total logs for"+function + "-" ,len(response['results']))
        messages = []

        for inner_list in response['results']:
            for dictionary in inner_list:
                if dictionary['field'] == '@message':
                    messages.append(dictionary['value'])

        #Messages Modified for format {mem:x,dutaion:y}
        result_list = []

        for message in messages:
            if "Memory Size" in message:
                memory_val = int(message.split("Memory Size: ")[1].split(" MB")[0])
                duration_val = float(message.split("Duration: ")[1].split(" ms")[0])
                result_list.append({"Memory": memory_val,"Duration": duration_val})

        #Get Average
        mem_duration_dict2 = defaultdict(list)

        for md in result_list:
            mem_duration_dict2[md['Memory']].append(md['Duration'])

        avg_mem_duration = [{'mem': mem, 'rt': sum(durations)/len(durations)} for mem, durations in mem_duration_dict2.items()]

        print(avg_mem_duration,end="\n")

        
        ## identfy target functions in the appliaction
        newRts={
            'cloudType':"public",
            "provider":"lambda",
            "rts":avg_mem_duration
        }

        # Find the function with the matching functionShortName
        matching_function = next(
            (fn for fn in appliaction.get('functions') if fn["functionShortName"] == function.split('_')[-1]),
            None
        )

        # Insert the new response times data if a matching function is found
        if matching_function:
            if len(matching_function.get('responseTimes'))==0: matching_function.get('responseTimes').append(newRts)
            else:
                responseTimes=matching_function.get('responseTimes')
                isFound=False
                for rt in responseTimes:
                    if rt.get('cloudType')=='public' and rt.get('provider')=='lambda':
                        rt['rts']=avg_mem_duration
                        isFound=True
                        break
                    
                
                if isFound==False:
                    matching_function.get('responseTimes').append(newRts)

        applicationCollection.update_one({'_id': ObjectId(appliaction.get('_id'))}, {'$set': appliaction})
        print('Lambda Log collection ends')

      


        