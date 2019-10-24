<template>
  <div class="newsContent">
    <new-header @onGetnews="returnMain" :active="newCateId"></new-header>
    <div class="mainNews animated zoomIn" style="animation-duration:1s;animation-delay:0s">
      <h3 class="newsTitle">{{newDesc.new_title}}</h3>
      <span class="newsAttribute">
        <i>时间：{{newDesc.new_time}}</i>
        <i>类别：{{newDesc.new_cate}}</i>
        <i>浏览次数：{{newDesc.new_seenum}}</i>
        <i>评论次数：{{newDesc.new_disnum}}</i>
      </span>
      <div class="news" v-html="newDesc.new_content">
      </div>
    </div>
    <div class="mainRight animated fadeInRight" style="animation-duration:1s;animation-delay:0.5s">
      <h3 class="hotTitle">相似推荐</h3>
      <ul class="rightContent">
        <li v-for="item in newDesc.new_sim" @click="newsDesc({'newid':item.new_id,'cateid':item.new_cate})" :key="item.new_id">
          <span>{{item.new_title}}</span>
          <i>{{item.new_time}}</i>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import {getNewsData} from '../assets/js/api'
import newHeader from '../components/newHeader.vue'
export default {
  name: 'news',
  data () {
    return {
      newDesc: {},
      newCateId: ''
    }
  },
  components: {
    'new-header': newHeader
  },
  methods: {
    getNews: function (option) {
      this.loading('加载中。。。')
      option.userName = this.$store.state.vuexlogin.userName
      getNewsData(option).then((res) => {
        this.$layer.closeAll()
        if (!res.code) {
          this.$children[0].layout()
        } else {
          res.new_time = this.timeFormat(res.new_time)
          res.new_sim.forEach(item => {
            item.new_time = this.timeFormat(item.new_time)
          })
          res.new_content = this.returnline(res.new_content, '\\n', '</br>')
          this.newDesc = res
        }
      }, (err) => {
        this.$layer.msg(err)
      })
    },
    returnMain: function (option) {
      this.$router.push({name: 'home', params: option})
    },
    newsDesc: function (opt) {
      console.log(opt)
      this.$router.push({
        name: 'news',
        query: {cateid: opt.cateid, newid: opt.newid}
      })
      this.$router.go(0)
    }
  },
  mounted () {
    var newId = this.getUrlparams(window.location.href).newid
    this.newCateId = this.getUrlparams(window.location.href).cateid
    this.getNews({'newid': newId})
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
  .newsContent{
    width: 100%;
    box-sizing: border-box;
    padding: 2% 8%;
    overflow: auto;
    .mainNews{
      width: 70%;
      float: left;
      padding: 20px;
      box-sizing: border-box;
      padding-top: 0;
      .newsTitle{
        font-size: 34px;
        line-height: 36px;
        margin: 20px 0;
        font-weight: 600;
      }
      .newsAttribute{
        display: block;
        font-size: 12px;
        color:#999;
        height:18px;
        padding: 3px;
        i{
          display: inline-block;
          margin-left:25px;
          &:first-child{
            margin-left: 0;
          }
        }
      }
      .news{
        color: #666;
        font-size: 16px;
        line-height: 25px;
        text-space: 2px;
        padding:20px;
        box-sizing: border-box;
      }
    }
  .mainRight{
    width:30%;
    float:right;
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
        margin-bottom: 10px;
        cursor: pointer;
        font-size: 14px;
        span{
          display: block;
          #ellies(1);
          width: 90%;
          height:14px;
          margin-bottom: 3px;
        }
        i{
          display: block;
          font-size: 12px;
          #ellies(1);
          width: 50%;
          margin-left: 3px;
        }
        &:hover{
           font-size: 15px;
           color:#000
         }
      }
    }
  }
  }

</style>
