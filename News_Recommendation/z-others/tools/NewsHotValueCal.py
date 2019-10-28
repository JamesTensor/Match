# -*- coding: utf-8 -*-
"""
    Author: thinkgamer
    Desc：
        代码11-1 新闻的热度值计算，并写入数据库
"""
from datetime import datetime
import pymysql
from NewsRec.settings import DB_HOST,DB_PORT,DB_USER,DB_PASSWD,DB_NAME

class CalHotValue:
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.result = self.calHotValue()

    # 连接mysql数据库
    def connect(self):
        db = pymysql.Connect(DB_HOST,DB_USER,DB_PASSWD,DB_NAME,DB_PORT, charset='utf8')
        return db

    # 计算热度值
    def calHotValue(self):
        base_time = datetime.now()
        sql = "select new_id, new_cate_id, new_seenum, new_disnum, new_time from new"
        self.cursor.execute(sql)
        result_list = self.cursor.fetchall()
        result = list()

        for row in result_list:
            diff =  base_time - datetime.strptime(str(row[4].date()), '%Y-%m-%d')
            hot_value = row[2] * 0.4 + row[3] * 0.5 - diff.days * 0.1
            result.append((row[0],row[1],hot_value))
        print("新闻热度值计算完毕,返回结果 ...")
        return result

    # 将热度值写入数据库
    def writeToMySQL(self):
        for row in self.result:
            sql_w = "insert into newhot( new_id,new_cate_id,new_hot ) values(%s, %s ,%s)" % (row[0],row[1],row[2])
            try:
                self.cursor.execute(sql_w)
                self.db.commit()
            except:
                print("rollback",row)
                self.db.rollback()
        print("热度数据写入数据库：newsrec.newhot")

if __name__ == "__main__":
    print("开始计算新闻的热度值 ...")
    chv = CalHotValue()
    chv.writeToMySQL()

