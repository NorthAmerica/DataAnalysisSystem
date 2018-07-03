from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .forms import TxtDataForm
from .models import Txt_Data
from .tools import readtools

# Create your views here.
def login(request):
	return render(request, 'login.html')

def login_check(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	resp = {'success': True}
	return JsonResponse(resp)

def index(request):
	#print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	return render(request, 'index.html')

# 数据上传页面
class data_upload_view(View):
	def get(self, request):
		txt_list = Txt_Data.objects.all()
		return render(request, 'date_upload.html',{'txts':txt_list})

	def post(self, request):
		try:
			form = TxtDataForm(self.request.POST, self.request.FILES)
			if form.is_valid():
				if form.cleaned_data.get('file').content_type=='text/plain':
					file_name = form.cleaned_data.get('file')._name
					file_date = file_name[-14:-4]
					account = file_name[:-14]
					new_file = form.save(commit=False)
					new_file.account = account
					new_file.file_date = file_date
					saved_film = form.save()
					r = readtools.ReadTxt()
					r.analyzer(r.reader(saved_film.file.name))
					data = {'is_valid': True, 'name': saved_film.file.name, 'url': saved_film.file.url}
				else:
					data={'is_valid':False,'message':'上传的文件格式必须是TXT文件！'}
			else:
				data = {'is_valid': False,'message':'上传的文件校验失败！'}
			return JsonResponse(data)
		except RuntimeError as err:
			data = {'is_valid': False, 'message': err}
			return JsonResponse(data)

# 获取JSON数据
def get_json(request):
	resp = {'success':True}
	return JsonResponse(resp)