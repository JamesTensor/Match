# -*- coding: utf-8 -*-
"""
    Author: thinkgamer
    Desc:
        代码11-4 获取NewsRec/settings.py中配置的前端展示的标签下的新闻
"""

import pymysql
from NewsRec.settings import DB_HOST,DB_PORT,DB_USER,DB_PASSWD,DB_NAME,ALLOW_TAGS
import os

class NewsTagsCor:

    def __init__(self,file_path):
        self.kw_path = file_path
        self.db = self.connect()
        self.cursor = self.db.cursor()

        self.result = self.getNewsTags()

    # 连接mysql数据库
    def connect(self):
        db = pymysql.Connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT, charset='utf8')
        return db

    # 获取每个标签下对应的文章
    def getNewsTags(self):
        result = dict()
        for file in os.listdir(self.kw_path):
            path = self.kw_path + file
            for line in open(path, encoding= "utf-8").readlines():
                try:
                    newid, tags = line.strip().split("\t")
                except:
                    print("%s 下无对应标签" % newid)
                for tag in tags.split(","):
                    if tag in ALLOW_TAGS:
                        sql = "select new_hot from newhot where new_id=%s" % newid
                        self.cursor.execute(sql)
                        hot_value = self.cursor.fetchone()
                        result.setdefault(tag,{})
                        result[tag][newid]=hot_value[0]
        return result

    # 对每个标签下的新闻进行排序，并写入mysql
    def writeToMySQL(self):
        for tag in self.result.keys():
            for newid in self.result[tag].keys():
                sql_w = "insert into newtag( new_tag,new_id,new_hot ) values('%s', '%s' ,%s)" % (tag, newid, self.result[tag][newid])
                try:
                    self.cursor.execute(sql_w)
                    self.db.commit()
                except:
                    print("rollback", tag,newid,self.result[tag][newid])
                    self.db.rollback()

if __name__ == "__main__":
    print("开始寻找对应关键词下的新闻 ... ")
    keywords_path = "./../data/keywords/"
    ntc = NewsTagsCor(file_path=keywords_path)
    ntc.writeToMySQL()
    print("关键词下的新闻数据写入完毕, 表为：newsrec.newtag")