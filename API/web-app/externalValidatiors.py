import os

def functions_name_collector(folder_location):
    functions = []

    for file in os.listdir(folder_location):
        if file.endswith(".py"):
            function_name = os.path.splitext(file)[0]
            functions.append(function_name)

    return functions
