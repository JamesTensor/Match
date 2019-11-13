

## 实现思路
- 基于GBDT模型的图书推荐（不同用户行为不同看到的为你推荐也不同，指定几个用户作为展示）
- 图书详情展示
- 我的足迹

## 后端依赖
- Python版本为3.6,安装依赖为 pip install -r requirement.txt

## 前端说明
- 依赖Node.js，版本为10.13

## 运行说明
- mysql新建bookrec数据库，将BookRecSys/BookRec/z-others/files/bookrec.sql 文件导入
- 修改 BookRecSys/BookRec/BookRec/settings.py 文件中的ALLOWED_HOSTS为本地IP地址和本地mysql配置信息
- 修改 BookRecSys/BookRec-Vue/config/index.js 中的 serverUrl
- 修改 BookRecSys/BookRec-Vue/src/assets/js/linkBase.js 中的 serverUrl
- 进入 BookRecSys/BookRec 执行python manage.py runserver 0.0.0.0:8000
- 进入 BookRecSys/BookRec-Vue 执行npm install /  npm run dev


-----
