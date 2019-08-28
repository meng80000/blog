from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from io import BytesIO
from utils.random_check_code import rd_check_code
from utils.pager import PageInfo
import os
from app01.forms import RegisterForm,LoginForm,ArticleForm,CommentForm
from django.db.models import Count,F
from django.db import transaction #事件，回滚
import json

def check_code(request):
    """
    验证码生成
    :param request:
    :return:
    """
    img,code=rd_check_code()
    stream=BytesIO()
    img.save(stream,"png")
    request.session["code"]=code
    return HttpResponse(stream.getvalue())

def login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method=="GET":
        obj=LoginForm()
        return render(request,"login.html",{"obj":obj})
    else:
        obj=LoginForm(request.POST)
        input_code=request.POST.get("code")
        session_code=request.session.get("code")
        if input_code.upper()==session_code.upper():
            if obj.is_valid():
                row=models.UserInfo.objects.filter(username=obj.cleaned_data["username"],password=obj.cleaned_data["password"]).first()
                if row:
                    request.session["username"]=obj.cleaned_data["username"]
                    request.session["password"]=obj.cleaned_data["password"]
                    request.session["id"]=row.nid
                    print(row.nid)
                    print(request.session.get("id"))
                    print(request.session)
                    return redirect("/home/")
                else:
                    # pass
                    return render(request,"login.html",{"obj":obj,"error_msg":"用户名或者密码错误"})
        else:
            return render(request,"login.html",{"obj":obj,"code_error":"验证码错误"})

def logout(request,**kwargs):
    """
    用户注销
    :param request:
    :return:
    """
    blog_name=kwargs.get("blog_name")
    site=kwargs.get("site")
    art=kwargs.get("art")
    if str(request.path_info)=="/logout/":
        session_key = request.session.session_key
        request.session.delete(session_key)
        return redirect("/")
    elif str(request.path_info)=="/"+str(site)+"/s/article="+str(art)+"/":
        session_key = request.session.session_key
        request.session.delete(session_key)
        return redirect("/"+str(site)+"/article="+str(art)+"/")
    else:
        session_key = request.session.session_key
        request.session.delete(session_key)
        return redirect("/blog/"+str(blog_name)+"/")

def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method=="GET":
        obj=RegisterForm(request)
        return render(request,"register.html",{"obj":obj})
    else:
        obj = RegisterForm(request,data=request.POST,files=request.FILES)
        print(obj.is_valid())
        if obj.is_valid():
            file_obj = request.FILES.get("avatar")
            file_path = os.path.join("static", file_obj.name)
            print(file_path)
            with open(file_path, "wb")as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            print(obj.cleaned_data)
            models.UserInfo.objects.create(
                username=obj.cleaned_data["username"],
                password=obj.cleaned_data["password"],
                nickname=obj.cleaned_data["nickname"],
                email=obj.cleaned_data["email"],
                avatar="/"+file_path,
            )
            return redirect("/login/")
        else:
            return render(request,"register.html",{"obj":obj,"msg":"恭喜你注册成功"})

