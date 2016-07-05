#!/usr/bin/env python3
# coding=utf-8

import os
import sys
import string
import xmlrpc.client

TESTPLANID = os.getenv("TESTPLAN_ID")
BUILDNAME  = os.getenv("BUILDNAME_VERSION")
if TESTPLANID == None or BUILDNAME == None:
    print("Please make sure you have export the TESTPLAN_ID")
    sys.exit(2)
else:
    print("TESTPLAN_ID : %s" % TESTPLANID)
    print('-' * 80)

resultname = "result.txt"

class TestlinkAPIClient:
    # substitute your server URL Here
    SERVER_URL = "https://testlink.deepin.io/lib/api/xmlrpc/v1/xmlrpc.php"

    def __init__(self, devKey):
        self.server = xmlrpc.client.ServerProxy(self.SERVER_URL)
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
client = TestlinkAPIClient("05742a441efd68af4062f2a7b12d7547")

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

def reportToTestlink(case_id, case_status):
    args = {}
    args["testplanid"] = TESTPLANID
    args["testcaseid"] = case_id
    # args["buildname"] = "new version"
    args["buildname"] = BUILDNAME
    args["status"] = case_status
    result = client.reportToTestlink(args)
    print(result)

ffile = open(resultname, 'r')
try:
    #result_content = ffile.read()
    while 1:
        line = ffile.readline()
        if not line:
            break
        tc_id, tc_result = line.split()
        print(tc_id + " : " + tc_result)
        reportToTestlink(int(tc_id), tc_result[0].lower())
finally:
    ffile.close()
    os.remove(resultname)
