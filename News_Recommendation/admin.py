# -*-coding: utf-8 -*-
from django.contrib import admin
from news.models import new,cate,newsim,newhot,newtag,newbrowse

class adminNews(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("new_title", "new_id", "new_seenum", "new_time",'new_cate',)
    # 添加search bar，在指定的字段中search
    search_fields = ("new_title", "new_time",'new_cate',)
    # 页面右边会出现相应的过滤器选项
    list_filter = (  "new_time",'new_cate',)
    # 排序
    ordering = ("-new_time",)

admin.site.register(new, adminNews)

class adminCate(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("cate_id", "cate_name",)
    # 添加search bar，在指定的字段中search
    search_fields = ("cate_id", "cate_name",)
    # 页面右边会出现相应的过滤器选项
    list_filter = (  "cate_name",)

admin.site.register(cate, adminCate)

class adminNewSim(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("new_id_base", "new_id_sim","new_correlation",)
    # 添加search bar，在指定的字段中search
    search_fields = ("new_id_base", "new_id_sim","new_correlation",)
    # 页面右边会出现相应的过滤器选项
    # list_filter = ("cate_name",)

admin.site.register(newsim, adminNewSim)

class adminNewHot(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("new_id", "new_cate", "new_hot",)
    # 添加search bar，在指定的字段中search
    search_fields = ("new_id", "new_cate", "new_hot",)

admin.site.register(newhot, adminNewHot)

class adminNewTag(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ( "new_tag","new_id", "new_hot",)
    # 添加search bar，在指定的字段中search
    search_fields = ("new_tag","new_id", "new_hot",)

admin.site.register(newtag, adminNewTag)


class adminNewBrowse(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ( "user_name","new_id", "new_browse_time",)
    # 添加search bar，在指定的字段中search
    search_fields = ("user_name","new_id", "new_browse_time",)
    # 页面右边会出现相应的过滤器选项
    list_filter = ("user_name",)
admin.site.register(newbrowse, adminNewBrowse)

