## 分享几个常用的召回推荐算法

1、Word2Vec计算物品相似度，我实际工作中也用它来计算两个菜肴之间的搭配度。

2、GNN作为一路召回。请关注我的另一个仓库：https://github.com/jiajiewang0326/KG_Based_Recommendation_with_GNNs

3、Userbased_CF

4、Itembased_CF。在很多推荐场景中，item数量远小于user数量，所以这个更适合，更高效。

5、热门召回。统计指定时间窗口的item的曝光量，点击量，从而计算CTR，按照CTR排序，选出topK个。因为这个代码涉及商业保密太多就不贴了。

6、基于地域、时间等推荐。我们做饮食推荐，而饮食习惯本身就有很强地域特点，而且蔬菜水果都是季节性的，此推荐模式在我们实际业务应用中反馈不错，获得了不错的收益。因为其中的规则都是企业资产就不贴了。

7、内容介绍、评论等文本内容挖掘作为一路召回。

8、基于标签的推荐

9、LFM



## 封装了几个常用推荐功能

Class_for_Recommendation





一部分数据集太大，可以自行下载：[http://grouplens.org/datasets/movielens/1m)](http://grouplens.org/datasets/movielens/1m)

说明：这个仓库里代码，都是我在快速试验效果阶段的产物，其中的方案后续经过多个大版本更新后应用或者被筛选淘汰，不涉商秘。