def home(request,*args,**kwargs):
    """
    网站主页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    # print(kwargs)
    condition={}
    type_id=int(kwargs.get("type_id")) if kwargs.get("type_id") else None
    if type_id:
        condition["article_type_id"]=type_id
    article_list=models.Article.objects.filter(**condition)
    type_choice_list=models.Article.type_choices
    all_count=models.Article.objects.all().count()
    page_info=PageInfo(request.GET.get("page"),all_count,5,"/home/",11)
    articles=article_list[page_info.start():page_info.end()]
    if request.session.get("username"):
        username=request.session["username"]
        obj = models.UserInfo.objects.filter(username=username).first()
        return render(request,
                      "home.html",
                      {"type_choice_list":type_choice_list,
                          "articles":articles,
                          "type_id":type_id,
                          "obj":obj,
                          "page_info":page_info,
                       }
                      )
    else:
        return render(request,
                      "home.html",
                      {"type_choice_list": type_choice_list,
                       "articles": articles,
                       "type_id": type_id,
                       "page_info": page_info,
                       }
                      )

def blog(request,*args,**kwargs):
    """
    个人主页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    blog_site=kwargs.get("site")#当前用户的博客后缀
    blog=models.Blog.objects.filter(site=blog_site).first()#当前博客对象
    obj=blog.user#当前博客用户对象
    article_list=models.Article.objects.filter(blog_id=blog.nid).all()#当前用户的所有文章
    #---------------------分页
    all_count=article_list.count()
    page_info=PageInfo(request.GET.get("page"),all_count,5,"/blog/"+blog_site+"/",11)
    articles=article_list[page_info.start():page_info.end()]
    #---------------------分页
    followers=models.UserFans.objects.filter(user_id=obj.nid).count()#粉丝数量
    users=models.UserFans.objects.filter(follower_id=obj.nid).count()#关注数量

    # tag_list=models.Article2Tag.objects.filter(tag__blog=blog).values("tag_id","tag__title").annotate(c=Count("id"))
    # print(tag_list)#标签名字和统计数量列表--方法一
    tag_list=models.Article.objects.filter(blog=blog).values("tags__nid","tags__title").annotate(c=Count("nid"))
    # print(tag_list)#标签名字和统计数量列表--方法二
    category_list=models.Article.objects.filter(blog_id=blog.nid).values("category_id","category__title",).annotate(c=Count("nid"))
    # print(category_list)#分类名字和统计数量列表
    # date_list=models.Article.objects.filter(blog=blog).extra(select={"c":"data_format(create_time,'%%Y-%%m')"}).values("c").annotate(ct=Count("nid"))
    date_list=models.Article.objects.filter(blog=blog).extra(select={"c":"strftime('%%Y-%%m',create_time)"}).values("c").annotate(ct=Count("nid"))
    # print(date_list)#时间分类
    if request.session.get("username"):
        current_name=request.session.get("username")
        current_obj = models.UserInfo.objects.filter(username=current_name).first()
        return render(request,
                      "blog.html",
                      {
                          "articles":articles,
                          "obj":obj,
                          "current_obj":current_obj,
                          "page_info":page_info,
                          "followers":followers,
                          "users":users,
                          "tag_list":tag_list,
                          "category_list":category_list,
                          "date_list":date_list,
                       }
                      )
    else:
        return render(request,
                      "blog.html",
                      {
                          "articles":articles,
                          "obj":obj,
                          "current_obj":None,
                          "page_info":page_info,
                          "followers":followers,
                          "users":users,
                          "tag_list":tag_list,
                          "category_list":category_list,
                          "date_list":date_list,
                       }
                      )

