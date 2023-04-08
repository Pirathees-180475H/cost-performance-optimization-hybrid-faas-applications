#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from io import BytesIO
import time
import zipfile
import numpy as np
import boto3
from tqdm import tqdm
from datetime import datetime, timezone
from time import gmtime, strftime
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


# In[2]:


##SetUP AWS Credentials
aws_accesskey="AKIASIU5OS3DWXHEHEFR"
aws_secretKey="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"
aws_region="ap-south-1"
lambda_client = boto3.client('lambda',aws_region)


# In[36]:


function_prefix='hybrid_public_app6'

app_folder_location = "C:/Users/PTS/Desktop/FYP/functions/App6"

functions = []

for file in os.listdir(app_folder_location):
    if file.endswith(".py"):
        function_name = os.path.splitext(file)[0]
        functions.append(function_name)

print(functions)


# In[43]:


## Code to create new empty functions with function_prefix+functionName


# In[62]:


# loop through the function files and update their code in Lambda

lambda_functions_names=[]

for function_file in os.listdir(app_folder_location):
    # check if the file is a Python file
    if function_file.endswith('.py'):
        # create a buffer to store the zip file contents
        buf = BytesIO()
        
        # create a zipfile containing the function code
        with zipfile.ZipFile(buf, 'w') as z:
            z.write(os.path.abspath(os.path.join(app_folder_location, function_file)), 'lambda_function.py')
        
        # move the buffer pointer to the start of the buffer
        buf.seek(0)
        
        # read the contents of the buffer
        pkg = buf.read()
        
        # update the function code in Lambda
        FunctionName='{}_{}'.format(function_prefix, os.path.splitext(function_file)[0])
        
        print("Updating Function to lambda -",FunctionName)
        
        lambda_functions_names.append(FunctionName)
                                    
        lambda_client.update_function_code(FunctionName='{}_{}'.format(function_prefix, os.path.splitext(function_file)[0]), ZipFile=pkg)

print(lambda_functions_names)


# In[45]:


#available_mem_list=[128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1280, 1344, 1408, 1472, 1536, 1600, 1664, 1728, 1792, 1856, 1920, 1984, 2048, 2112, 2176, 2240, 2304, 2368, 2432, 2496, 2560, 2624, 2688, 2752, 2816, 2880, 2944, 3008]

available_mem_list=[128, 192, 256]


# In[64]:


#Invoke In functions in multiple Configurations
for mem in available_mem_list:
    print('Memory: {} Timestamp: {} UTC: {}'.format(mem,time.time(),strftime("%d %b %Y %H:%M:%S +0000", gmtime())))
        
    for function in functions:
        print('Function: {} Timestamp: {} UTC: {}'.format(function,time.time(),strftime("%d %b %Y %H:%M:%S +0000", gmtime())))
        lambda_client.update_function_configuration(FunctionName='{}_{}'.format(function_prefix, function), MemorySize=mem)
        time.sleep(1)
        for i in tqdm(range(2)):
            time.sleep(2)
            lambda_client.invoke(FunctionName='{}_{}'.format(function_prefix, function), InvocationType='Event')


# In[49]:


# Collect Logs
logclient = boto3.client('logs')
from datetime import datetime, timedelta
import time


# In[65]:


logclient = boto3.client('logs')

for function in functions:
    print("\n")
    log_group_name="/aws/lambda/"+function_prefix+"_"+function
    
    #Prepare Query 
    query_f1 = logclient.start_query(
        logGroupName=log_group_name,
        queryString="fields @timestamp, @message| sort @timestamp desc",
        startTime=int((datetime.today() - timedelta(hours=15)).timestamp()),
        endTime=int(datetime.now().timestamp()),
        limit=10000
    )
    
    #Get Results of the Query
    query_results_f1 = logclient.get_query_results(queryId=query_f1['queryId'])

    #Response will contains results(logs)
    response = None

    while response == None or response['status'] == 'Running':
        print("function - "+function_prefix + function +'Waiting for query to complete ...')
        time.sleep(1)
        response = logclient.get_query_results(
            queryId=query_f1['queryId']
        )

    print("Total logs for "+function_prefix+" "+function)
    print(+len(response['results']))

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



# In[97]:


print(len(result_list))


# In[ ]:




