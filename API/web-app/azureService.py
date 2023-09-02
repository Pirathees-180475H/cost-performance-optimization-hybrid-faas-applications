from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.logic import LogicManagementClient
import requests
import json


def azure():

    credential = DefaultAzureCredential()
    subscription_id = "1166a1e9-7656-47a5-a47d-98891deb4ddf"
    resource_group_name = "faas"
    function_app_name = "CloudPerformers"
    function_name = "myFunction"  # Replace with your function name
    region = "East US"

   # Create an instance of the WebSiteManagementClient
    web_client = WebSiteManagementClient(credential, subscription_id)

    # Get the Function App details
    function_app = web_client.web_apps.get(resource_group_name, function_app_name)

    # Define the function name and code
    function_name = "myNewFunction"
    function_code = """
    import logging

    def main(req):
        logging.info('Function executed successfully!')
        return 'Function executed successfully!'
    """

    # Create the function
    function_config = {
        "config": {
            "bindings": [
                {
                    "name": "req",
                    "type": "httpTrigger",
                    "direction": "in",
                    "methods": [
                        "get",
                        "post"
                    ]
                },
                {
                    "name": "$return",
                    "type": "http",
                    "direction": "out"
                }
            ]
        },
        "files": {
            "index.py": function_code
        }
    }

    web_client.web_apps.create_or_update_function(resource_group_name, function_app_name, function_name, function_config)





