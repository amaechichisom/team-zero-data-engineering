import json

def log_operation(operation_data):
    with open("file_operations_log.json", "a") as log_file:
        log_file.write(json.dumps(operation_data) + "\n")
