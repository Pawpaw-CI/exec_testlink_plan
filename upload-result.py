#!/usr/bin/env python3
# coding=utf-8

import os
import sys
import xmlrpc.client

TESTPLANID = os.getenv("TESTPLAN_ID")
BUILDNAME  = os.getenv("BUILDNAME_VERSION")
SERVER_URL = os.getenv("SERVER_URL")
TESTLINKAPIKEY = os.getenv("TESTLINKAPIKEY")
if TESTPLANID == None or BUILDNAME == None:
    print("Please make sure you have export the TESTPLAN_ID")
    sys.exit(2)
else:
    print("TESTPLAN_ID : %s" % TESTPLANID)
    print('-' * 80)

resultname = "lava_result.txt"

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

    def reportToTestlink(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.reportTCResult(dictargs)

# substitute your Dev Key Here
client = TestlinkAPIClient(TESTLINKAPIKEY)

def getAllTestCaseID():
    args = {}
    allid = []
    args["testplanid"] = TESTPLANID
    plantestcases = client.getTestCaseForTestPlan(args)
    for k in sorted(plantestcases.keys()):
        allid.append(plantestcases[k][0]['tcase_id'])
        print(plantestcases[k][0]['tcase_id'] + " : " + str(plantestcases[k][0]['tcase_name']))

    print('-' * 80)

    return allid

def reportToTestlink(case_id, case_status, platform_id):
    args = {}
    args["testplanid"] = TESTPLANID
    args["testcaseid"] = case_id
    args["platformid"] = platform_id
    # args["buildname"] = "new version"
    args["buildname"] = BUILDNAME
    args["status"] = case_status
    result = client.reportToTestlink(args)
    print(result)

platform_docker_id = 1
platform_desktop_id = 2

ffile = open(resultname, 'r')
try:
    #result_content = ffile.read()
    while 1:
        line = ffile.readline()
        if not line:
            break
        tc_id, tc_result = line.split()
        print(tc_id + " : " + tc_result)
        reportToTestlink(int(tc_id), tc_result[0].lower(), platform_desktop_id)
finally:
    ffile.close()
