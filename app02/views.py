from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Count

# Create your views here.
from app02 import models

def foo(request):
    obj=models.User.objects.filter(username="root").first()
    x=models.User2Role.objects.filter(user_id=obj.id)
    role_list=models.Role.objects.filter(users__user_id=obj.id)
    print(obj.username,role_list)
    #此方法会在结果列表中多加一列数据
    # permission_list=models.Permission2Action2Role.objects.filter(role__in=role_list).values("permission__url","action__code").annotate(c=Count("id"))
    #此方法不会多加数据 ---  通过权限角色关系表查找到的某个用户的数据
    permission_list=models.Permission2Action2Role.objects.filter(role__in=role_list).values("permission__url","action__code").distinct()
    print(obj,permission_list)
    #通过role列表查找到的某个用户的所有权限
    obj=models.Role.objects.filter(users__user=obj).values("permission2rction2role__action__caption","permission2rction2role__role__caption","permission2rction2role__permission__caption")
    print(obj)
    return HttpResponse(1111111111)

def login(request):
    if request.method=="GET":
        return render(request,"login2.html")
    else:
        user_permission_dict={
            "/auth-index.html":["GET","POST","DEL","EDIT"],
            "/order.html":["GET","POST","DEL","EDIT"],
        }
        request.session["user_permission_dict"]=user_permission_dict
        return HttpResponse("登录成功")

