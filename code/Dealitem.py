import myDBConnect
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


class itemDeal(object):

    def __init__(self):
        connect = myDBConnect.connectMysql()
        self.db, self.cursor = connect.getConnect()
        self.map = {}

    def getAllClass(self):
        # 查找所有的类目
        sql = 'select class from items group by class'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        # for item in result:
        #     print(item)

        # fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
        # fetchall(): 接收全部的返回结果行.
        # rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
        # self.getClassItems()

    def getClassItems(self, classId, fileName):
        # 查找指定类目的商品
        print("开始获取商品信息")
        sql1 = 'select id,participle from items where class =  "%s"'
        self.cursor.execute(sql1, classId)
        # item = self.cursor.fetchone()
        # print(item)
        items = self.cursor.fetchall()
        list = []
        itemsLen = len(items)
        print("开始处理商品为列表：商品个数：" + str(itemsLen))
        for item in items:
            list.append(item[1].replace('\n', ''))
        # vectorizer = CountVectorizer(analyzer=lambda x:x.split(','))
        # transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
        # tfidf = transformer.fit_transform(
        #     vectorizer.fit_transform(list))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
        # word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
        # weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        # for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        #     print("-------这里输出第", i, u"类文本的词语tf-idf权重------")
        #     for j in range(len(word)):
        #         print(word[j], weight[i][j])
        print("开始计算权重")
        tfidf2 = TfidfVectorizer(analyzer=lambda x: x.split(','))
        re = tfidf2.fit_transform(list)
        # print(type(np.where(re.data>0,1,0)))
        # re.data = np.where(re.data > 0, 1, 0)
        print(re.shape)
        # #打印出对应的分词的权重
        # feature_names = tfidf2.get_feature_names()
        # for reIndex,b in enumerate(re):
        #     # b = re[0]
        #     # print(re[0].shape)
        #     date = b.data
        #     # # 稀疏矩阵非0元素对应的列索引值所组成数组
        #     # print(b.indices)
        #     map = {}
        #     for index, i in enumerate(b.indices):
        #         map.setdefault(feature_names[i], date[index])
        #     # # 第一个元素0，之后每个元素表示稀疏矩阵中每行元素(非零元素)个数累计结果
        #     # print(b.indptr)
        #     print(str(items[reIndex][0])+":"+str(map))

        begin = -10000
        end = 0
        arrayList = []

        # 对大的矩阵进行切分
        while end != itemsLen:
            begin += 10000
            end += 10000
            if end >= itemsLen:
                end = itemsLen
            arrayList.append({"begin": begin, "end": end})
        # print(arrayList)

        # 矩阵进行交叉计算
        for i in arrayList:
            for j in arrayList:
                #两个矩阵之间的相似度
                similar = cosine_similarity(re[i["begin"]:i["end"]], re[j["begin"]:j["end"]])
                similar[similar < 0.6] = 0
                similar[similar >= 1] = 0
                a = sparse.csr_matrix(similar)
                self.iniMap(a, items[i["begin"]:i["end"]], items[j["begin"]:j["end"]])
        # print(len(self.map))
        self.writeFile(self.map.items(), fileName)

    # a:A,B矩阵的相似度的稀疏矩阵
    def iniMap(self, a, AItems, BItems):
        list = []
        for reIndex, b in enumerate(a):
            date = b.data
            list.clear()
            for index, i in enumerate(b.indices):
                similar = str(BItems[i][0]) + ":" + str(date[index])
                list.append(similar)
            # f.write(str(AItems[reIndex][0]) + ":" + str(list) + "\n")
            mist = self.map.get(str(AItems[reIndex][0]), []) + list
            self.map[str(AItems[reIndex][0])] = mist

    def writeFile(self, items, fileName):
        print("开始写入文件")
        # with open("284similar.txt", 'a') as f:
        with open(fileName, 'a') as f:
            for key, value in items:
                f.write(str(key) + ":" + str(value) + "\n")
        # 一类计算完成后，清空map
        self.map = {}


if __name__ == '__main__':
    it = itemDeal()
    classIds = it.getAllClass()
    for Id in classIds:
        it.getClassItems(Id, str(Id)+".txt")
