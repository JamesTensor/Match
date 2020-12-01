## 分享几个常用的召回推荐算法

1、Word2Vec计算物品相似度，我实际工作中也用它来计算两个菜肴之间的搭配度。

2、GNN，请关注我的另一个仓库：https://github.com/jiajiewang0326/KG_Based_Recommendation_with_GNNs

3、userbased_CF

4、itembased_CF

5、热门召回。统计指定时间窗口的item的曝光量，点击量，从而计算CTR，按照CTR排序，选出topK个。因为涉及商业保密就不贴代码了。

6、基于地域、时间等推荐。此方式在Boohee业务应用中反馈不错，获得了一些收益。因为其中的规则涉及商业保密就不贴代码了。

7、内容介绍、评论等文本主题提取作为一路召回。

8、基于标签的推荐

9、LFM



## 封装了几个常用推荐功能

Class_for_Recommendation





一部分数据集太大，可以自行下载：[http://grouplens.org/datasets/movielens/1m)](http://grouplens.org/datasets/movielens/1m)

