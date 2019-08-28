from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
from utils.xss import xss

class RegisterForm(Form):
    username=fields.CharField(
        max_length=10,
        min_length=3,
        required=True,
        widget=widgets.TextInput(attrs={"placeholder": "用户名",'class':'form-control'}),
        error_messages={
            "required":"用户名不能为空",
            "min_length": "用户名长度必须在3-10个字符",
            "max_length": "用户名长度必须在3-10个字符",
        }
    )
    nickname = fields.CharField(
        max_length=10,
        min_length=3,
        required=True,
        widget=widgets.TextInput(attrs={"placeholder": "昵称",'class':'form-control'}),
        error_messages={
            "required": "用户名不能为空",
            "min_length": "用户名长度必须在3-10个字符",
            "max_length": "用户名长度必须在3-10个字符",
        }
    )
    password=fields.CharField(
        min_length=3,required=True,
        widget=widgets.TextInput(attrs={"placeholder": "密码",'class':'form-control'}),
        error_messages={
            "min_length":"密码长度不得少于3个字符",
            "required":"密码不能为空",
        }

    )
    pwd = fields.CharField(
        min_length=3, required=True,
        widget=widgets.TextInput(attrs={"placeholder": "确认密码",'class':'form-control'}),
        error_messages={
            "min_length": "密码长度不得少于3个字符",
            "required": "密码不能为空",
        }

    )
    email=fields.EmailField(
        widget=widgets.TextInput(attrs={"placeholder": "邮箱",'class':'form-control'}),
        error_messages={
            "required":"邮箱不能为空",
            "invalid":"邮箱格式错误"
        }
    )
    avatar=fields.FileField(
        widget=widgets.FileInput(attrs={"id":"imgSelect","class":"f1"}),
        # error_messages={'incomplete': 'Enter a country calling code.'},
    )
    def __init__(self,request,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.request=request

    def clean_code(self):
        input_code=self.cleaned_data.get("code")
        session_code=self.request.session.get("code")
        if input_code.upper()==session_code.upper():
            return input_code
        raise ValidationError("验证码错误")

    def clean(self):
        p1=self.cleaned_data.get("password")
        p2=self.cleaned_data.get("pwd")
        if p1==p2:
            # return self.cleaned_data
            return None
        # self.add_error(None,ValidationError("密码不一致"))     默认下加到 __all__里
        self.add_error("pwd",ValidationError("密码不一致"))    #定义加到pwd字段里

class LoginForm(Form):
    username=fields.CharField(
        max_length=10,
        min_length=3,
        required=True,
        widget=widgets.TextInput(attrs={"placeholder":"用户名"}),
        error_messages={
            "required":"用户名不能为空",
            "min_length": "用户名长度必须在3-10个字符",
            "max_length": "用户名长度必须在3-10个字符",
        }
    )
    password=fields.CharField(
        min_length=3,required=True,
        widget=widgets.TextInput(attrs={"placeholder": "密码"}),
        error_messages={
            "min_length":"密码长度不得少于3个字符",
            "required":"密码不能为空",
        }

    )

class ArticleForm(Form):
    title=fields.CharField(
        max_length=64,
        widget=widgets.TextInput(attrs={"id":"in","name":"title"}),
    )
    content=fields.CharField(
        widget=widgets.Textarea(attrs={"id":"msg","name":"content"}),
    )
    def clean_content(self):
        old_content=self.cleaned_data["content"]
        return xss(old_content)

class CommentForm(Form):
    content=fields.CharField(
        widget=widgets.Textarea(attrs={"id":"msg","name":"content"}),
    )
    def clean_content(self):
        old_content=self.cleaned_data["content"]
        return xss(old_content)