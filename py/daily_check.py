import os
import sys
import subprocess
import datetime
import json

# for daily system check for bccard proxy gw
# created by bacsumu11 2023-06

# common function to sum from string array
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


# result var
today_str = datetime.datetime.now().strftime("%Y%m%d")
result_json = {}
result_saving_path = "/mnt/cron/bc_daily_check/"
file_path_of_result = result_saving_path+today_str+"_result.json"   # saving file pattern is {YYYYMMDD}_result.json
#file_path_of_result = "/mnt/cron/bc_daily_check/result.json"

# if saving file path is received from argv then file_path_of_result is replaced from argv
print("system argv="+",".join(sys.argv))
if len(sys.argv) > 1:
    file_path_of_result = sys.argv[1]

# 1. check if log file is updated
current_time = datetime.datetime.now()
print("current_time=%s" % current_time)

# 1. /logs/rcs.log, /logs/bccard.log check last modified time of log files
last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime("/logs/rcs.log"))
minutes_difference_rcslog  = (current_time - last_modified_time).total_seconds() // 60
#print("/logs/rcs.log interval of minute : minutes_difference=%.2f, current_time=%s, last_modified_time=%s"
#      % (minutes_difference_rcslog, current_time, last_modified_time))

last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime("/logs/bccard.log"))
minutes_difference_bccardlog  = (current_time - last_modified_time).total_seconds() // 60
#print("/logs/bccard.log interval of minute : minutes_difference=%.2f, current_time=%s, last_modified_time=%s"
#      % (minutes_difference_bccardlog, current_time, last_modified_time))

# make result data
result_json["log-update-elapsed-time"] = {}
if minutes_difference_rcslog > 5.0 or minutes_difference_bccardlog > 5.0:   # if elapsed minute of last log update time is over 5 minutes then result is fail
    result_json["log-update-elapsed-time"]["result"] = "fail"
    result_json["log-update-elapsed-time"]["code"] = 2001
    result_json["log-update-elapsed-time"]["message"] = "last log update time is over 5 minutes"
else:
    result_json["log-update-elapsed-time"]["result"] = "success"
    result_json["log-update-elapsed-time"]["code"] = 1000
    result_json["log-update-elapsed-time"]["message"] = "success"


# 2. check ping/pong ids
command = "tail -1000 /logs/bccard.log | grep 'PING' | grep -oP '(?<=U=\[)([^]]+)(?=\])' | sort | uniq"

proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
tempList = str(out).split("\n")
tempList = [x for x in tempList if x] #delete empty elements
#print("PING ids in /logs/bccard.log [count:%d] \n%s" % (len(tempList), tempList))

# make result data
result_json["client-session"] = {}
if minutes_difference_bccardlog > 5.0:
    result_json["client-session"]["result"] = "fail"
    result_json["client-session"]["code"] = 2001
    result_json["client-session"]["message"] = "last log update time is over 5 minutes"
elif len(tempList) <= 0:
    result_json["client-session"]["result"] = "fail"
    result_json["client-session"]["code"] = 2002
    result_json["client-session"]["message"] = "there is no connected session"
else:
    result_json["client-session"]["result"] = "success"
    result_json["client-session"]["code"] = 1000
    result_json["client-session"]["message"] = "ping/pong session list= "+",".join(tempList)

# 3. check DLV count
command = "cat /logs/bccard.log | grep -E 'DAK' |grep -oP '(?<=U=\[)([^]]+)(?=\])' | sort | uniq -c |awk '{print $2, $1}'"

proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
#print("DAK count in /logs/bccard.log\n%s" % (out))
tempList = str(out).split("\n")
tempList = [x for x in tempList if x] #delete empty elements
sumResult = count_result_code_from_arry(tempList)

# make result data
result_json["client-delive"] = {}
if minutes_difference_bccardlog > 5.0:
    result_json["client-delive"]["result"] = "fail"
    result_json["client-delive"]["code"] = 2001
    result_json["client-delive"]["message"] = "last log update time is over 5 minutes"
elif sumResult["sum"] > 0:
    result_json["client-delive"]["result"] = "success"
    result_json["client-delive"]["code"] = 1000
    result_json["client-delive"]["message"] = "delive list(sum="+str(sumResult["sum"])+")= "+",".join(tempList)
else:
    result_json["client-delive"]["result"] = "fail"
    result_json["client-delive"]["code"] = 2002
    result_json["client-delive"]["message"] = "there is no delived count"

# 4. check RPT count
command = "cat /logs/bccard.log | grep -E 'RPT' |grep -oP '(?<=RPT)(.+)'|sed 's/K=\[[^]]*\]//'|sed 's/N=\[[^]]*\]//'|sed 's/[UNR=]//g'|sed 's/\[//g'|sed 's/\]//g'|sort|uniq -c|awk '{print $2, $3, $1}'"

proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
#print("RPT count in /logs/bccard.log\n%s" % (out))
tempList = str(out).split("\n")
tempList = [x for x in tempList if x] #delete empty elements
sumResult = count_result_code_from_arry(tempList)

# make result data
result_json["client-report"] = {}
if minutes_difference_bccardlog > 5.0:
    result_json["client-report"]["result"] = "fail"
    result_json["client-report"]["code"] = 2001
    result_json["client-report"]["message"] = "last log update time is over 5 minutes"
elif (sumResult["success_sum"] + sumResult["fail_sum"]) == 0:
    result_json["client-report"]["result"] = "fail"
    result_json["client-report"]["code"] = 2002
    result_json["client-report"]["message"] = "there is no report count"