def tag(request, *args, **kwargs):
    """
    个人文章标签页面
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    # print(kwargs)

    blog_site=kwargs.get("site")#当前用户的博客后缀
    tag_id=kwargs.get("tag_id")
    blog=models.Blog.objects.filter(site=blog_site).first()#当前博客对象
    obj=blog.user#当前博客用户对象
    article_tag_list=models.Article.objects.filter(tags__nid=tag_id,blog=blog).all()#当前用户的所有文章

    #---------------------分页
    all_count=article_tag_list.count()
    page_info=PageInfo(request.GET.get("page"),all_count,5,"/blog/"+blog_site+"/",11)
    articles=article_tag_list[page_info.start():page_info.end()]
    #---------------------分页
    followers=models.UserFans.objects.filter(user_id=obj.nid).count()#粉丝数量
    users=models.UserFans.objects.filter(follower_id=obj.nid).count()#关注数量

    # tag_list=models.Article2Tag.objects.filter(tag__blog=blog).values("tag_id","tag__title").annotate(c=Count("id"))
    # print(tag_list)#标签名字和统计数量列表--方法一
    tag_list=models.Article.objects.filter(blog=blog).values("tags__nid","tags__title").annotate(c=Count("nid"))
    # print(tag_list)#标签名字和统计数量列表--方法二
    category_list=models.Article.objects.filter(blog_id=blog.nid).values("category_id","category__title",).annotate(c=Count("nid"))
    # print(category_list)#分类名字和统计数量列表
    # date_list=models.Article.objects.filter(blog=blog).extra(select={"c":"data_format(create_time,'%%Y-%%m')"}).values("c").annotate(ct=Count("nid"))
    date_list=models.Article.objects.filter(blog=blog).extra(select={"c":"strftime('%%Y-%%m',create_time)"}).values("c").annotate(ct=Count("nid"))
    # print(date_list)#时间分类
    if request.session.get("username"):
        current_name=request.session.get("username")
        current_obj = models.UserInfo.objects.filter(username=current_name).first()
        return render(request,
                      "tag.html",
                      {
                          "articles":articles,
                          "obj":obj,
                          "current_obj":current_obj,
                          "page_info":page_info,
                          "followers":followers,
                          "users":users,
                          "tag_list":tag_list,
                          "category_list":category_list,
                          "date_list":date_list,
                       }
                      )
    else:
        return render(request,
                      "tag.html",
                      {
                          "articles":articles,
                          "obj":obj,
                          "current_obj":None,
                          "page_info":page_info,
                          "followers":followers,
                          "users":users,
                          "tag_list":tag_list,
                          "category_list":category_list,
                          "date_list":date_list,
                       }
                      )

def category(request, *args, **kwargs):
    """
    个人文章分类页面
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    # print(kwargs)

    blog_site = kwargs.get("site")  # 当前用户的博客后缀
    category_id = kwargs.get("category_id")
    blog = models.Blog.objects.filter(site=blog_site).first()  # 当前博客对象
    obj = blog.user  # 当前博客用户对象
    article_tag_list = models.Article.objects.filter(category_id=category_id, blog=blog).all()  # 当前用户的所有文章

    # ---------------------分页
    all_count = article_tag_list.count()
    page_info = PageInfo(request.GET.get("page"), all_count, 5, "/myblog/" + blog_site + "/", 11)
    articles = article_tag_list[page_info.start():page_info.end()]
    # ---------------------分页
    followers = models.UserFans.objects.filter(user_id=obj.nid).count()  # 粉丝数量
    users = models.UserFans.objects.filter(follower_id=obj.nid).count()  # 关注数量

    # tag_list=models.Article2Tag.objects.filter(tag__blog=blog).values("tag_id","tag__title").annotate(c=Count("id"))
    # print(tag_list)#标签名字和统计数量列表--方法一
    tag_list = models.Article.objects.filter(blog=blog).values("tags__nid", "tags__title").annotate(c=Count("nid"))
    # print(tag_list)#标签名字和统计数量列表--方法二
    category_list = models.Article.objects.filter(blog_id=blog.nid).values("category_id",
                                                                           "category__title", ).annotate(
        c=Count("nid"))
    # print(category_list)#分类名字和统计数量列表
    # date_list=models.Article.objects.filter(blog=blog).extra(select={"c":"data_format(create_time,'%%Y-%%m')"}).values("c").annotate(ct=Count("nid"))
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={"c": "strftime('%%Y-%%m',create_time)"}).values("c").annotate(ct=Count("nid"))
    # print(date_list)#时间分类
    if request.session.get("username"):
        current_name=request.session.get("username")
        current_obj = models.UserInfo.objects.filter(username=current_name).first()
        return render(request,
                      "category.html",
                      {
                          "articles": articles,
                          "obj": obj,
                          "current_obj": current_obj,
                          "page_info": page_info,
                          "followers": followers,
                          "users": users,
                          "tag_list": tag_list,
                          "category_list": category_list,
                          "date_list": date_list,
                      }
                      )
    else:
        return render(request,
                      "category.html",
                      {
                          "articles": articles,
                          "obj": obj,
                          "current_obj": None,
                          "page_info": page_info,
                          "followers": followers,
                          "users": users,
                          "tag_list": tag_list,
                          "category_list": category_list,
                          "date_list": date_list,
                      }
                      )

