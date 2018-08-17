import pymysql

class connectMysql(object):
    def __init__(self):
        self.db = pymysql.Connect("localhost", "root", "123456", "taobao", charset="utf8")
        self.cursor = self.db.cursor()

    def getConnect(self):
        return self.db, self.cursor

    def closeConnect(self):
        self.db.close()
