<template>
  <div class="recommonContain">
    <mheader :active="activenow" @onGetnews="switchtab"> </mheader>
    <div class="mainContent">
      <div class="Con bookCon">
        <h3>图书标签</h3>
        <ul class="lists">
          <li :class="tag == 'all' ? 'oktag' : ''" @click="getTagData('all')">推荐</li>
          <li :class="tag == item ? 'oktag' : ''" v-for="(item,index) in tags" :key="index" @click="getTagData(item)">{{item}}</li>
          <!--<li v-show="tags.length < 20" class="moretag" @click="getmoreTag()">更多 >></li>-->
        </ul>
        <hr style="border: 5px dotted #ddd"/>
        <div class="allsign">
          <ul class="relists">
            <li class="relist title">
              <p>封面图</p>
              <p class="rename">书名</p>
              <p class="recreater">作者</p>
              <p class="recreater">标签</p>
              <p class="recreater">评分</p>
              <p class="recreater">评价人数</p>
            </li>
            <li v-for="item in books" :key="item.id" class="relist" >
              <p><img :src='"../../static/img/"+item.id+".jpg"' @click="getOne($event,item.id)" class="bookimg" @error="imgError(item)"/></p>
              <p class="rename">{{item.name}}</p>
              <p class="recreater">{{item.author}}</p>
              <p class="recreater">{{item.tag}}</p>
              <p class="recreater">{{item.score}}</p>
              <p class="recreater">{{item.judge}}</p>
            </li>
            <li v-show="(books.length <= 20) && showmobook" class="more" @click="showmore()">更多 >></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="rightpag">
      <mpagnation v-if="total>display" :total="total" :current-page='current' :refresh='refresh' @pagechange="pagechange"></mpagnation>
    </div>
   </div>
</template>

