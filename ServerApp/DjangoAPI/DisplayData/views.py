from django.conf.urls import url
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import json, requests, subprocess, os

# Create your views here.

@csrf_exempt
def formInputAPI(request):
    # print('in formInputAPI')
    if request.method == 'GET':

        results = cmdRunner(request.GET)

        return JsonResponse(results, safe=False)

def cmdRunner(x):
    cmd_command = x["command"].strip()
    modulename = x["modulename"].strip()
    print(cmd_command + "\n" + modulename)
    command_str = "python3 ../../maryam.py -e " + modulename + " " + cmd_command
    print(command_str)

    '''
    stream = os.popen(cmd_str)
    data = stream.read()
    
    print(data)

    return data
    '''

    
    process = subprocess.run(["python3 ../../maryam.py -e " + modulename + " " + cmd_command],
    shell=True,
    capture_output=True)
    
    stdout = process.stdout
    stderr = process.stderr
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    data = stdout + stderr

    print(data)
    return data
