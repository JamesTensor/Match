# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from news.models import new,cate,newhot,newtag,newbrowse,newsim
from NewsRec.settings import ALLOW_USERS,ALLOW_TAGS

# 选择用户登录
@csrf_exempt
def login(request):
    if request.method == "GET":
        result = dict()
        result["users"]=ALLOW_USERS
        result["tags"]=ALLOW_TAGS
        return JsonResponse(result)
    elif request.method == "POST":
        # 从前端获取用户名 并写入 session
        uname = request.POST.get('username')
        request.session["username"]=uname
        # 前端将标签以逗号拼接的字符串形式返回
        tags= request.POST.get('tags')
        return JsonResponse({"username": uname, "tags": tags,"baseclick":0 , "code": 1})

# 主页
def home(request):
    # 从前端请求中获取cate
    _cate = request.GET.get("cateid")
    if "username" not in request.session.keys():
        return JsonResponse({ "code":0 })
    total = 0 # 总页数
    # 如果cate 是为你推荐，走该部分逻辑 tag_flag = 0 表示不是从标签召回数据
    if _cate == "1":
        news, news_hot_value = getRecNews(request)
    # 如果cate 是热度榜，走该部分逻辑
    elif _cate == "2":
        news,news_hot_value = getHotNews()
    # 其他正常的请求获取
    else:
        _page_id = int(request.GET.get("pageid"))
        news = new.objects.filter(new_cate=_cate).order_by("-new_time")
        total = news.__len__()
        news = news[_page_id * 10:(_page_id+1) * 10]
    # 数据拼接
    result = dict()
    result["code"] = 2
    result["total"] = total
    result["cate_id"] = _cate
    result["cate_name"] = str(cate.objects.get(cate_id=_cate))
    result["news"] = list()
    for one in news:
        result["news"].append({
            "new_id":one.new_id,
            "new_title":str(one.new_title),
            "new_time": one.new_time,
            "new_cate": one.new_cate.cate_name,
            "new_hot_value": news_hot_value[one.new_id] if _cate == "2" or _cate == "1" else 0 ,
            "new_content": str(one.new_content[:100])
        })
    return JsonResponse(result)

# 热度榜单的数据排序逻辑：new_seenum * 0.3 + new_disnum * 0.5 + (new_date-base_data) * 0.2
def getHotNews():
    # 从新闻热度表中取top 20新闻数据
    all_news = newhot.objects.order_by("-new_hot").values("new_id","new_hot")[:20]
    all_news_id = [one["new_id"] for one in all_news]
    all_news_hot_value = { one["new_id"]:one["new_hot"] for one in all_news}
    # 返回 热度榜单数据
    return new.objects.filter(new_id__in=all_news_id),all_news_hot_value

# 为你推荐的数据获取逻辑
def getRecNews(request):
    tags = request.GET.get('tags')
    baseclick = request.GET.get("baseclick")
    tag_flag = 0 if tags == "" else 1
    tags_list= tags.split(",")
    uname = request.session["username"]
    # 走标签召回逻辑
    if tag_flag == 1 and int(baseclick) == 0:
        num = (20 / len(tags_list)) + 1
        news_id_list = list()
        news_id_hot_dict = dict()
        for tag in tags_list:
            result = newtag.objects.filter(new_tag=tag).values("new_id","new_hot")[:num]
            for one in result:
                news_id_list.append(one["new_id"])
                news_id_hot_dict[one["new_id"]] = one["new_hot"]
        return new.objects.filter(new_id__in=news_id_list)[:20], news_id_hot_dict
    # 走正常排序逻辑
    elif tag_flag ==0:
        # 首先判断用户是否有浏览记录
        # 如果有该用户的浏览记录 则从浏览的新闻获取相似的新闻返回
        if newbrowse.objects.filter(user_name=uname).exists():
            # 判断用户最近浏览的新闻是否够10个，如果够的话 取 top 10，每个取两个相似
            # 如果不够10个 每个取 20/真实个数 +1 相似
            num = 0
            browse_dict = newbrowse.objects.filter(user_name=uname).order_by("-new_browse_time").values("new_id")[:10]
            if browse_dict.__len__() < 10:
                num = ( 20 / browse_dict.__len__()) +1
            else:
                num = 2
            news_id_list = list()
            all_news_hot_value = dict()
            # 遍历最近浏览的N篇新闻，每篇新闻取num篇相似新闻
            for browse_one in browse_dict:
                for one in newsim.objects.filter(new_id_base=browse_one["new_id"]).order_by("-new_correlation")[:num]:
                    news_id_list.append(one.new_id_sim)
                    all_news_hot_value[one.new_id_sim] = (newhot.objects.filter(new_id=browse_one["new_id"])[0]).new_hot
            return new.objects.filter(new_id__in=news_id_list)[:20], all_news_hot_value
        # 如果该用户没有浏览记录，即该用户是第一次进入系统且没有选择任何标签 返回热度榜单数据的20-40
        else:
            # 从新闻热度表中取top20 新闻数据
            all_news = newhot.objects.order_by("-new_hot").values("new_id", "new_hot")[20:40]
            all_news_id = [one["new_id"] for one in all_news]
            all_news_hot_value = {one["new_id"]: one["new_hot"] for one in all_news}
            print(all_news_hot_value)
            # 返回 热度榜单数据
            return new.objects.filter(new_id__in=all_news_id), all_news_hot_value


# 切换用户
def switchuser(request):
    if "username" in request.session.keys():
        uname = request.session["username"]
        # 删除新闻浏览表中的记录
        newbrowse.objects.filter(user_name=uname).delete()
        print("删除用户: %s 的新闻浏览记录 ..." % uname)
        # 删除session值
        del request.session["username"]
        print("用户: %s 执行了切换用户动作，删除其对应的session值 ..." % uname)
    return JsonResponse({"code":1})
    # return HttpResponseRedirect("/index/login/")
