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
from lambdaService import deploy_application_in_public_cloud_lambda,invoke_public__lambda_functions_in_diffrent_mem,collect_lambda_logs
from openFaasService import deploy_application_in_private_cloud_openFaas,invoke_application_in_private_cloud_openFaas,collect_logs_in_private_cloud_openFaas

client = MongoClient('mongodb://localhost:27017/')  
db = client['cloudPerformace']  
userCollection = db['users'] 
applicationCollection=db['applications'] 

def deploy_application_new_and_update_hybrid_cloud(app_id,request):
    time.sleep(10)
    application = applicationCollection.find_one({'_id': ObjectId(app_id)})
    application['feedback']=[] #Set feedback to empty when process starts
    try:
        if application is None: raise ValueError("Application Not Found!")

        #Public and private
        deploy_application_in_public_cloud_lambda(application)
        deploy_application_in_private_cloud_openFaas(application)

        applicationCollection.update_one({'_id': ObjectId(app_id)}, {'$set': application})

        return jsonify("Deployed New function / Updated Function Code in hybrid cloud !!!"), 201
        
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400



def deploy_application_new_and_update_public_cloud(app_id,request):
    time.sleep(10)
    application = applicationCollection.find_one({'_id': ObjectId(app_id)})
    application['feedback']=[] #Set feedback to empty when process starts
    try:
        if application is None: raise ValueError("Application Not Found!")
        #Only in public
        deploy_application_in_public_cloud_lambda(application)

        applicationCollection.update_one({'_id': ObjectId(app_id)}, {'$set': application})

        return jsonify("Deployed New function / Updated Function Code !!!"), 201
    
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400


def deploy_application_new_and_update_private_cloud(app_id,request):
    time.sleep(10)
    application = applicationCollection.find_one({'_id': ObjectId(app_id)})
    application['feedback']=[] #Set feedback to empty when process starts

    try:
        if application is None: raise ValueError("Application Not Found!")
        
        #Only in private
        deploy_application_in_private_cloud_openFaas(application)

        applicationCollection.update_one({'_id': ObjectId(app_id)}, {'$set': application})

        return jsonify("Deployed New function / Updated Function Code in private cloud !!!"), 201
    
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400
    



def invoke_collect_logs_hybrid(app_id,request):

    invoke__collect_logs_public(app_id,request)
    invoke__collect_logs_private(app_id,request)



def invoke__collect_logs_public(app_id,request):
    application = applicationCollection.find_one({'_id': ObjectId(app_id)})
    try:
        InvokeConfig = request.json

        if application is None: raise ValueError("Application Not Found!")
        if 'publicMemList' not in InvokeConfig  or len(InvokeConfig.get('publicMemList'))==0 :raise ValueError("Please provide mem list!!")
        if 'invocationCount' not in InvokeConfig : raise ValueError("Please provide invocation count")

        deployed_lambda_functions=application.get('lambdaFunctionNames')
        if deployed_lambda_functions is None or len(deployed_lambda_functions)==0: raise ValueError("Functions of this Application Not deployed yet!!")
            
      
        invoke_public__lambda_functions_in_diffrent_mem(application,deployed_lambda_functions,InvokeConfig.get('publicMemList'),int(InvokeConfig.get('invocationCount')))
        collect_lambda_logs(application,deployed_lambda_functions)

        return jsonify("Invoked and logs collected For Public Cloud!!!"), 201
    
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400


def invoke__collect_logs_private(app_id,request):
    application = applicationCollection.find_one({'_id': ObjectId(app_id)})
    try:
        InvokeConfig = request.json
        if application is None: raise ValueError("Application Not Found!")
        if 'privateMemList' not in InvokeConfig  or len(InvokeConfig.get('privateMemList'))==0 :raise ValueError("Please provide mem list!!")
        if 'invocationCount' not in InvokeConfig : raise ValueError("Please provide invocation count")

        #Only invoke in private
        invoke_application_in_private_cloud_openFaas(application,int(InvokeConfig.get('invocationCount')))
        collect_logs_in_private_cloud_openFaas(application)

        return jsonify("Invoked and logs collected For Private Cloud!!!"), 201
    
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400
