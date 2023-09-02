from flask import Flask,request,Response,jsonify
from userService import create_user, get_user,login_user,update_user_cloud_configs
from applicationService import create_application,get_functions_of_user,validate_application,status_of_application,get_applications_by_user_id_handler,get_applications_by_application_id;
from deploymentService import deploy_application_new_and_update_public_cloud,deploy_application_new_and_update_private_cloud,deploy_application_new_and_update_hybrid_cloud
from deploymentService import invoke__collect_logs_public,invoke__collect_logs_private,invoke_collect_logs_hybrid
import time
from flask_cors import CORS
from azureService import azure
from models.Main import modelsMain

### Configurations
app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'], allow_headers=['Content-Type'])


@app.route('/azure')
def azure_route():
    azure()
    return "Done" 


#index Route
@app.route('/')
def index():
    return "WelCome"

#Create User
@app.route('/users', methods=['POST'])
def create_user_route():
    return create_user(request)

#Login User
@app.route('/login',methods=['POST'])
def login_route():
    return login_user(request)

#Get User
@app.route('/users/<user_id>', methods=['GET'])
def get_user_route(user_id):
    return get_user(user_id)

##update cloud configurations
@app.route('/user/cloudCongif/<user_id>',methods=['POST'])
def update_cloud_config_route(user_id):
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    elif request.method == 'POST':
        update_user_cloud_configs(user_id,request)
    else :
        return jsonify({'status': 'Error'})

#Validate application for user
@app.route('/application/validate/<user_id>',methods=['POST'])
def validate_application_route(user_id):
    return validate_application(user_id,request)

#Create application under user
@app.route('/application/<user_id>',methods=['POST'])
def create_application_route(user_id):
    return create_application(user_id,request)

#Get Applications of the user
@app.route('/application/user/<user_id>',methods=['GET'])
def get_applications_of_user_route(user_id):
    return get_applications_by_user_id_handler(user_id)

#Get Application by using application Id
@app.route('/application/<app_id>',methods=['GET'])
def get_application_by_id_route(app_id):
    return get_applications_by_application_id(app_id)


#Get Functions of the user
@app.route('/application/functions/<user_id>',methods=['GET'])
def get_functions_route(user_id):
    return get_functions_of_user(user_id)

                     #DEPLOY

##Deploy a application in public cloud
@app.route('/application/deploy/public/<app_id>',methods=['POST'])
def deploy_application_public_route(app_id):
    return deploy_application_new_and_update_public_cloud(app_id,request)

##Deploy a application in private
@app.route('/application/deploy/private/<app_id>',methods=['POST'])
def deploy_application_private_route(app_id):
    return deploy_application_new_and_update_private_cloud(app_id,request)

##Deploy a application in hybrid
@app.route('/application/deploy/hybrid/<app_id>',methods=['POST'])
def deploy_application_hybrid_route(app_id):
    return deploy_application_new_and_update_hybrid_cloud(app_id,request)

            #Invoke
##Invoke and collect logs public
@app.route('/application/invoke/public/<app_id>',methods=['PUT'])
def invoke_collect_logs_public_route(app_id):
    return invoke__collect_logs_public(app_id,request)

#Invoke and collect logs private
@app.route('/application/invoke/private/<app_id>',methods=['PUT'])
def invoke_collect_logs_private_route(app_id):
    return invoke__collect_logs_private(app_id,request)

#Invoke and collect logs hybrid 
@app.route('/application/invoke/hybrid/<app_id>',methods=['PUT'])
def invoke_collect_logs_hybrid_route(app_id):
    return invoke_collect_logs_hybrid(app_id,request)

        #Optimize
# optimize the application
@app.route('/application/optimize/<app_id>',methods=['PUT'])
def optimization_route(app_id):
    return modelsMain(app_id,request)
    

## Get status of the application
@app.route('/applicationStatus/<application_id>', methods=['GET'])
def get_status_of_application_route(application_id):
    return status_of_application(application_id)

if __name__ == "__main__":
    app.run(debug=True)



