#!/usr/bin/env python3
# coding=utf-8

import os
import sys
import string
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
client = TestlinkAPIClient("05742a441efd68af4062f2a7b12d7547")

def getAllTestCaseID(execution_type=2):  # execution_type 1:手动　2:自动
    args = {}
    allid = []
    args["testplanid"] = TESTPLANID
    plantestcases = client.getTestCaseForTestPlan(args)
    if 2 == execution_type:
        print('Auto test id:')
        printline()
    else:
        print('Manual test id:')
        printline()

    for k in sorted(plantestcases.keys()):
        if plantestcases[k][0]['execution_type'] == str(execution_type):
            allid.append(plantestcases[k][0]['tcase_id'])
            print(plantestcases[k][0]['tcase_id'] + " : " + str(plantestcases[k][0]['tcase_name']))

    printline()

    return allid

plancaseid = getAllTestCaseID()

ffile = open(idfilename, 'w')
try:
    str_id = ",".join(str(i) for i in plancaseid)
    print(str_id)
    ffile.write(str_id)
finally:
    ffile.close()
