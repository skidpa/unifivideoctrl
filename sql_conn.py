#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'pa'

import mysql.connector


class DbCtrl:
    def __init__(self):
        self.host = 'localhost'
        self.usr = ''
        self.passwd = '' # TODO: better and secure handlign of db password
        self.db = ''

    def dbconn(self):
        db = mysql.connector.connect(host=self.host,
                                     user=self.usr,
                                     passwd=self.passwd,
                                     db=self.db)

        return db

    def closedb(self, db):
        db.close()

    def tests(self):
        db = self.dbconn()

        cursor = db.cursor()
        cursor.execute("SELECT name,pass FROM usr")
        result = cursor.fetchall()
        for x in result:
            print x
        self.closedb(db)
