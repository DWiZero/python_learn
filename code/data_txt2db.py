import pymysql


class data_fashion2db(object):
    def __init__(self):
        self.db = pymysql.Connect("localhost", "root", "123456", "taobao", charset="utf8")
        self.cursor = self.db.cursor()

    def process_matchsets(self):
        with open('dim_fashion_matchsets（new).txt', 'r') as f:
            for line in f:
                itmes = line.split(' ')
                sql = "INSERT INTO fashion_matchsets(id,sets) VALUES (" + \
                      itmes[0] + ',"' + itmes[1] + '")'
                print(sql)
                self.cursor.execute(sql)
                # 执行sql语句
                self.db.commit()
        self.db.close()

    def process_item(self):
        with open('dim_items（new).txt', 'r') as f:
            for line in f:
                itmes = line.split(' ')
                sql = "INSERT INTO items(id,class,participle) VALUES (" + \
                      itmes[0] + ',' + itmes[1] + ',"' + itmes[2] + '")'
                print(sql)
                self.cursor.execute(sql)
                # 执行sql语句
                self.db.commit()
        self.db.close()

    def process_history(self):
        with open('user_bought_history.txt', 'r') as f:
            for line in f:
                itmes = line.split(' ')
                sql = "INSERT INTO bought_history(userId,itemId,date) VALUES (" + \
                      itmes[0] + ',' + itmes[1] + ',"' + itmes[2] + '")'
                print(sql)
                self.cursor.execute(sql)
                # 执行sql语句
                self.db.commit()
        self.db.close()


# if __name__ == '__main__':
#     df = data_fashion2db()
#     df.process_item()
