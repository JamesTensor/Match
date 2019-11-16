# -*- coding:utf-8 -*-
"""
    Author: Thinkgamer
    Desc: 数据预处理
"""
import pandas
import re
import random

class Prepare:
    def __init__(self):
        self.file = "./data/豆瓣图书.xlsx"
        self.data = self._load_data()
        self.trans_data = self._transform()

    def _load_data(self):
        data = pandas.read_excel(self.file,sheet_name='Sheet1')
        return data

    def _transform(self):
        trans_data = dict()
        for row in self.data.iterrows():
            print(row[1]["ID"])
            trans_data[row[1]["ID"]] = list()
            trans_data[row[1]["ID"]].append(row[1]["标题"].replace(",","&"))

            author = "未定义" if row[1]["作者"]!=row[1]["作者"] else row[1]["作者"].replace("\n","").replace(" ","").replace(",","&")
            trans_data[row[1]["ID"]].append(author)

            img ="未定义" if row[1]["图片"] !=row[1]["图片"] else row[1]["图片"]
            trans_data[row[1]["ID"]].append(img)

            trans_data[row[1]["ID"]].append( row[1]["标签"])

            price = random.randint(20,50)+ random.randrange(1,10) /10 if row[1]["价格"]!=row[1]["价格"] else row[1]["价格"]
            trans_data[row[1]["ID"]].append( str(price) )

            publish_month = random.randint(1,15) if row[1]["距今出版月份"]!=row[1]["距今出版月份"] else row[1]["距今出版月份"]
            trans_data[row[1]["ID"]].append( str(publish_month))

            click_num = random.randint(1,100) if row[1]["点击次数"]!=row[1]["点击次数"] else row[1]["点击次数"]
            trans_data[row[1]["ID"]].append( str(click_num))


            socre = random.randint(1,9) + random.randrange(1,10) /10 if row[1]["评分"]!=row[1]["评分"] else row[1]["评分"]
            trans_data[row[1]["ID"]].append( str(socre))

            judge = 99 if row[1]["评价人数"] != row[1]["评价人数"] else row[1]["评价人数"]
            trans_data[row[1]["ID"]].append( str(judge))

            trans_data[row[1]["ID"]].append( str( random.randint(10,20) ))
            trans_data[row[1]["ID"]].append( str( random.randint(20,40) ))
            trans_data[row[1]["ID"]].append( str( random.randint(20,100) ))
            trans_data[row[1]["ID"]].append( str( random.randint(1,20) ))
            trans_data[row[1]["ID"]].append( str( random.randint(1,10) ))
            trans_data[row[1]["ID"]].append( str( random.randint(10,100) ))
            trans_data[row[1]["ID"]].append( str( random.randint(10,100) ))
            trans_data[row[1]["ID"]].append( str( random.randint(10,100) ))
            mess = re.sub("\n+","=",row[1]["出版信息"].replace(" ","").replace(",","&"))
            trans_data[row[1]["ID"]].append(mess)
        return trans_data

    def write_to_file(self):
        fw=open("./data/to_sql.txt","a",encoding="utf-8")
        for id in self.trans_data.keys():
            fw.write(str(id) + "," + ",".join(self.trans_data[id]) + "\n")
        fw.close()
        print("写入文件完成！")

if __name__ == "__main__":
    pre = Prepare()
    pre.write_to_file()