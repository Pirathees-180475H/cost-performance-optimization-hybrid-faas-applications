from flask import request, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from applicationService import get_applications_by_user_id_logic

client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['cloudPerformace']  # Replace 'mydatabase' with your database name
userCollection = db['users']  # Replace 'users' with your collection name


#Register
def create_user(request):
    try:
        user = request.json
        if 'name' not in user or 'email' not in user or 'password' not in user:
            raise ValueError('Name and Email are required')
        
        ##Validate unique user name and email
        validate_user_name_email(user['name'],user['email'])

        #Set empty attributes
        user['applicationNames']=[]

        # Insert the user document into the MongoDB collection
        result = userCollection.insert_one(user)
        
        # Return the inserted document ID
        response = {'status':"Success",'message': 'User created successfully.', 'id': str(result.inserted_id)}
        return jsonify(response), 201
    
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400

def login_user(request):
    try:
        credentials = request.json
        if 'name' not in credentials or 'password' not in credentials:
            raise ValueError('Name and Password are required')
     
        user = userCollection.find_one({'name':credentials['name'],'password':credentials['password']})

        if user:
            response = {'status':"Success",'message': 'User ID for this user is', 'id': str(user['_id'])}
        else:
            response = {'status':"Success",'message': 'Name or Password is Incorrect !'}

        # Return the inserted document ID
        return jsonify(response), 201
    
    except Exception as e:
        response = {'status':"Error",'message': str(e)}
        return jsonify(response), 400

def get_user(user_id):
    try:
        user = userCollection.find_one({'_id': ObjectId(user_id)})
        applicationsList=get_applications_by_user_id_logic(user_id)

        if user:
            # Remove the MongoDB-generated "_id" field and convert it to a string
            user.pop('_id')
            user= update_user_details_to_return(user,applicationsList)
            response = {'status':"Success",'user': user}
            return jsonify(response)
        else:
            raise ValueError("user not found!")
    
    except Exception as e:
        response = {"status":"Error",'message': str(e)}
        return jsonify(response), 404

# Update User Configurations
def update_user_cloud_configs(user_id,request):
    try:
        user = userCollection.find_one({'_id':ObjectId(user_id)})
        cloudConfigBody=request.json
        if user:
            #Set empty cloud Config
            if user.get('cloudConfig') is None : user['cloudConfig']=[] # set empty configuration
            user['cloudConfig']=cloudConfigBody
            userCollection.update_one({'_id': ObjectId(user_id)}, {'$set': user})
            user = userCollection.find_one({'_id': ObjectId(user_id)})
            user.pop('_id')
            response = {'status':"Success",'user': user}
            return jsonify(response)

        else:
            raise ValueError("User Not Found !")
    except Exception as e:
        response ={"status":"Error",'message':str(e)}
        return jsonify(response), 404


#Modify it to return all Details
def update_user_details_to_return(user,applicationsList):
    user['totalApplications']=len(applicationsList)

    totalFunctions=0
    publicFunctions=0
    privateFunctions=0
    typeWise={}
  
    for application in applicationsList:
        for function in application.get("functions"):
            cloud=function.get('cloudType')

            functionType=function.get('functionType')
            totalFunctions+=1
            if((cloud is not None) and (cloud=='public')):
                publicFunctions+=1
            
            if((cloud is not None) and (cloud=='private')):
                privateFunctions+=1

            if(typeWise.get(functionType) is None):
                typeWise[functionType]=1
            else:
                typeWise[functionType]=typeWise.get(functionType)+1

    
    user['totalFunctions']=totalFunctions
    user['totalPrivateFunctions']=privateFunctions
    user['totalPublicFunctions'] = publicFunctions
    user['functionsTypeWise']=typeWise

    return user

def validate_user_name_email(name,email):
    user = userCollection.find_one({'name': name})
    if user:
        raise ValueError("User Name alrady exists!")
    
    user = userCollection.find_one({'email':email })
    if user:
        raise ValueError("Email already exists!")


def update_user(user_id, request):
    try:
        user = request.json
        if 'name' not in user or 'email' not in user:
            raise ValueError('Name and email are required.')

        result = userCollection.update_one({'_id': ObjectId(user_id)}, {'$set': user})
        if result.modified_count == 1:
            response = {'message': 'User updated successfully.'}
            return jsonify(response)
        else:
            raise ValueError('User not found.')

    except Exception as e:
        response = {'message': str(e)}
        return jsonify(response), 404
    

def delete_user(user_id):
    try:
        result = userCollection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 1:
            response = {'message': 'User deleted successfully.'}
            return jsonify(response)
        else:
            raise ValueError('User not found.')

    except Exception as e:
        response = {'message': str(e)}
        return jsonify(response), 404