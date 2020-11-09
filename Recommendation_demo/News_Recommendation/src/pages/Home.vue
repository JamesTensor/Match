<template>
  <div class="recommonContain">
    <new-header :active="isActive" @onGetnews="getCateNews"> </new-header>
    <div class="mainContent">
      <div class="mainLeft">
        <ul class="leftContent">
          <li class="animated slideInUp" style="animation-duration:1s;animation-delay:0s" v-for="item in newsData.news" :key="item.new_id" @click="newsDesc({'newid':item.new_id,'cateid':newsData.cate_id})">
            <h3 class="newsTitle">
              {{item.new_title}}
              <span class="newsOther">{{item.new_time}}</span>
              <span v-if="isActive==1" class="newsCate" >{{item.new_cate}}</span>
            </h3>
            <p class="newsContent">{{item.new_content}}</p>
          </li>
          <div  v-if="morebtn & isActive==1" class="moreBtn">
            <span @click="showMore">加载更多</span>
          </div>
          <li v-if="moRecommon" class="animated slideInUp" style="animation-duration:1s;animation-delay:0s" v-for="item in newsOtherdata.news" :key="item.new_id+10" @click="newsDesc({'newid':item.new_id,'cateid':newsData.cate_id})">
            <h3 class="newsTitle">
              {{item.new_title}}
              <span class="newsOther">{{item.new_time}}</span>
              <span class="newsCate" >{{item.new_cate}}</span>
            </h3>
            <p class="newsContent">{{item.new_content}}</p>
          </li>
        </ul>
        <new-pagnation v-if="total>10" :total="total" :current-page='current' :refresh='refresh' @pagechange="pagechange"></new-pagnation>

      </div>
      <div class="mainRight">
        <h3 class="hotTitle">{{hot_newsData.cate_name}}</h3>
        <ul class="rightContent">
          <li class="animated fadeInRight" style="animation-duration:1s;animation-delay:0s" v-for="item in hot_newsData.news" @click="newsDesc({'newid':item.new_id,'cateid':newsData.cate_id})" :key="item.new_id">
            <span>{{item.new_title}}</span>
            <i>{{item.new_time}}</i>
          </li>
        </ul>
      </div>
    </div>
   </div>
</template>

