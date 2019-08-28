#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import re

class M1(MiddlewareMixin):
    def precess_request(self,request,*args,**kwargs):
        valid=[
            "/auth-login.html/",
            "/index.html/"
        ]
        if request.path.info not in valid:
            action=request.GET.get("md")
            user_permission_dict=request.session.get("user_permission_dict")
            if not user_permission_dict:
                return HttpResponse("无权限")

            flag=False
            for k,v in user_permission_dict.items:
                if re.match(k,request.path_info):
                    if action in v:
                        flag=True
                        break
                return HttpResponse("无权限")


# class M2(MiddlewareMixin):
#     def precess_request(self, request, *args, **kwargs):
#         valid = [
#             "/auth-login.html/",
#             "/index.html/"
#         ]
#         if request.path.info not in valid:
#             action = request.GET.get("md")
#             user_permission_dict = request.session.get("user_permission_dict")
#             if not user_permission_dict:
#                 return HttpResponse("无权限")
#             action_list = user_permission_dict.get(request.path_info)
#
#             if not action_list:
#                 return HttpResponse("无权限")
#             if action not in action_list:
#                 return HttpResponse("无权限")