import fetch from '../../axios/fetch'
// 主页分类数据
export const getCateNewsData = (getdata) => fetch('/api/index/home/', getdata, 'get')
// 主页分类
export const getCateData = () => fetch('/api/news/cates/', '', 'get')
// 获取新闻详情
export const getNewsData = (newsInfo) => fetch('/api/news/one/', newsInfo, 'get')
// 获取用户以及标签
export const getLogin = () => fetch('/api/index/login/', '', 'get')
// 登录
export const login = (loginInfo) => fetch('/api/index/login/', loginInfo, 'post')
// 退出切换用户
export const layout = () => fetch('/api/index/switchuser/', '', 'get')
