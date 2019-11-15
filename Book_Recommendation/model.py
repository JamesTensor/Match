# -*- coding:utf-8 -*-

"""
    Author: Thinkgamer
    Desc: 训练模型
"""
import random
import pandas
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import mean_squared_error

class Model:
    def __init__(self):
        self.data = self._load_data()
        self.train_data, self.test_data = self._split_data()
        self.gbdt = self._train_model()

    # 加载数据
    def _load_data(self):
        if os.path.exists("./data/train.txt"):
            print("训练模型数据准备完毕,路径为：./data/train.txt")
            return
        else:
            tag_dict = dict()
            for line in open("./data/to_sql.txt","r",encoding="utf-8"):
                id,name,author,img,tag,price,pub_month,click,score,judge,rec_most,rec_more,rec_normal,\
                    rec_bad,rec_morebad,readed,reading,readup,mess= line.strip().split(",")
                tag_dict.setdefault(tag,{})
                tag_dict[tag][id] = {
                    "price":price,"pub_month":pub_month,"click": click,"score": score,"judge": judge,
                    "rec_most": rec_most,"rec_more": rec_more,"rec_normal": rec_normal,"rec_bad": rec_bad,
                    "rec_morebad": rec_morebad,"readed": readed,"reading": reading,"readup": readup
                }
            result = list()
            # 从每个标签中选择20条数据，构建训练模型的数据集
            for tag in tag_dict.keys():
                samples = random.sample(list(tag_dict[tag].values()), 20)
                for sample in samples:
                    label = random.randint(0,1)
                    features = ",".join(dict(sample).values())
                    result.append( str(label) + "," + features)

            # 将准备好的数据写入文件
            fw = open("./data/train.txt","a",encoding="utf-8")
            fw.write("label,price,pub_month,click,score,judge,rec_most,rec_more,rec_normal,rec_bad,rec_morebad,readed,reading,readup\n")
            fw.write("\n".join(result))
            fw.close()
            print("训练模型数据准备完毕,路径为：./data/train.txt")

    # 加载数据并拆分成训练集和测试集
    def _split_data(self):
        data = pandas.read_csv("./data/train.txt")
        train, test = train_test_split(data, test_size=0.3, random_state=40)
        return train, test

    # 训练模型
    def _train_model(self):
        lable = "label"
        x_columns = [x for x in self.train_data.columns if x not in [lable]]
        x_train = self.train_data[x_columns]
        y_train = self.train_data[lable]
        gbdt = GradientBoostingClassifier(learning_rate=0.05, n_estimators=70, max_depth=10)
        gbdt.fit(x_train, y_train)
        return gbdt

    # 测试模型
    def _evalute_model(self):
        lable = "label"
        x_columns = [x for x in self.test_data.columns if x not in [lable]]
        x_test = self.test_data[x_columns]
        y_test = self.test_data[lable]
        y_pred = self.gbdt.predict_proba(x_test)
        new_y_pred = list()
        for y in y_pred:
            # y[0] 表示样本label=0的概率 y[1]表示样本label=1的概率
            new_y_pred.append(1 if y[1] > 0.5 else 0)
        mse = mean_squared_error(y_test, new_y_pred)
        print("MSE: %.4f" % mse)
        accuracy = metrics.accuracy_score(y_test.values, new_y_pred)
        print("Accuracy : %.4g" % accuracy)
        auc = metrics.roc_auc_score(y_test.values, new_y_pred)
        print("AUC Score : %.4g" % auc)


if __name__ == "__main__":
    model = Model()
    model._evalute_model()
    # 保存模型
    # joblib.dump(model.gbdt, './model/gbdt.model')
    # 加载模型
    # joblib.load('./model/gbdt.model')