## 说明
	本项目为演示案例，采用前后端分离实现，后端使用的是Python的Django框架，前端使用的是Vue，数据库为MySQL

## 实现思路
- 各大主题下的热度排序
- 每篇新闻的关键词抽取和展示
- 基于item的推荐
- 热度榜（注意覆盖度）
- 为你推荐（不同用户行为不同看到的为你推荐也不同，指定几个用户作为展示）

## 后端依赖
- Python版本为3.6
- Python包和对应的版本在NewsRecSys/NewsRec/z-others/files/requirement.txt文件中
- 安装依赖为 pip install -r requirement.txt

## 前端说明
- 依赖Node.js，版本为10.13

## 运行说明
- mysql新建newsrec数据库，将NewsRecSys/NewsRec/z-others/files/newsrec.sql 文件导入
- 修改 NewsRecSys/NewsRec/NewsRec/settings.py 文件中的ALLOWED_HOSTS为本地IP地址和本地mysql配置信息
- 修改 NewsRecSys/NewsRec-Vue/config/index.js 中的 serverUrl
- 修改 NewsRecSys/NewsRec-Vue/src/assets/js/linkBase.js 中的 serverUrl
- 进入 NewsRecSys/NewsRec 执行python manage.py runserver 0.0.0.0:8000
- 进入 NewsRecSys/NewsRec-Vue 执行npm install /  npm run dev
- 浏览器输入 http://127.0.0.1:8001 访问

## 相关说明
- 后台访问地址：http://127.0.0.1:8000/admin/  (admin，admin)
- Navicat 破解版 （链接：https://pan.baidu.com/s/1dYtKQxnoSZywuRfgCOfPRQ  提取码：qw8k） 


-----
