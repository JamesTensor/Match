import fetch from '../../axios/fetch'
// 获取用户以及标签
export const getLogin = () => fetch('/api/index/login/', '', 'get')
// 登录
export const login = (loginInfo) => fetch('/api/index/login/', loginInfo, 'post')
// 退出切换用户
export const layout = () => fetch('/api/index/switchuser/', '', 'get')
// 主页分类数据
export const getMainData = (getData) => fetch('/api/index/home/', getData, 'get')
// 主页分类详情
export const getOneData = (oneData) => fetch('/api/index/one/', oneData, 'get')
// 足迹
export const getHistory = (hisData) => fetch('/api/index/history/', hisData, 'get')
