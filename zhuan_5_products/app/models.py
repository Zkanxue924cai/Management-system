from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20,verbose_name="用户名")
    password = models.CharField(max_length=20,verbose_name="密码")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20,verbose_name="电话号码")

class Data(models.Model):
    is_up = models.IntegerField(choices=((0,'禁用'),(1,"启用")),default=0,verbose_name="产品状态")
    encode = models.CharField(max_length=20,verbose_name="产品编码")
    name = models.CharField(max_length=20,verbose_name="产品名称")
    category = models.CharField(max_length=20,verbose_name="产品品类")
    node = models.CharField(max_length=20,verbose_name="节点类型")
    type = models.CharField(max_length=20,verbose_name="产品类型")
    car = models.CharField(max_length=20,verbose_name="接入车系")
    num = models.IntegerField(max_length=20,verbose_name="接入设备数量")