def date_time(request, *args, **kwargs):
    """
    个人文章分类页面
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    # return HttpResponse(11111111111)
    blog_site = kwargs.get("site")  # 当前用户的博客后缀
    date_time = kwargs.get("date_time")
    blog = models.Blog.objects.filter(site=blog_site).first()  # 当前博客对象
    obj = blog.user  # 当前博客用户对象
    date_list = models.Article.objects.filter(blog=blog).extra(select={"c": "select strftime('%%Y-%%m',create_time) from app01_article where strftime('%%Y-%%m',create_time)=%s"},select_params=date_time)
    # ---------------------分页
    all_count = date_list.count()
    page_info = PageInfo(request.GET.get("page"), all_count, 5, "/"+blog_site+"/date_time="+date_time+"/", 11)
    articles = date_list[page_info.start():page_info.end()]
    # ---------------------分页
    followers = models.UserFans.objects.filter(user_id=obj.nid).count()  # 粉丝数量
    users = models.UserFans.objects.filter(follower_id=obj.nid).count()  # 关注数量

    # tag_list=models.Article2Tag.objects.filter(tag__blog=blog).values("tag_id","tag__title").annotate(c=Count("id"))
    # print(tag_list)#标签名字和统计数量列表--方法一
    tag_list = models.Article.objects.filter(blog=blog).values("tags__nid", "tags__title").annotate(c=Count("nid"))
    # print(tag_list)#标签名字和统计数量列表--方法二
    category_list = models.Article.objects.filter(blog_id=blog.nid).values("category_id","category__title", ).annotate(c=Count("nid"))
    # print(category_list)#分类名字和统计数量列表
    date_list = models.Article.objects.filter(blog=blog).extra(select={"c": "strftime('%%Y-%%m',create_time)"}).values("c").annotate(ct=Count("nid"))
    # print(date_list)#时间分类
    if request.session.get("username"):
        current_name=request.session.get("username")
        current_obj = models.UserInfo.objects.filter(username=current_name).first()
        return render(request,
                      "datatime.html",
                      {
                          "articles": articles,
                          "obj": obj,
                          "current_obj": current_obj,
                          "page_info": page_info,
                          "followers": followers,
                          "users": users,
                          "tag_list": tag_list,
                          "category_list": category_list,
                          "date_list": date_list,
                      }
                      )
    else:
        return render(request,
                      "datatime.html",
                      {
                          "articles": articles,
                          "obj": obj,
                          "current_obj": None,
                          "page_info": page_info,
                          "followers": followers,
                          "users": users,
                          "tag_list": tag_list,
                          "category_list": category_list,
                          "date_list": date_list,
                      }
                      )

def arts(request, *args, **kwargs):
    """
    文章详细页
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    blog_site = kwargs.get("site")  # 当前用户的博客后缀
    article_nid=kwargs.get("art")#点击的文章id
    blog = models.Blog.objects.filter(site=blog_site).first()  # 当前博客对象
    obj = blog.user  # 当前博客用户对象
    article_detail=models.ArticleDetail.objects.filter(article_id=article_nid).first()#查看的文章详细内容
    followers = models.UserFans.objects.filter(user_id=obj.nid).count()  # 粉丝数量
    users = models.UserFans.objects.filter(follower_id=obj.nid).count()  # 关注数量
    up_num=models.UpDown.objects.filter(article_id=article_nid,up_down=1).count()#文章点赞数
    down_num=models.UpDown.objects.filter(article_id=article_nid,up_down=0).count()#文章点踩数
    # tag_list=models.Article2Tag.objects.filter(tag__blog=blog).values("tag_id","tag__title").annotate(c=Count("id"))
    # print(tag_list)#标签名字和统计数量列表--方法一
    tag_list = models.Article.objects.filter(blog=blog).values("tags__nid", "tags__title").annotate(c=Count("nid"))
    # print(tag_list)#标签名字和统计数量列表--方法二
    category_list = models.Article.objects.filter(blog_id=blog.nid).values("category_id","category__title", ).annotate(c=Count("nid"))
    # print(category_list)#分类名字和统计数量列表
    # date_list=models.Article.objects.filter(blog=blog).extra(select={"c":"data_format(create_time,'%%Y-%%m')"}).values("c").annotate(ct=Count("nid"))
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={"c": "strftime('%%Y-%%m',create_time)"}).values("c").annotate(ct=Count("nid"))
    # print(date_list)#时间分类
    ##############################评论#################################
    msg_list=[]
    comment_obj = models.Comment.objects.filter(article_id=article_nid).values("nid", "content", "reply_id", "user__blog__site","user__nid", "user__nickname")
    for i in comment_obj:
        msg_list.append(i)
    msg_list_dict = {}
    result = []
    for i in msg_list:
        i["child"] = []
        msg_list_dict[i["nid"]] = i
    for i in msg_list:
        pid = i["reply_id"]
        if pid:
            msg_list_dict[pid]["child"].append(i)
        else:
            result.append(i)
    from utils.comment import comment_tree
    comment_str=comment_tree(result)
    if request.session.get("username"):
        if request.method == "GET":
            comment=CommentForm()
            current_name=request.session.get("username")
            current_obj = models.UserInfo.objects.filter(username=current_name).first()
            if current_name != obj.username:
                up_down_msg = models.UpDown.objects.filter(user_id=current_obj.nid,article_id=article_nid).first()
            else:
                up_down_msg=None
            return render(request,
                          "arts.html",
                          {
                              "article_detail": article_detail,
                              "obj": obj,
                              "comment": comment,
                              "up_down_msg": up_down_msg,
                              "up_num": up_num,
                              "down_num": down_num,
                              "current_obj": current_obj,
                              "followers": followers,
                              "users": users,
                              "tag_list": tag_list,
                              "category_list": category_list,
                              "date_list": date_list,
                              "comment_str": comment_str,
                          }
                          )
    else:
        return render(request,
                      "arts.html",
                      {
                          "article_detail": article_detail,
                          "obj": obj,
                          "current_obj": None,
                          "followers": followers,
                          "users": users,
                          "tag_list": tag_list,
                          "category_list": category_list,
                          "date_list": date_list,
                          "comment_str": comment_str,
                      }
                      )

