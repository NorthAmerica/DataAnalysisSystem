from django.urls import path
from . import views

app_name='das'

urlpatterns = [
	#path('',views.login,name='login'),
	path('login_check',views.login_check,name='login_check'),
	path('index',views.index, name='index'),
	path('data_upload',views.data_upload_view.as_view(), name='data_upload'),
]