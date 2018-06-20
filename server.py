#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'pa'

import socket
import threading
import camera_funct
import sql_conn

class Server:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.ip = 'localhost'
        self.port = 10000

        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        self.cam = camera_funct.CameraCtrl()
        self.db = sql_conn.DbCtrl()

    def getpass(self):
        db = self.db.dbconn()
        cursor = db.cursor()
        sql = "SELECT name, pass from usr"
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result


    def handler(self, client, address):

        while True:
            data = client.recv(1024)
            print data
            password = self.getpass()
            print password
            x = data.split(';')
            print "x: ", x
            #if x[0] == '1234': # TODO: insert pin-code from database
            if any(x[0] in s for s in password):
                print "hej"
                data = 'LOGIN OK'
                if x[1] == 'indoor' and x[2] == 'arm':
                    print 'call indoor arm funciton'
                    data = 'indoor;arm'
                    self.cam.nvrLogin()
                    self.cam.loadCameras(x[1])
                    self.cam.cameraEnable()
                    self.cam.nvrLogout()
                if x[1] == 'outdoor' and x[2] == 'arm':
                    print 'call outdoor arm funciton'
                    data = 'outdoor;arm'
                if x[1] == 'indoor' and x[2] == 'disarm':
                    print 'call indoor disarm funciton'
                    data = 'indoor;disarm'
                    self.cam.nvrLogin()
                    self.cam.loadCameras(x[1])
                    self.cam.cameraDisable()
                    self.cam.nvrLogout()
                if x[1] == 'outdoor' and x[2] == 'disarm':
                    print 'call outdoor disarm funciton'
                    data = 'outdoor;disarm'
                for clients in self.connections:
                    clients.send(data)
            if not data:
                print str(address[0]) + ':' + str(address[1]), 'disconnected'
                self.connections.remove(client)
                client.close()
                break

    def run(self):
        while True:
            client, address = self.sock.accept()
            clienThread = threading.Thread(target=self.handler,
                                           args=(client, address))
            clienThread.daemon = True
            clienThread.start()
            self.connections.append(client)
            print str(address[0]) + ':' + str(address[1]), 'connected'
            client.send("hejsan svejsan") #send connection message to newly connected client.


if __name__ == "__main__":
    server = Server()
    server.run()