else:
    result_json["client-report"]["result"] = "success"
    result_json["client-report"]["code"] = 1000
    result_json["client-report"]["message"] = "success count="+str(sumResult["success_sum"])+",fail count="+str(sumResult["fail_sum"])

# 5. check RPT of RCS
command = "cat /logs/rcs.log | grep RPT | grep -v RPT_RESULT | grep RECV | grep -oP '(?<=RPT)(.+)'|sed 's/K=\[[^]]*\]//'|sed 's/T=\[[^]]*\]//'|sed 's/CNT=\[[^]]*\]//'|sed 's/N=\[[^]]*\]//'|sed 's/[UR=]//g'|sed's/\[//g'|sed 's/\]//g'|sort|uniq -c|awk '{print $2, $3, $1}'"

proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
#print("RPT count in /logs/rcs.log\n%s" % (out))
tempList = str(out).split("\n")
tempList = [x for x in tempList if x] #delete empty elements
sumResult = count_result_code_from_arry(tempList)

# make result data
result_json["rcs-report"] = {}
if minutes_difference_rcslog > 5.0:
    result_json["rcs-report"]["result"] = "fail"
    result_json["rcs-report"]["code"] = 2001
    result_json["rcs-report"]["message"] = "last log update time is over 5 minutes"
elif (sumResult["success_sum"] + sumResult["fail_sum"]) == 0:
    result_json["rcs-report"]["result"] = "fail"
    result_json["rcs-report"]["code"] = 2002
    result_json["rcs-report"]["message"] = "there is no rcs report count"
else:
    result_json["rcs-report"]["result"] = "success"
    result_json["rcs-report"]["code"] = 1000
    result_json["rcs-report"]["message"] = "success count="+str(sumResult["success_sum"])+",fail count="+str(sumResult["fail_sum"])


# 5. check RPT_RESULT of RCS
command = "cat /logs/rcs.log | grep RPT_RESULT | grep RECV | grep -oP '(?<=RPT_RESULT)(.+)'|sed 's/K=\[[^]]*\]//'|sed 's/T=\[[^]]*\]//'|sed 's/CNT=\[[^]]*\]//'|sed 's/N=\[[^]]*\]//'|sed 's/[UR=]//g'|sed 's/\[//g'|sed 's/\]//g'|sort|uniq -c|awk '{print $2, $3, $1}'"

proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
#print("RPT_RESULT count in /logs/rcs.log\n%s" % (out))
tempList = str(out).split("\n")
tempList = [x for x in tempList if x] #delete empty elements
sumResult = count_result_code_from_arry(tempList)

# make result data
result_json["rcs-report_result"] = {}
if minutes_difference_rcslog > 5.0:
    result_json["rcs-report_result"]["result"] = "fail"
    result_json["rcs-report_result"]["code"] = 2001
    result_json["rcs-report_result"]["message"] = "last log update time is over 5 minutes"
elif (sumResult["success_sum"] + sumResult["fail_sum"]) == 0:
    result_json["rcs-report_result"]["result"] = "fail"
    result_json["rcs-report_result"]["code"] = 2002
    result_json["rcs-report_result"]["message"] = "there is no rcs report count"
else:
    result_json["rcs-report_result"]["result"] = "success"
    result_json["rcs-report_result"]["code"] = 1000
    result_json["rcs-report_result"]["message"] = "success count="+str(sumResult["success_sum"])+",fail count="+str(sumResult["fail_sum"])

# 6. check AUTH of RCS
command = "cat /logs/rcs.log | grep AUTH | grep RECV | grep -oP '(?<=AUTH)(.+)'|sed 's/T=\[[^]]*\]//'|sed 's/K=\[[^]]*\]//'|sed 's/DESC=\[[^]]*\]//'|sed 's/[U(CODE)=]//g'|sed 's/\[//g'|sed 's/\]//g'|sort|uniq -c|awk '{print $2, $3, $1}'"

proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
#print("AUTH count in /logs/rcs.log\n%s" % (out))
tempList = str(out).split("\n")
tempList = [x for x in tempList if x] #delete empty elements
sumResult = count_result_code_from_arry(tempList)

# make result data
result_json["rcs-auth"] = {}
if minutes_difference_rcslog > 5.0:
    result_json["rcs-auth"]["result"] = "fail"
    result_json["rcs-auth"]["code"] = 2001
    result_json["rcs-auth"]["message"] = "last log update time is over 5 minutes"
elif sumResult["fail_sum"] > 0:
    result_json["rcs-auth"]["result"] = "fail"
    result_json["rcs-auth"]["code"] = 2002
    result_json["rcs-auth"]["message"] = "auth request success count="+str(sumResult["success_sum"])+",fail count="+str(sumResult["fail_sum"])
else:
    result_json["rcs-auth"]["result"] = "success"
    result_json["rcs-auth"]["code"] = 1000
    result_json["rcs-auth"]["message"] = "auth request success count="+str(sumResult["success_sum"])+",fail count="+str(sumResult["fail_sum"])

print("daily check system resut\n----------------\n%s\n----------------" % json.dumps(result_json, indent=4))

# write result to file
with open(file_path_of_result, "w") as f:
    f.write(json.dumps(result_json, indent=4))

f.close()
print("result is writed to " + file_path_of_result)

# delete result.json older than 10 days
command = "find " + result_saving_path + " -name '*result.json' -type f -mtime +10 -delete"

proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
print("be deleted *rusult.json files older than 10 days\n%s" % (out))
