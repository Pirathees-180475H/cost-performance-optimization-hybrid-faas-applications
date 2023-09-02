from flask import request, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
import time
from externalValidatiors import functions_name_collector


client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['cloudPerformace']  # Replace 'mydatabase' with your database name
userCollection = db['users']  # Replace 'users' with your collection name
applicationCollection=db['applications']


def create_application(userId,request):
    try:
        application = request.json
        user = userCollection.find_one({'_id': ObjectId(userId)})

        #Validate User
        if  user is None:
            raise ValueError("user not found!")
        
        #Validate Application Properties and add it with user
        if 'applicationName' not in application:
            raise ValueError("Application Name is Required !")
        
        if 'applicationLocation' not in application:
            raise ValueError("ApplicationLocation is Required")
        
        if 'functionsCount' not in application:
            raise ValueError("Function Count is Required !")
        
        if int(application.get('functionsCount')) != len(functions_name_collector(application.get('applicationLocation'))):
            raise ValueError("Function Count and Application location are contradict!")
        
        if application.get('applicationName') in user.get('applicationNames', []):
             raise ValueError("Application name already exists, Try Diffrent Name")
        

        ## Validate Each Functions
        if 'functions' not in application or len(application.get('functions'))==0:
            raise ValueError("Functions List can't be empty")
        
        validate_functions(application.get('functions'),application.get('functionsCount'),application.get('applicationLocation'))

        ## Validate Edges
        if 'edges' not in application or len(application.get('edges'))==0:
            raise ValueError("Edges List can't be empty")
        
        validate_edges(application.get('edges'),application.get('functions'))


        #Update User collection
        application_names = user.get('applicationNames', [])
        application_names.append(application.get('applicationName'))
        user['applicationNames'] = application_names

        userCollection.update_one({'_id': ObjectId(userId)}, {'$set': user})
        
        # Insert the user document into the MongoDB collection
        application['userId']=userId
        application['status']=['Pending']
        application['date']=datetime.now()
        application['feedback']=[]
        result = applicationCollection.insert_one(application)
        
        # Return the inserted document ID
        response = {'status':"Success",'message': 'Application created successfully.', 'id': str(result.inserted_id)}
        return jsonify(response), 201
    
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 201

#Purpose of validating application
def validate_application(userId,request):
    try:
        application = request.json
        user = userCollection.find_one({'_id': ObjectId(userId)})

        #Validate User
        if  user is None:
            return jsonify("user not found!") , 201
        
        #Validate Application Properties and add it with user
        if 'applicationName' not in application or application.get('applicationName')=="":
            return jsonify("Application Name is Required !"),201
        
        if 'applicationLocation' not in application or application.get('applicationLocation')=="":
            return jsonify("Application Location is Required!"),201
        
        if 'functionsCount' not in application or application.get('functionsCount')=="":
            return jsonify("Function Count is Required !"),201
        
        if 'functions' not in application or application.get('functions')==[]:
            return jsonify("Functions  Required !"),201
        
        if application.get('applicationName') in user.get('applicationNames', []):
            return jsonify("Application name already exists, Try Diffrent Name"),201
        
        
        applicationLocation=application.get('applicationLocation')
        functions=application.get('functions')
        functionNames=[]
        functionShortNames=[]

        for function in functions:  
                if function.get('functionShortName') not in functions_name_collector(applicationLocation):
                    return jsonify("Short Name not matched with application Location !"),201
                
                if function.get('functionName') in functionNames:
                    return jsonify("Function Name must uinque!"),201
                else:
                    functionNames.append(function.get('functionName'))

                if function.get('functionShortName') in functionShortNames:
                    return jsonify("Function Short Name must uinque!"),201
                else:
                    functionShortNames.append(function.get('functionShortName'))

        # Return the inserted document ID
        return jsonify("valid"), 201
    
    except Exception as e:
        response = str(e)
        return jsonify(response), 201


#Get Applications of user
def get_applications_by_user_id_logic(userId):
    #applications = applicationCollection.find({'userId': userId})
    applications = list(applicationCollection.find({'userId': userId}).sort('date', -1))
    for application in applications:
        id=application.pop('_id')
        application['id']=str(id)
    return list(applications)