<script>
import {getCateNewsData} from '../assets/js/api'
import newheader from '../components/newHeader.vue'
import pagnation from '../components/pagnation'
export default {
  name: 'HelloWorld',
  data () {
    return {
      isActive: '1',
      newsData: {},
      hot_newsData: {},
      // 推荐加载更多
      newsOtherdata: {},
      moRecommon: false,
      morebtn: false,
      // 分页相关
      total: 0, // 总条数
      current: 1, // 当前激活页
      display: 10, // 每页显示多少条
      refresh: false // 是否刷新（第一页激活）有搜索时需要
    }
  },
  components: {
    'new-header': newheader,
    'new-pagnation': pagnation
  },
  methods: {
    getCateNews: function (option) {
      let cateId = option.cateid
      let getdata = {}
      if (cateId === '2') {
        this.loading('加载中。。。')
        getdata = {
          cateid: '2',
          userName: this.$store.state.vuexlogin.userName
        }
        getCateNewsData(getdata).then((res) => {
          if (!res.code) {
            this.$children[0].layout()
          } else {
            res.news.forEach((item) => {
              this.$layer.closeAll()
              item.new_time = this.timeFormat(item.new_time)
            })
            this.total = res.total
            this.hot_newsData = res
          }
        }, (err) => {
          this.$layer.msg('小主稍等，紧急恢复中。。。')
        })
      } else if (cateId === '1') {
        this.loading('加载中。。。')
        if (option.tags) {
          getdata.tags = option.tags
          getdata.baseclick = option.baseclick
        } else {
          getdata.tags = ''
          getdata.baseclick = option.baseclick
        }
        if (option.baseclick === '0') {
          getdata.baseclick = 0
        } else {
          getdata.baseclick = 1
        }
        getdata.cateid = '1'
        this.isActive = cateId
        getdata.userName = this.$store.state.vuexlogin.userName
        getCateNewsData(getdata).then((res) => {
          this.$layer.closeAll()
          if (!res.code) {
            this.$children[0].layout()
          } else {
            res.news.forEach((item) => {
              item.new_time = this.timeFormat(item.new_time)
            })
            this.total = res.total
            this.newsData = res
            if (res.news.length >= 10) {
              let arr1 = res.news.slice(0, 10)
              let arr2 = res.news.slice(11)
              this.newsData.news = arr1
              this.newsOtherdata.news = arr2
              this.morebtn = true
            } else {
              this.newsData = res
              this.newsOtherdata = {}
              this.morebtn = false
            }
          }
        }, (err) => {
          this.$layer.msg('小主稍等，紧急恢复中。。。')
        })
      } else {
        this.loading('加载中。。。')
        if (cateId) {
          getdata.cateid = cateId
          this.isActive = cateId
        }
        if (option.pageid) {
          getdata.pageid = option.pageid
        } else {
          getdata.pageid = 1
        }
        getdata.userName = this.$store.state.vuexlogin.userName
        getCateNewsData(getdata).then((res) => {
          this.$layer.closeAll()
          if (!res.code) {
            this.$children[0].layout()
          } else {
            res.news.forEach((item) => {
              item.new_time = this.timeFormat(item.new_time)
            })
            this.total = res.total
            this.newsData = res
          }
        }, (err) => {
          this.$layer.msg('小主稍等，紧急恢复中。。。')
        })
      }
    },
    newsDesc: function (opt) {
      this.$router.push({
        name: 'news',
        query: {cateid: opt.cateid, newid: opt.newid}
      })
    },
    // 分页
    pagechange: function (currentPage) {
      this.refresh = false
      this.page = currentPage
      // 滚到顶部 注意不在window而在document.documentElement
      document.documentElement.scrollTop = 0
      document.body.scrollTop = 0
      // 获取列表 可根据后端要求改变page的方式
      this.getCateNews({'pageid': this.page, 'cateid': this.isActive})
    },
    // 推荐更多
    showMore: function () {
      this.moRecommon = true
      this.morebtn = false
    }
  },
  mounted () {
    this.getCateNews({'cateid': '2'})
    var tags = this.$route.query.tags
    var baseclick = this.$route.query.baseclick + ''
    if (this.$route.params.cateid) {
      this.getCateNews({'cateid': this.$route.params.cateid})
    } else {
      this.getCateNews({'cateid': '1', 'tags': tags, 'baseclick': baseclick})
    }
  }
}
</script>
<style lang="less" scoped>
  @baseColor:#20a0ff;
  #ellies(@n){
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: @n;
    -webkit-box-orient: vertical;
  }
  .recommonContain{
    width: 100%;
    padding:2% 8%;
    padding-bottom: 0;
    box-sizing: border-box;
    .mainContent{
      width: 100%;
      display: flex;
      box-sizing: border-box;
      .mainLeft{
        width: 60%;
        box-sizing: border-box;
        .leftContent{
          li{
            width: 80%;
            margin:2% 5%;
            padding:1% 3%;
            border:1px solid #666;
            border-radius: 5px;
            box-shadow: 5px 5px 10px #999;
            cursor: pointer;
            .newsTitle{
              font-size: 16px;
              margin-bottom: 10px;
              color: #333;
              line-height: 20px;
              span{
                font-size: 12px;
              }
              .newsCate{
                display: inline-block;
                height: 50px;
                width: 50px;
                border: 1px solid #eee;
                float: right;
                overflow: hidden;
                word-break: break-all;
                font-size: 14px;
                border-radius: 50%;
                color: @baseColor;
                padding: 3px 10px;
                box-sizing: border-box;
                text-align: center;
                #ellies(2)
              }
            }
            .newsContent{
              font-size: 14px;
              line-height: 17px;
              color:#666;
              #ellies(2)
            }
            &:hover{
              padding:2% 3%;
            }
          }
          .moreBtn{
            text-align: center;
            margin:20px;
            span{
              display: inline-block;
              padding: 10px 25px;
              border: 1px solid #eee;
              border-radius: 10px;
              color: #777;
              &:hover{
                background: @baseColor;
                color: #fff;
              }
            }
          }
        }
      }
      .mainRight{
        flex: 1;
        &>h3{
          width:100%;
          padding: 10px;
          margin-top:15px;
          background: #dfdfdfdf;
          vertical-align: middle;
          box-sizing: border-box;
        }
        .hotTitle{
          font-size: 18px;
          padding: 5px;
          color: #333;
          margin-bottom: 10px;
        }
        .rightContent{
          padding: 5px;
          li{
            width: 100%;
            color: #666;
            height:16px;
            line-height: 16px;
            display: flex;
            margin-bottom: 10px;
            justify-content: space-around;
            cursor: pointer;
            font-size: 14px;
            span{
              #ellies(1);
              width: 70%;
            }
            i{
              font-size: 12px;
              #ellies(1);
              width: 30%;
            }
            &:hover{
              font-size: 15px;
              color:#000
            }
          }
        }
      }
    }
  }
</style>
