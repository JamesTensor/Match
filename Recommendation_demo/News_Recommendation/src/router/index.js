import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import home from '@/pages/Home'
import news from '@/pages/News'
import login from '@/pages/Login'

Vue.use(Router)
const router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home,
      meta: {
        needLogin: true
      }
    },
    {
      path: '/news',
      name: 'news',
      component: news,
      meta: {
        needLogin: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: login,
      meta: {
        needLogin: false
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.needLogin) {
    if (store.state.vuexlogin.isLogin || localStorage.getItem('username')) {
      next()
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    }
  } else {
    next()
  }
})

export default router