<script>
import {getMainData, getOneData} from '../assets/js/api'
import newheader from '../components/newHeader.vue'
import pagnation from '../components/pagnation'
export default {
  name: 'HelloWorld',
  data () {
    return {
      books: {},
      // 歌单相关
      tags: [],
      // 分页相关
      total: 0, // 总条数
      current: 1, // 当前激活页
      display: 30, // 每页显示多少条
      refresh: false, // 是否刷新（第一页激活）有搜索时需要
      page: '1',
      tag: 'all',
      activenow: '1',
      tmpbook: {},
      showmobook: false
    }
  },
  components: {
    'mheader': newheader,
    'mpagnation': pagnation
  },
  methods: {
    // base64转换函数
    base64: function (img) {
      var canvas = document.createElement('canvas')
      canvas.width = img.width
      canvas.height = img.height
      var ctx = canvas.getContext('2d')
      ctx.drawImage(img, 0, 0, img.width, img.height)
      var ext = img.src.substring(img.src.lastIndexOf('.') + 1).toLowerCase()
      var dataURL = canvas.toDataURL('image/' + ext)
      return dataURL
    },
    getBookdatas: function (option) {
      var getdata = {}
      getdata.rec = option.tag
      if (!option.page) {
        getdata.page = '1'
      } else {
        getdata.page = option.page
      }
      console.log(option)
      getdata.username = this.$store.state.vuexlogin.userName
      getMainData(getdata).then((res) => {
        this.$layer.closeAll()
        if (!res.code) {
          this.$children[0].layout()
        } else {
          this.tags = res.data.tags
          if (getdata.rec === 'all') {
            this.total = 0
            this.tmpbook = res.data.books
            this.showmobook = true
            this.books = res.data.books.slice(0, 20)
          } else {
            this.showmobook = false
            this.books = res.data.books
            this.total = res.data.total
          }
        }
      }, (err) => {
        this.$layer.msg('小主稍等，紧急恢复中。。。')
      })
    },
    getOne: function (e, opt) {
      console.log()
      var onedata = {
        'id': opt
      }
      onedata.username = this.$store.state.vuexlogin.userName
      getOneData(onedata).then(res => {
        res.data.mess = this.returnline(res.data.mess, '=', '<br>')
        // var dataimg = e.target.getElementsByClassName('bookimg')[0].getAttribute('src')
		var dataimg = e.target.src
        this.$layer.open({
          content: '<div>' +
            '<div style="display: flex;justify-content: center">' +
            '<img style="width: 120px;height:180px;margin-right: 20px" src="' + dataimg + '"/>' +
            '<div style="color: #999;font-size: 12px;line-height: 18px;">' + res.data.mess + '</div>' +
            '</div>' +
            '<div style="display: flex;width:700px;flex-flow: column;margin-top:20px;color: #666;font-size: 14px">' +
            '<div style="line-height: 19px;">' +
            '<span style="display:inline-block;margin:5px"><b>书名：</b>' + res.data.name + '</span> |' +
            '<span style="display:inline-block;margin:5px"><b>标签：</b>' + res.data.tag + '</span> |' +
            '<span style="display:inline-block;margin:5px"><b>点击次数：</b>' + res.data.click + '</span> |' +
            '</div>' +
            '<div style="line-height: 19px;">' +
            '<span style="display:inline-block;margin:5px"><b>评分：</b>' + res.data.score + '</span> |' +
            '<span style="display:inline-block;margin:5px"><b>评价（人）：</b>' + res.data.judge + '</span> |' +
            '</div>' +
            '<div style="line-height: 19px;">' +
            '<span style="display:inline-block;margin:5px"><b>力荐（人）：</b>' + res.data.rec_most + '</span> |' +
            '<span style="display:inline-block;margin:5px"><b>推荐（人）：</b>' + res.data.rec_more + '</span> |' +
            '<span style="display:inline-block;margin:5px"><b>一般（人）：</b>' + res.data.rec_normal + '</span> |' +
            '</div>' +
            '<div style="line-height: 19px;">' +
            '<span style="display:inline-block;margin:5px"><b>不看好（人）：</b>' + res.data.rec_bad + '</span> |' +
            '<span style="display:inline-block;margin:5px"><b>极不看好（人）：</b>' + res.data.rec_morebad + '</span> |' +
            '</div>' +
            '<div style="line-height: 19px;">' +
            '<span style="display:inline-block;margin:5px"><b>读过（人）：</b>' + res.data.readed + '</span> |' +
            '<span style="display:inline-block;margin:5px"><b>正在阅读（人）：</b>' + res.data.reading + '</span> |' +
            '<span style="display:inline-block;margin:5px"><b>想读（人）：</b>' + res.data.readup + '</span>' +
            '</div>' +
            '</div>' +
            '</div>',
          title: '',
          btn: ['了解']
        })
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
      this.getBookdatas({'page': this.page, 'tag': this.tag})
    },
    // tag获取
    getTagData: function (nowtag) {
      // this.tags = this.tags.slice(0, 15)
      this.refresh = true
      this.tag = nowtag
      if (nowtag.indexOf('+') > -1) {
        var tmptag = nowtag.split('+')
        this.tag = tmptag[0]
        this.isActive = tmptag[1]
      }
      this.getBookdatas({'tag': this.tag})
    },
    // 切换
    switchtab: function (opt) {
      if (opt.url !== '/') {
        this.$router.push({path: opt.url, query: {'username': this.$store.state.vuexlogin.userName}})
      }
    },
    // showmore
    showmore: function () {
      this.books = this.tmpbook
      this.showmobook = false
    },
    // err img
    imgError (item) {
      item.img = require('../assets/img/book.jpg')
    }
  },
  mounted () {
    this.getBookdatas({'tag': 'all'})
  }
}
</script>
<style lang="less" scoped>
  @baseColor:#20a0ff;
  #ellies(@n){
    overflow: hidden;
    text-overflow: ellipsis;
    -webkit-line-clamp: @n;
    -webkit-box-orient: vertical;
    white-space: nowrap;
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
      justify-content: space-around;
      .Con{
        box-sizing: border-box;
        padding:10px;
        border:1px solid #ddd;
        box-shadow: 0 0 5px 5px #eee;
        min-height: 500px;
        margin-top:15px;
        margin-bottom: 15px;
        .lists{
          margin-top:10px;
          li{
            display: inline-block;
            border: 1px solid #ddd;
            box-sizing: border-box;
            padding: 6px;
            border-radius: 4px;
            margin:5px;
            text-align: center;
            cursor: pointer;
            font-size: 12px;
            &:hover{
              color: @baseColor;
              border: 1px solid @baseColor;
            }
          }
          .oktag{
            color: @baseColor;
            border: 1px solid @baseColor;
          }
          .moretag{
            color: orange;
            border: 1px solid orange;
          }
        }
        .relists{
          margin-top:20px;
          display: flex;
          justify-content: space-around;
          flex-flow: column;
          .more{
            margin:auto;
            padding: 5px;
            border:1px solid orange;
            color:#fff;
            background: orange;
            text-align: center;
            width: 150px;
            border-radius: 3px;
            height: 30px;
            line-height: 30px;
            margin-top:15px;
            cursor: pointer;
          }
          .relist{
            width: 100%;
            box-sizing: border-box;
            padding: 5px;
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: space-around;
            box-shadow: 0 0 1px 2px #ddd;
            /*&:hover{
              color: @baseColor;
              box-shadow: 0 0 20px 5px #ddd;
            }*/
			.bookimg:hover{
            cursor: pointer;
			  box-shadow: 0 0 20px 5px #ddd;
			}
            .recreater{
              font-size: 12px;
              color: #666;
              line-height: 14px;
              margin-bottom: 5px;
              margin-top: 5px;
              #ellies(1)
            }
            .rename{
              font-size: 14px;
              line-height: 16px;
              #ellies(1)
            }
            img{
              width: 100px;
              height:120px;
              border-radius: 5px;
            }
            p{
              width: 20%;
              box-sizing: border-box;
            }
            p:nth-child(1){
              padding-left: 20px;
            }
            p:nth-child(4),p:nth-child(5),p:nth-child(6){
              width: 13%;
            }
          }
          .title{
            box-shadow: none;
            margin-bottom: 30px;
            &:hover{
              box-shadow: none;
              color: #666;
              cursor: auto;
            }
          }
          .onelist{
            width: 100%;
            color:#666;
            margin:5px 0;
            display: flex;
            justify-content: space-between;
            cursor: pointer;
            &:hover{
              color:@baseColor;
            }
            .onetime,.onename{
              #ellies(1);
              display: inline-block;
              box-sizing: border-box;
              padding: 0 10px;
            }
          }
        }
      }
      .bookCon{
        flex: 2;
        margin-right: 15px;
      }
      .Con{
        flex: 1;
        margin-left: 15px;
        min-width: 30%;
      }
    }
    .rightpag{
      width: 100%;
    }
  }
</style>
