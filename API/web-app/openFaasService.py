import time

def deploy_application_in_private_cloud_openFaas(application):
    print('Private deployment')
    time.sleep(10)
    #set feed backs
    feedbacks=application.get('feedback')
    feedbacks.append('Deployed in private cloud')
    application['feedback']=feedbacks

    #set up application status
    status=application.get('status')
    if 'Private_deployed' not in application.get('status'): status.append('Private_deployed')  # Append the new status 'Public_deployed'
    application['status']=status
    return 5

def invoke_application_in_private_cloud_openFaas(application,invocationCount):
    print('Private Invocation')
    time.sleep(10)
    return 2

def collect_logs_in_private_cloud_openFaas(application):
    print('Private Log collection')
    time.sleep(5)
    return 4


    