#Get Applications_by_user_id method
def get_applications_by_user_id_handler(user_id):
    try:
        user = userCollection.find_one({'_id': ObjectId(user_id)})
        if user is None:
            raise ValueError("User Not Found!")
            
        applications=get_applications_by_user_id_logic(user_id)
        response = {'status':"Success",'message': 'Applications Retrived for the user are', 'applications': applications}
        return jsonify(response), 201

    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400

#Get appluication by application id
def get_applications_by_application_id(applicationId):
    try:
        application = applicationCollection.find_one({'_id': ObjectId(applicationId)})
        if application is None:
            raise ValueError("Application Not Found!")
            
        application['id']=str(application.pop('_id'))
        response = {'status':"Success",'message': 'Application Retrived successfully.', 'application': application}
        return jsonify(response), 201

    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400


##Validate Each Functions
def validate_functions(functions,functionCount,folder_location):
    validFunctionTypes=['CPU',"Network","Disk"]
    functionNames=[]
    functionShortNames=[]

    if len(functions) != int(functionCount):
        raise ValueError("Check Function Count!")
    
    for function in functions:
        if 'functionName' not in function:
            raise ValueError("Please Name the functions")
        
        if 'functionShortName' not in function:
            raise ValueError("Please give short Name for the function")
        
        if function.get('functionShortName') not in functions_name_collector(folder_location):
            raise ValueError("Please provide valid short name")
        
        if 'functionType' not in function:
            raise ValueError('Please Provide function type')
        
        if function.get('functionType') not in validFunctionTypes:
            raise ValueError("Please provide valid functionType")
        
        #Validate Unique FunctionNames 
        if function.get('functionName') in functionNames:
            raise ValueError("Function Names must be unique")
        else:
            functionNames.append(function.get('functionName'))

        #Validate Unique FunctionShort Names
        if function.get('functionShortName') in functionShortNames:
            raise ValueError("Function Short Names must be unique")
        else:
            functionShortNames.append(function.get('functionShortName'))

##Validate Edges
def validate_edges(edges,functions):
    for edge in edges:
        if len(edge) !=3:
            raise ValueError("Edge Size must be 3!")
        
        if(edge[0] > len(functions) or edge[1] > len(functions)):
            raise ValueError("Edges have invalid node numbers")
        
        if(edge[2] >1):
            raise ValueError("Probability Taking wrong value !")


##Get functions of the USER
def get_functions_of_user(user_id):
    applications=get_applications_by_user_id_logic(user_id)
    response=[]

    for application in applications:
        for function in application.get('functions'):
            fn={}
            fn['name']=function.get('functionName')
            fn['date']=application.get('date')
            fn['applicationName']=application.get('applicationName')
            fn['category']=function.get('functionType')
            ##Set Response Times for Dashboard
            if('responseTimes' in function):
                for responseTime in function['responseTimes']:
                    if (responseTime['cloudType']=='public' and responseTime['provider']=='lambda' and 'rts' in responseTime):
                        fn['publicResponseTimes']=responseTime.get('rts')
                    
                    if (responseTime['cloudType']=='private' and responseTime['provider']=='openFaaS' and 'rts' in responseTime):
                        fn['privateResponseTimes']=responseTime.get('rts')

            ##End of setting up response times
            applicationStatus=application.get('status')

            if ('Pending' in applicationStatus) and ('Public_deployed' not in applicationStatus) and ('Private_deployed' not in applicationStatus):
                fn['status']='Pending'
            if ('Pending' not in applicationStatus) and ('Public_deployed' in applicationStatus) and ('Private_deployed' not in applicationStatus):
                fn['status']="Deployed in Public Cloud"
            if ('Pending' not in applicationStatus) and ('Public_deployed' not in applicationStatus) and ('Private_deployed' in applicationStatus):
                fn['status']="Deployed in Private Cloud"
            if ('Pending' not in applicationStatus) and ('Public_deployed'  in applicationStatus) and ('Private_deployed'  in applicationStatus):
                fn['status']="Deployed in Hybrid Cloud"
            response.append(fn)
    
    return response


def status_of_application(app_id):
    try:
        application = applicationCollection.find_one({'_id': ObjectId(app_id)})

        if application is None:
            raise ValueError("Application Not Found!")

        if 'feedback' not in application:
            response = []
        else:
            response = application['feedback']

        return response 
     
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400
    