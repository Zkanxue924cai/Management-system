# @user: 看雪
# @Time: 2025/2/14 下午4:45
# @Project: PyCharm
# @FileName: urls.py
from django.urls import path,include
from .views import *

urlpatterns = [
    path('enroll/',EnrollView.as_view(),name='enroll'),
    path('login/',LoginView.as_view(),name='login'),
    path('image/',ImageView.as_view(),name='image'),
    path('index/',IndexView.as_view(),name='index'),
    path('alone/',AloneView.as_view(),name='alone'),
    path('indextwo/',IndexTwoView.as_view(),name='indextwo'),
]