def click(request):
    ret={"sts":True,"msg":None}
    try:
        current_name = request.session.get("username")#当前登录用户信息
        if current_name:#当前为登录状态
            article_id = request.POST.get("article_id")
            status = request.POST.get("status")
            blog_obj=models.Article.objects.filter(nid=article_id).first()
            blog_name=blog_obj.blog.user.username#当前博客用户名
            current_obj = models.UserInfo.objects.filter(username=current_name).first()
            up_down_obj = models.UpDown.objects.filter(article_id=article_id, user_id=current_obj.nid).first()
            print(current_obj.nid,article_id)
            if current_name == blog_name:  # 当前登录用户和博客为同一个人
                return HttpResponse("不能自己给自己赞踩")
            else:  # 当前登录用户和博客用户不是同一个人
                with transaction.atomic():
                    if not up_down_obj:#该用户没有点过赞或踩
                        if status=="True":  # 点赞
                            models.UpDown.objects.create(up_down=True, article_id=article_id, user_id=current_obj.nid)
                            models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)
                            return HttpResponse("add_ok")
                        elif status=="False":  # 点踩
                            models.UpDown.objects.create(up_down=False, article_id=article_id, user_id=current_obj.nid)
                            models.Article.objects.filter(nid=article_id).update(down_count=F("down_count") + 1)
                            return HttpResponse("add_no")
                    else:
                        if up_down_obj.up_down and status=="True":  # 取消赞
                            models.UpDown.objects.filter(user_id=current_obj.nid, article_id=article_id).delete()
                            models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") - 1)
                            return HttpResponse("del_ok")
                        if not up_down_obj.up_down and status=="False":  # 取消踩
                            models.UpDown.objects.filter(user_id=current_obj.nid, article_id=article_id).delete()
                            models.Article.objects.filter(nid=article_id).update(down_count=F("down_count") - 1)
                            return HttpResponse("del_no")
                        if up_down_obj.up_down == False or up_down_obj.up_down == True and status != str(up_down_obj.up_down):
                            return HttpResponse("你想多了！")  # 点击冲突时提示
        else:
            return HttpResponse("请先登录再操作！")#未登录用户点赞踩提示
    except Exception as e:
        ret["sts"]=False
        ret["msg"]=str(e)
    # return HttpResponse(json.dumps(ret))
    return HttpResponse(ret)

