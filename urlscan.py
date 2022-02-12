import argparse
import requests
import json
import time
#
# [x] Connect to API
# [x] Send request
# [x] Handle JSON results
# [x] Save JSON results
# [x] Look for specific value in JSON file 
#     https://stackoverflow.com/questions/48155126/searching-a-json-file-for-a-specific-value-python
# [ ] Check if API return error message
# [ ] Display more verbous
# [ ] More args to get specific results (redirect, time, ...)
#
# functions
def saveFile(name, data):
    name = name.replace("/","_")
    name = name + ".json"
    with open(name, "w") as out_file:
        json.dump(data, out_file, indent=4)
        out_file.close()
    return name

def  printData(file):
    with open(file, "r") as data:
        work = json.load(data)
        remoteIP = work['data']['requests'][0]['response']['response']['remoteIPAddress']
        remotePort = work['data']['requests'][0]['response']['response']['remotePort']
        serverTime = work['data']['requests'][0]['response']['response']['headers']['date']
        print("remoteIP = ", remoteIP)
        print("remotePort = ", remotePort)
        print("serverTime = ", serverTime)

def status(status, message):
    if status == "ok":
        st = "[X]"
    elif status == "ko":
        st = "[!]"
    elif status == "out":
        st = "==>"
    elif status == "in":
        st = "<=="
    elif status == "err":
        st = "/!\\"
    elif status == "res":
        print("===",message,"===")
        return
    else:
        st =" "

    print(st," ", message)
#
#
parser = argparse.ArgumentParser()
parser.add_argument("url", help="url", metavar="< URL >")
parser.add_argument("-t", "--time", help="pause in seconds",nargs=1)
parser.add_argument("-v", "--verbose", help="verbose", action="store_true")
args = parser.parse_args()
#
# variables, parameters
if args.time:
    delay = args.time
else:
    delay = 10

msg = "URL to process: " + args.url
status("in",msg)
#
# api data parameters
api = 'https://urlscan.io/api/v1/scan/'
apikey = 'APIKEY'
headers = {'API-Key': apikey ,'Content-Type':'application/json'}
data = {'url': args.url, 'visibility':'public'}

#
# api request
try:
    response = requests.post(api , headers=headers, data=json.dumps(data))
    status("ok","API connexion successful")
    # pause 10 secs to get api response
    status("ok",str(delay) + " secs pause to let API process request")
    time.sleep(delay)
    r_json = response.json()
    status("ok","API response received")
    if args.verbose:
        print(r_json)

except:
    status("ko","API connexion failed")
    exit()

#
# CHECK IF ERRORS
if not r_json['api']:
    status("err","API process error")
    exit()
#
# RETRIEVE API RESULTS
# get api 'results url'
results_api_url = r_json['api']
#
msg = 'API results URL:' + results_api_url
status("out",msg)

# get api results via GET method to api 'results url'
results_response = requests.get(results_api_url)

#
# save results with json format
file = saveFile(args.url, results_response.json())
msg = "API results file generated: " + file
status("out", msg)

# display results
status("res","RESULTS")
printData(file)
# results = json.dumps(results_response.json(), indent=4)
# print("Results:\n", results)
#
