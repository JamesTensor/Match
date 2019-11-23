<template>
  <div class="recommonContain">
    <mheader :active="activenow" @onGetnews="switchtab"> </mheader>
    <div class="mainContent">
      <ul class="liscan">
        <li>
          <span>时间</span>
          <span>操作</span>
        </li>
        <li v-for="(item,index) in datas" :key="index">
          <span>{{item.time}}</span>
          <span>{{item.action}}<b v-if="item.object">【{{item.object}}】</b> </span>
        </li>
      </ul>
    </div>
    <div class="rightpag">
      <mpagnation v-if="total>display" :total="total" :current-page='current' :refresh='refresh' @pagechange="pagechange"></mpagnation>
    </div>
  </div>
</template>

<script>
import {getHistory} from '../assets/js/api'
import newheader from '../components/newHeader.vue'
import pagnation from '../components/pagnation'
export default {
  name: 'HelloWorld',
  data () {
    return {
      books: {},
      // 分页相关
      total: 0, // 总条数
      current: 1, // 当前激活页
      display: 30, // 每页显示多少条
      refresh: false, // 是否刷新（第一页激活）有搜索时需要
      page: '1',
      datas: '',
      activenow: '2'
    }
  },
  components: {
    'mheader': newheader,
    'mpagnation': pagnation
  },
  methods: {
    getBookdatas: function (option) {
      var getdata = {}
      if (!option.page) {
        getdata.page = '1'
      } else {
        getdata.page = option.page
      }
      getdata.username = this.$store.state.vuexlogin.userName
      getHistory(getdata).then((res) => {
        this.$layer.closeAll()
        if (!res.code) {
          this.$children[0].layout()
        } else {
          res.data.click.time = this.timeFormat(res.data.click.time)
          this.datas = res.data.click
        }
      }, (err) => {
        this.$layer.msg('小主稍等，紧急恢复中。。。')
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
      this.getBookdatas({'page': this.page})
    },
    // 切换
    switchtab: function (opt) {
      if (opt.url !== '/history') {
        this.$router.push({path: opt.url, query: {'username': this.$store.state.vuexlogin.userName}})
      }
    }
  },
  mounted () {
    this.getBookdatas({'page': '1'})
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
      .liscan{
        width: 100%;
        li{
          width: 100%;
          color: #666;
          font-size: 14px;
          display: block;
          margin:20px;
          span{
            display: inline-block;
            width: 40%;
          }
        }
        li:first-child{
          color: #000;
        }
      }
    }
    .rightpag{
      width: 70%;
    }
  }
</style>
