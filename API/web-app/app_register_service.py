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
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    abc=1
    for edge in edges:
        if len(edge) !=3:
            raise ValueError("Edge Size must be 3!")
        
        if(edge[0] > len(functions) or edge[1] > len(functions)):
            raise ValueError("Edges have invalid node numbers")
        
        if(edge[2] >1):
            raise ValueError("Probability Taking wrong value !")

