import platform
import os
import sys
import subprocess
import datetime
import json
import re

### common function to sum from string array
"""
Counts the result code from an array.

Parameters:
    inArray (list): The input array containing the result codes.

Returns:
    dict: A dictionary with the following keys:
        - 'sum' (int): The sum of all the result codes.
        - 'success_sum' (int): The sum of the success result codes.
        - 'fail_sum' (int): The sum of the fail result codes.
"""
def count_result_code_from_arry(inArray):
    return_map = {"sum":0, "success_sum":0, "fail_sum":0}

    for tempLine in inArray:
        tempLineArray = tempLine.split(" ")

        if len(tempLineArray) == 2:
            return_map["sum"] += int(tempLineArray[1])

        elif len(tempLineArray) == 3:
            if "10000" == tempLineArray[1]:
                return_map["success_sum"] += int(tempLineArray[2])
            else:
                return_map["fail_sum"] += int(tempLineArray[2])
    return return_map

"""
Generates a JSON object with the specified key name, result, code, and message.

Args:
    keyName (str): The key name for the JSON object.
    result (any): The result value to be stored in the JSON object.
    code (int): The code value to be stored in the JSON object.
    message (str): The message value to be stored in the JSON object.

Returns:
    dict: A JSON object containing the key name, result, code, and message.
"""
def generate_result_json(code, message):

    item_json = {}
    result = "fail"

    if code == 1000:
        result = "success"

    item_json["result"] = result
    item_json["code"] = code
    item_json["message"] = message

    return item_json

"""
Executes a subprocess command and captures its output.

Args:
    command (str): The command to be executed.

Returns:
    list: A list of strings representing the output lines of the command.
"""
def subprocess_output_lines(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, err = proc.communicate()

    if err is not None:
        print(" [ERROR] %s : %s " % (command, err))

    return out.decode("utf-8").splitlines()

"""
Delete the result.json file that is older than 10 days for a given hostname.

Parameters:
- path (str): The path to the directory where the file is located.
- hostname (str): The hostname used to identify the file.

Returns:
None
"""
def delete_result_file(path, hostname):
    command = "find " + path + " -name '*result.json_" + hostname + "' -type f -mtime +10 -delete"

    outline = subprocess_output_lines(command)

    print("[info] be deleted : %s" % outline)

"""
Count the number of strings in a list that contain a specific target string.

Parameters:
- strings (List[str]): A list of strings to search through.
- target (str): The string to search for in each element of the list.

Returns:
- count (int): The number of strings that contain the target string.
"""
def count_specific_string(strings, target):
    count = 0
    for string in strings:
        if target in string:
            count += 1
    return count

### check command

def grep_access_5xx(logPath):
    grep_command = "grep '\" 50[0-9]' " + logPath

    if(platform.system() == "Windows"):
        grep_command = "findstr /R \" 50[0-9]\" "+ logPath

    print("[shell] " + grep_command)

    grep_out = subprocess_output_lines(grep_command)

    len_5xx = len(grep_out)
    count_502 = count_specific_string(grep_out, " 502 ")
    count_504 = count_specific_string(grep_out, " 504 ")

    result = " [REPORT] %s 5xx : %s, 502 : %s, 504 : %s " % (logPath, len_5xx, count_502, count_504)

    if count_502 > 10:
        return generate_result_json(2001, result)
    elif count_504 > 10:
        return generate_result_json(2002, result)
    elif len_5xx > 10:
        return generate_result_json(2003, result)

    return generate_result_json(1000, result)

def grep_error(logPath):
    grep_command = "grep ' [error]' " + logPath

    if(platform.system() == "Windows"):
        grep_command = "findstr /R \" [error]\" "+ logPath

    print("[shell] " + grep_command)
        
    grep_out = subprocess_output_lines(grep_command)

    len_error = len(grep_out)
    count_upstream = count_specific_string(grep_out, " upstream ")

    result = " [REPORT] %s Error : %s, upstream : %s " % (logPath, len_error, count_upstream)

    if count_upstream > 10:
        return generate_result_json(2001, result)
    elif len_error > 10:
        return generate_result_json(2002, result)

    return generate_result_json(1000, result)

def get_upstream_access_token():
    curl_command = "curl --request POST -k 'https://localhost:8443/api/1.0/token' --header 'Content-Type: application/json' --data-raw '{"clientId": "lguplus", "clientSecret": "SK.pwk293spkFFvhju"}' | jq .accessToken"
    token = subprocess_output_lines(curl_command)[0].decode("UTF-8")

    print("[shell] " + curl_command + " token : " + token)

    return token

def local_upstream_check(uri_path):

    ### 난수 나 동적 으로 바뀌는 결과는 검증 할 수 없음 ... (200)

    curl_command = "curl -o /dev/null -w '%{http_code}' --request POST -k 'https://+" uri_path "+' --header 'Content-Type: application/json' --data-raw '{\"clientId\": \"lguplus\", \"clientSecret\": \"SK.pwk293spkFFvhju\"}'"
    code = subprocess_output_lines(curl_command)[0].decode("UTF-8")

    print("[shell] " + curl_command + " res : " + code)

    result = " [REPORT] uri : https://localhost:8443/api/1.0/token code : " + code

    if code != "200":
        return generate_result_json(2001, result)

    return generate_result_json(1000, result)

### for daily system check for rbc proxy gw
# profile

## P. Environment

hostname = subprocess_output_lines("hostname")[0]
today = datetime.datetime.now().strftime("%Y%m%d")
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
current_time = datetime.datetime.now()

os.getcwd()
PATH = os.getcwd() + '/logs'
result_saving_path = PATH

if(platform.system() == "Windows"):
    PATH = os.getcwd() + '\py'
    result_saving_path = PATH

os.chdir(PATH)
file_path_of_result = result_saving_path + "/" +today+"_result.json_" + hostname

if len(sys.argv) > 1:
    file_path_of_result = sys.argv[1]

## P. Log Path Name
path_access_log = "access_api_8443.log"
path_error_log = "error_api_8443.log"

path_access_b_log = "access_api_8443.log." + yesterday
path_error_b_log = "error_api_8443.log." + yesterday

result_json = {}

print("[conf] hostname = %s" % hostname)
print("[conf] today_str = %s" % today)
# print("[conf] yesterday = %s" % yesterday)
print("[conf] file_path_of_result = %s" % file_path_of_result)
print("[conf] argv = "+",".join(sys.argv))
print("[conf] current_time = %s" % current_time)
print("[conf] PATH = %s" % PATH)

### Check List return Report
## 1. access 5xxs log Check
## 2. error [error] log Check
## 3. access api 8443 log yesterday Check
## 4. error api 8443 log yesterday Check

## 5. Local Auth Check
## 6. Local Chatbot Check

result_json["access_5xx_check_now"] = grep_access_5xx(path_access_log)
result_json["error_check_now"] = grep_error(path_error_log)
result_json["access_5xx_check_yesterday"] = grep_access_5xx(path_access_b_log)
result_json["error_check_yesterday"] = grep_error(path_error_b_log)

result_json["local_upstream_auth_check"] = local_upstream_check("api/v1/auth/token")
result_json["local_upstream_chatbot_check"] = local_upstream_check("api/v1/auth/chatbot")

print("---------------------------")

print( json.dumps(result_json, indent=4) )

print("---------------------------")

# write result to file
with open(file_path_of_result, "w") as f:
    f.write(json.dumps(result_json, indent=4))

f.close()
print("result is writed to " + file_path_of_result)

print("---------------------------")

delete_result_file(result_saving_path, hostname)
