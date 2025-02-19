import base64
import code
import json
import random
from urllib import request

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.http import HttpResponse
import math
from django.http import JsonResponse
from django.views import View
from .models import *


# 验证码生成区域
def generate_code():
    # 生成随机数
    code = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
    return code


def create_image(code):
    # 生成图片（等待填入内容）
    width = 100
    height = 40
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    # 添加干扰线
    for i in range(2):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        draw.line((x1, y1), fill=(255, 255, 255))
    # 设置验证码文字样式
    font = ImageFont.truetype('simsun.ttc', size=28)
    for i, char in enumerate(code):
        draw.text((15 + i * 18, 5), char, font=font, fill=(0, 0, 0))
    # 转为二进制
    buffer = BytesIO()
    image.save(buffer, 'PNG')
    return buffer.getvalue()


class ImageView(View):
    def get(self, request):
        # 调用方法，生成验证码
        captcha = generate_code()
        image = create_image(captcha)
        base64_image = base64.b64encode(image).decode('utf-8')
        return JsonResponse({'image': f'data:image/png;base64,{base64_image}', 'captcha': captcha})


# Create your views here.
class EnrollView(View):
    def post(self, request):
        body = json.loads(request.body)
        User.objects.create(
            name=body['name'],
            password=body['password'],
            email=body['email'],
            phone=body['phone']
        )
        return JsonResponse({'code': 200})


class LoginView(View):
    def post(self, request):
        body = json.loads(request.body)
        all_users = User.objects.all()
        for user in all_users:
            if user.name == body['name'] and user.password == body['password']:
                if body['captcha_session'] != body['captcha']:
                    return JsonResponse({'error': '验证码错误'})
                return JsonResponse({'code': 200})

        return JsonResponse({'error': '用户名或密码错误'})


class IndexTwoView(View):
    def get(self, request):
        data_all = Data.objects.all()
        data = []
        for i in data_all:
            data.append({
                'id': i.id,
                'is_up': i.is_up,
                'encode': i.encode,
                'name': i.name,
                'category': i.category,
                'node': i.node,
                'type': i.type,
                'car': i.car,
                'num': i.num,
            })
        return JsonResponse(
            {'data': data}
        )

class IndexView(View):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 4))
        data_all = Data.objects.all()
        data_count = data_all.count()
        max_page = math.ceil(data_all.count() / page_size)
        start = (page - 1) * page_size
        end = page * page_size
        data = []
        for i in data_all:
            data.append({
                'id': i.id,
                'is_up': i.is_up,
                'encode': i.encode,
                'name': i.name,
                'category': i.category,
                'node': i.node,
                'type': i.type,
                'car': i.car,
                'num': i.num,
            })
        data = data[start:end]
        return JsonResponse(
            {'data': data, 'page': page, 'page_size': page_size, 'max_page': max_page, 'data_count': data_count}
        )

    def post(self, reqeust):
        body = json.loads(reqeust.body)
        Data.objects.create(
            encode=body['encode'],
            name=body['name'],
            category=body['category'],
            node=body['node'],
            type=body['type'],
            car=body['car'],
            num=body['num'],
        )
        return JsonResponse({'code': 200})

    def put(self, reqeust):
        pass

    def patch(self, request):
        id = request.GET.get('id')
        data = Data.objects.get(id=id)
        if data.is_up == 0:
            data.is_up = 1
            data.save()
        else:
            data.is_up = 0
            data.save()
        return JsonResponse({'code': 200})

    def delete(self, request):
        id = request.GET.get('id')
        list_id = id.split(',')
        for i in list_id:
            is_up = Data.objects.get(id=i).is_up
            if is_up == 0:
                Data.objects.get(id=i).delete()
            else:
                pass
        return JsonResponse({'code': 200})


class AloneView(View):
    def get(self, request):
        id = request.GET.get('id')
        Da = Data.objects.get(id=id)
        data = []
        data.append({
            'encode': Da.encode,
            'name': Da.name,
            'category': Da.category,
            'node': Da.node,
            'type': Da.type,
            'car': Da.car,
            'num': Da.num,
        })
        return JsonResponse({'data': data})

    def put(self, request):
        id = request.GET.get('id')
        body = json.loads(request.body)
        Data.objects.filter(id=id).update(
            type=body['type'],
            car=body['car'],
            num=body['num'],
            name=body['name'],
            encode=body['encode'],
            category=body['category'],
            node=body['node'],
        )
        return JsonResponse({'code': 200})
