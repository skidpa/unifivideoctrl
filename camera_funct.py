#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'pa'
import requests
from texttable import Texttable
import json
from sql_conn import DbCtrl


class CameraCtrl:

    def __init__(self):
        self.nvrProtocol = 'https'
        self.nvrAddress = ''
        self.nvrPort = ''
        self.apiVersion = '/api/2.0/'
        self.nvrUserName = ''
        self.nvrPassword = ''
        self.apiLogin = ''
        self.apiLoginCreds = ''
        self.apiCamera = ''
        self.apiHeader = {'Content-Type': 'application/json'}
        self.cameras = ''
        self.MotionEnable = '", "recordingSettings": { "channel": "0", "fullTimeRecordEnabled": false, "motionRecordEnabled": true} '
        self.MotionDisable = '", "recordingSettings": { "channel": "0", "fullTimeRecordEnabled": false, "motionRecordEnabled": false}'
        self.enableRec = ''
        self.disableRec = ''
        self.setFullTime = {}
        self.loginReq = ''
        self.logoutReq = ''
        self.camerasToSave = []
        self.cameraList = []
        self.db_conn = DbCtrl()
        self.setCredentials()

    # function to load login credentials for unifi-video TODO: load from db
    def setCredentials(self):
        self.nvrUserName = ''
        self.nvrPassword = '!'

    # function to clear login credentials for unifi-video
    def clearCredentials(self):
        self.nvrUSerName = ''
        self.nvrPassword = ''

    # function that handles the login
    def nvrLogin(self):
        print 'nvrLogin'
        self.apiLoginCreds = '{"email": "' + self.nvrUserName + '", "password": "' + self.nvrPassword + '"}'
        self.loginReq = requests.post(self.nvrProtocol + '://' + self.nvrAddress + ':' + self.nvrPort
                                      + self.apiVersion + 'login',
                                      data=self.apiLoginCreds,
                                      headers=self.apiHeader,
                                      verify=False)


        if str(self.loginReq) == '<Response [200]>':
            print "Logged in..."
        else:
            print self.loginReq
            print self.loginReq.headers
            print self.loginReq.cookies
            print self.loginReq.text

    # function that get's a list of avaliable cameras and prints corresponding name and id on the screen
    def cameraGet(self):
        print 'camera list'
        self.cameras = requests.get(self.nvrProtocol + '://' + self.nvrAddress + ':' + self.nvrPort
                                      + self.apiVersion + 'camera',
                                      cookies=self.loginReq.cookies,
                                      headers=self.apiHeader,
                                      verify=False)

        if str(self.cameras) == '<Response [200]>':
            print "camera list:..."
            cameraJson = self.cameras.json()
            cameraJsonData = cameraJson['data']
            cameraJsonZones = cameraJsonData[0]

            # create tabular with the texttable package
            t = Texttable()
            t.header(['Camera Name', 'Camera ID'])
            t.set_chars(['-', '|', '-', '-'])
            # not tested with more than 1 camera probably fails due to cameraJsonZones set to [0]['zones']
            for item in cameraJsonZones:
                #print cameraJsonZones[item]
                if str(item) == '_id':
                    #print cameraJsonZones[item]
                    #t.add_row([item['name'], item['_id']])
                    t.add_row([cameraJsonZones['name'], cameraJsonZones['_id']])

            print t.draw()
            return cameraJsonZones
        else:
            print self.cameras
            print self.cameras.headers
            print self.cameras.cookies
            print self.cameras.text

    # function that enables recording for cameras in the camerList
    def cameraEnable(self):
        print 'camera enable'

        for camera in self.cameraList:
            if camera['zone'] == 'indoor':
                self.enableRec = '{ "name":"' + camera['name'] + self.MotionEnable + '}'
                sendEnableReq = requests.put(self.nvrProtocol + '://' + self.nvrAddress + ':' + self.nvrPort
                                             + self.apiVersion + 'camera/' + camera['_id'],
                                             cookies=self.loginReq.cookies, data=self.enableRec,
                                             headers=self.apiHeader, verify=False)
                print sendEnableReq

    # function that disables recording for cameras in the cameraList
    def cameraDisable(self):
        print 'camera disable'

        for camera in self.cameraList:
            if camera['zone'] == 'indoor':
                self.disableRec = '{ "name":"' + camera['name'] + self.MotionDisable + '}'
                sendDisableReq = requests.put(self.nvrProtocol + '://' + self.nvrAddress + ':' + self.nvrPort
                                             + self.apiVersion + 'camera/' + camera['_id'],
                                             cookies=self.loginReq.cookies, data=self.disableRec,
                                             headers=self.apiHeader, verify=False)
                print sendDisableReq

    # function that handles logout
    def nvrLogout(self):
        print 'nvrLogout'
        self.logoutReq = requests.get(self.nvrProtocol + '://' + self.nvrAddress + ':' + self.nvrPort
                                      + self.apiVersion + 'logout',
                                      cookies=self.loginReq.cookies,
                                      headers=self.apiHeader, verify=False)

        if str(self.loginReq) == '<Response [200]>':
            print "Logged Out..."
        else:
            print self.logoutReq
            print self.logoutReq.headers
            print self.logoutReq.cookies
            print self.logoutReq.text

    def jsontest(self):
        data = json.load(open('cameras.json'))

        for item in data:
            #print item['name']
            if item['zone'] == "indoor":
                print "inne"
                print item['name']
                print item['_id']

            if item =='zone1':
                print data[item][0]['name']
                print data[item][0]['_id']
                for j in item:
                    print j
                    print data[item]


    # The idea is that one loads all cameras with the list camera function in the gui and creates a dict and saves it
    # The saved file is then loaded on the server side each time the server starts this way n number of zones can be created
    # If a camera is to belong to multiple zones it should have multiple entries in the json file.
    # NOTE: this "zones" variable has nothing to do with the nvr! only so that we can arm/disarm ex indoor and outdoor
    # separately
    # this wont work since the idea got changed a bit. Code is still here awaiting re work
    def saveJson(self):
        data = [{'test':'test1','test2':'test2'}]
        #self.cameras = requests.get(self.nvrProtocol + '://' + self.nvrAddress + ':' + self.nvrPort
        #                            + self.apiVersion + 'camera',
        #                            cookies=self.loginReq.cookies,
        #                            headers=self.apiHeader,
        #                            verify=False)
        #cameraJsonZones = json.load(open('camerazones2.json')) # the dict that contains camers to save
        cameraJsonZones = self.cameraGet()
        print cameraJsonZones
        db = self.db_conn.dbconn()
        cursor = db.cursor()
        val = []

        #fetch cameras already in the db
        db_camera = "SELECT camera_id from cameras"
        cursor.execute(db_camera)
        result = cursor.fetchall()

        
        for item in cameraJsonZones:

            if str(item) == '_id':
                #print '_id: ', item['_id'], '\nname: ', item['name'], '\nzone: ' , usrzone
                #self.camerasToSave.extend([{"zone": usrzone, "name": item['name'], "_id": item['_id']}])

                print '_id: ', cameraJsonZones['_id'], '\nname: ', cameraJsonZones['name'], '\nzone: ', usrzone
                self.camerasToSave.extend([{"zone": usrzone, "name": cameraJsonZones['name'], "_id": cameraJsonZones['_id']}])

        with open('camerasTEst.json', 'w') as outfile:
            str_ = json.dumps(self.camerasToSave,
                              indent=2, sort_keys=False,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)

    # funktion for adding cameras to the database TODO: test with multiple cameras.
    def addCamera(self):

        cameraJsonZones = self.cameraGet()
        #print cameraJsonZones

        db = self.db_conn.dbconn()
        cursor = db.cursor()
        val = []

        # fetch cameras already in the db
        db_camera = "SELECT camera_id from cameras"
        cursor.execute(db_camera)
        result = cursor.fetchall()

        for item in cameraJsonZones:

            if str(item) == '_id':
                if any(cameraJsonZones['_id'] in s for s in result):
                    print 'camera {} with id {} is already added'.format(cameraJsonZones['name'],
                                                                         cameraJsonZones['_id'])
                else:
                    print 'camera {} with id {} can be added'.format(cameraJsonZones['name'], cameraJsonZones['_id'])
                    usrzone = raw_input('enter a zone for the camera: ')
                    camtoadd = (cameraJsonZones['name'], usrzone, cameraJsonZones['_id'])
                    val.append(camtoadd)

        print 'val: ', val
        print 'send to sql'
        sql = "INSERT INTO cameras (camera_name,camera_zone,camera_id) VALUES (%s,%s,%s)"
        cursor.executemany(sql, val)
        db.commit()
        print("affected rows = {}".format(cursor.rowcount))
        db.close()

    # function that will remove cameras from the database
    def removeCamera(self, camera_id):
        print "removeCamera"
        db = self.db_conn.dbconn()
        cursor = db.cursor()
        sql = "SELECT camera_name, camera_id from cameras WHERE camera_id='%s'" % camera_id
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            print 'Camera not in db.'
        else:
            rmcam = "DELETE FROM cameras WHERE camera_id='%s'" % camera_id
            cursor.execute(rmcam)
            db.commit()

        print result
        db.close()

    def loadCameras(self, zone):
        #self.cameraList = json.load(open('camerasTEst.json'))

        db = self.db_conn.dbconn()
        cursor = db.cursor()
        sql = "SELECT camera_name, camera_id, camera_zone from cameras WHERE camera_zone='%s'" % zone
        cursor.execute(sql)
        result = cursor.fetchall()
        print 'LoadCamera result: ', result

        if not result:
            print 'no cameras in zone'
        else:
            for cameras in result:
                self.cameraList.extend([{"zone": cameras[2], "name": cameras[0], "_id": cameras[1]}])

        print self.cameraList

    def clearCameras(self):
        self.cameraList = []