def manage(request,site,**kwargs):
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            condition[k] = v
    # print(condition)
    obj=models.Blog.objects.filter(site=site).first()
    # 大分类
    type_list = models.Article.type_choices
    # 个人分类
    category_list = models.Category.objects.filter(blog_id=obj.nid)
    # 个人标签
    tag_list = models.Tag.objects.filter(blog_id=obj.nid)
    # 进行筛选
    condition['blog_id'] = obj.nid
    article_list = models.Article.objects.filter(**condition)
    all_count = article_list.count()
    page_info = PageInfo(request.GET.get("page"), all_count, 5, "/" + site + "/manage-0-0-0.html", 11)
    articles = article_list[page_info.start():page_info.end()]

    return render(request,'manage.html',{
        'type_list':type_list,
        'category_list':category_list,
        'tag_list':tag_list,
        # 'article_list':article_list,
        'articles':articles,
        "page_info": page_info,
        'kwargs':kwargs,
        'site':site,
        'obj':obj,
    })

def new_article(request,site):
    if request.method=="GET":
        print(request.session.get("username"))
        print(request.session.get("password"))
        print(request.session.get("id"))
        msg=request.session.get("username")
        if not msg:
            return redirect("/home/")
        obj=ArticleForm()
        blog=models.Blog.objects.filter(site=site).first()
        current_obj=models.UserInfo.objects.filter(nid=blog.user.nid).first()
        followers = models.UserFans.objects.filter(user_id=current_obj.nid).count()  # 粉丝数量
        users = models.UserFans.objects.filter(follower_id=current_obj.nid).count()  # 关注数量
        tag_list = models.Article.objects.filter(blog=blog).values("tags__nid", "tags__title").annotate(c=Count("nid"))
        category_list = models.Article.objects.filter(blog_id=blog.nid).values("category_id","category__title", ).annotate(c=Count("nid"))
        type_choice_list = models.Article.type_choices
        # print(type_choice_list)
        categorys=[]
        for i in tag_list:
            if i["tags__title"]:
                categorys.append(i)
        return render(request,"new_article.html",{
            "obj":obj,
            "site":site,
            "current_obj":current_obj,
            "tag_list":tag_list,
            "category_list":category_list,
            "followers":followers,
            "users":users,
            "categorys":categorys,
            "type_choice_list":type_choice_list,
        })
    else:
        obj=ArticleForm(request.POST)
        msg=request.session.get("username")
        if not msg:
            return redirect("/home/")
        if obj.is_valid():
            content=obj.cleaned_data["content"]
            summary = content[:30]
            title=obj.cleaned_data["title"]
            tag = request.POST.get("tag") if request.POST.get("tag") else 0
            type = request.POST.get("type") if request.POST.get("type") else 0
            blog_id = request.session.get("id")

            artic_obj = models.Article.objects.create(
                title=title,
                summary=summary,
                read_count=0,
                comment_count=0,
                up_count=0,
                down_count=0,
                article_type_id=tag,
                blog_id=blog_id,
                category_id=type,
            )

            models.ArticleDetail.objects.create(
                content=content,
                article_id=artic_obj.nid,
            )
            return render(request,"see.html",{"content":content})

def reply(request):



    return HttpResponse(666)
















def wangzhe(request):
    if request.method=="GET":
        obj=ArticleForm()
        return render(request,"wangzhe.html",{"obj":obj})
    else:
        obj=ArticleForm(request.POST)
        if obj.is_valid():
            print(111111111111111)
            msg=obj.cleaned_data["content"]
            print(msg)
            # msg=9999999999999

            return render(request,"see.html",{"msg":msg})

def upload(request):
    upload_type=request.GET.get("dir")
    print(upload_type)
    # print(request.POST,request.FILES)
    file_obj=request.FILES.get("imgFile")
    file_path=os.path.join("static/img",file_obj.name)
    with open(file_path,"wb") as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    dic = {
        'error': 0,
        'url': "/"+file_path,
        'message': '错误了...'
    }
    import json
    return HttpResponse(json.dumps(dic))
    # return render(request,"see.html",)

def test(request):
    models.Comment.objects.create(
        content="你麻麻喊你回家吃乃乃~~",
        article_id="16",
        user_id="3",
        reply_id="",
        # title="宝塔镇河妖",
        # summary="你大爷还是你大爷！",
        # read_count="232",
        # comment_count="154",
        # up_count="53",
        # down_count="1",
        # article_type_id="4",
        # blog_id="3",
        # category_id="3",
    )
    return HttpResponse(666)
