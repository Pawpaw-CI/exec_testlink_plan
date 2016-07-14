#!/usr/bin/env python3
# coding=utf-8

import os
import json
import xmlrpc.client

TESTPLANID = os.getenv("TESTPLAN_ID")
BUILDID    = os.getenv("BUILD_ID")
SERVER_URL = os.getenv("SERVER_URL")
TESTLINKAPIKEY = os.getenv("TESTLINKAPIKEY")

def printline():
    print('-' * 80)

if TESTPLANID == None or SERVER_URL == None or TESTLINKAPIKEY == None:
    print("Please make sure you have export the parameters.")
    exit(1)
else:
    print("TESTPLAN_ID : %s\n" % TESTPLANID)
    print("BUILD_ID : %s\n" % BUILDID)
    printline()

idfilename = "id.txt"

class TestlinkAPIClient:
    def __init__(self, devKey):
        self.server = xmlrpc.client.ServerProxy(SERVER_URL)
        self.devKey = devKey

    def getInfo(self):
        return self.server.tl.about()

    def getProjects(self):
        return self.server.tl.getProjects(dict(devKey=self.devKey))

    def getPlaninfo(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.getTestPlanByName(dictargs)

    def getTestCaseForTestPlan(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.getTestCasesForTestPlan(dictargs)

    def getTestCaseIDByName(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.getTestCaseIDByName(dictargs)

    def createTestPlan(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.createTestPlan(dictargs)

    def addTestCaseToTestPlan(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.addTestCaseToTestPlan(dictargs)

# substitute your Dev Key Here
client = TestlinkAPIClient(TESTLINKAPIKEY)

platform_docker = '1'
platform_desktop = '2'

def getAllTestCaseID(execution_type=2):  # execution_type 1:手动　2:自动
    args = {}
    allid = {}
    docker_id = []
    lava_id = []
    args["testplanid"] = TESTPLANID
    plantestcases = client.getTestCaseForTestPlan(args)
    if 2 == execution_type:
        print('Auto test id:')
        printline()
    else:
        print('Manual test id:')
        printline()

    for k in sorted(plantestcases.keys()):
        if type(plantestcases[k]) == list:
            if plantestcases[k][0]['execution_type'] == str(execution_type) and plantestcases[k][0]["platform_id"] == platform_docker:
                docker_id.append(str(plantestcases[k][0]['tcase_id']))
                print(plantestcases[k][0]['tcase_id'] + " : " + str(plantestcases[k][0]['tcase_name']))

            if plantestcases[k][0]['execution_type'] == str(execution_type) and plantestcases[k][0]["platform_id"] == platform_desktop:
                lava_id.append(plantestcases[k][0]['tcase_id'])
                print(plantestcases[k][0]['tcase_id'] + " : " + str(plantestcases[k][0]['tcase_name']))

        if type(plantestcases[k]) == dict:
            if platform_docker in plantestcases[k].keys() and str(execution_type) == plantestcases[k][platform_docker]['execution_type']:
                docker_id.append(str(plantestcases[k][platform_docker]['tcase_id']))
                print(plantestcases[k][platform_docker]['tcase_id'] + " : " + str(plantestcases[k][platform_docker]['tcase_name']))

            if platform_desktop in plantestcases[k].keys() and str(execution_type) == plantestcases[k][platform_desktop]['execution_type']:
                lava_id.append(plantestcases[k][platform_desktop]['tcase_id'])
                print(plantestcases[k][platform_desktop]['tcase_id'] + " : " + str(plantestcases[k][platform_desktop]['tcase_name']))

    printline()
    print("docker_id "),
    print(docker_id)
    print("lava_id: ")
    print(lava_id)
    allid['docker_id'] = docker_id
    allid['lava_id'] = ",".join(str(i) for i in lava_id)

    return allid

caseid_dict = getAllTestCaseID()

ffile = open(idfilename, 'w')
try:
    print(caseid_dict)
    ffile.write(json.dumps(caseid_dict))
finally:
    ffile.close()
