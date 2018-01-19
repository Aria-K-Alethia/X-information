from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import connection
from .crawler import *
from .models import Book,Notification,Journal
from datetime import datetime
from datetime import timedelta
import copy

import json
# Create your views here.
category_dict = {0:'北航教务',1:'北航官网'}
journal_category_dict = { 0:'学习报告', 1:'读书笔记'}
cursor = connection.cursor()
def home(request):
	return render(request, 'index.html')

def start_crawlers():
	output = buaa_index_feeder()
	output += buaa_jiaowu_feeder()
	if(len(output) != 0):
		i = 0
		while(i < len(output)):
			try:
				output[i].save()
			except Exception as e:
				print('ignore this noti cause it contains unnecessary info',output[i])
				output.pop(i)
				i -= 1
			i += 1
		return (output[0].id if len(output) != 0 else -1)
	else:
		return -1

#Customized JSONEncoder
class Customized_Encoder(json.JSONEncoder):
	def default(self,obj):
		if(isinstance(obj,datetime)):
			return obj.strftime("%Y-%m-%d %H:%M:%S")
		else:
			return json.JSONEncoder.default(self,obj)


@csrf_exempt
def user_login(request):
	if(request.method == 'POST'):
		data = request.POST
		username = str(data.get('username'))
		password = str(data.get('password'))
		user = auth.authenticate(request,username=username,password=password)
		if(user is not None and user.is_active):
			auth.login(request,user)
			request.session['username'] = username
			return HttpResponse(json.dumps({'code': 0, 'username':user.username}))
		else:
			return HttpResponse(json.dumps({'code': 1}))

@csrf_exempt
def user_logged_in(request):
	if(request.method == 'POST'):
		username = request.session.get('username',default=None)
		if(username == None):
			return HttpResponse(json.dumps({'username': None}))
		else:
			return HttpResponse(json.dumps({'username': username}))

@csrf_exempt
def user_logout(request):
	if(request.method == 'POST'):
		try:
			auth.logout(request)
			return HttpResponse(json.dumps({'code': 0}))
		except Exception as e:
			return HttpResponse(json.dumps({'code': 1}))

@csrf_exempt
def notification_refresh(request):
	if(request.method == 'POST'):
		begin_id = start_crawlers()
		print(begin_id)
		if(begin_id >= 0):
			return HttpResponse(json.dumps({'code': 0,'begin_id':begin_id}))
		else:
			return HttpResponse(json.dumps({'code': 1}))

@csrf_exempt
def notification_newest(request):
	if(request.method == 'POST'):
		begin_id = int(request.POST.get('begin_id'))
		result = Notification.objects.filter(id__gte=begin_id)
		result = list(result.values('id','noti_from','overview','link','post_time'))
		for item in result:
			item['noti_from'] = category_dict[item['noti_from']]
		return HttpResponse(json.dumps({'info_list':result},cls=Customized_Encoder))

@csrf_exempt
def notification_history(request):
	if(request.method == 'POST'):
		date = datetime.strptime(str(request.POST.get('from_time')),"%Y %m %d %H")
		keys = ('id','noti_from','post_time','link','overview')
		date = date - timedelta(days=3)
		'''
		result = Notification.objects.filter(post_time__gte=date)
		result = list(result.values('id','noti_from','overview','link','post_time'))
		for item in result:
			item['noti_from'] = category_dict[item['noti_from']]
		''' 
		cursor.callproc('get_history_notification',[date])
		result = cursor.fetchall()
		cursor.nextset()
		result = [dict(zip(keys,item)) for item in result]
		result.reverse()
		for item in result:
			item['noti_from'] = category_dict[item['noti_from']]
		return HttpResponse(json.dumps({'info_list':result},cls=Customized_Encoder))

@csrf_exempt
def notification_delete(request):
	if(request.method == 'POST'):
		target_id = int(request.POST.get('id'))
		try:
			target = Notification.objects.get(id=target_id)
			target.delete()
			return HttpResponse(json.dumps({'code': 0}))
		except Exception as e:
			return HttpResponse(json.dumps({'code': 1}))

@csrf_exempt
def notification_per_month(request):
	if(request.method == 'POST'):
		from_date = datetime.strptime(str(request.POST.get('from_time')),"%Y-%m")
		end_date = datetime.strptime(str(request.POST.get('end_time')),"%Y-%m")
		keys = []
		data_list = []
		flag = False
		for noti_from,name in category_dict.items():
			data = []
			temp = copy.copy(from_date)
			while(temp <= end_date):
				if(not flag):
					keys.append(datetime.strftime(temp,"%Y-%m"))
				cursor.callproc("get_noti_per_month",[temp,noti_from])
				try:
					data.append(str(cursor.fetchone()[0]))	
				except Exception as e:
					print("error in noti per month:can not fetch data")
				cursor.nextset()
				temp = datetime(temp.year,temp.month+1,temp.day) if temp.month != 12 else datetime(temp.year+1,1,temp.day)
			flag = True
			data_list.append({'noti_from':name,'data':data})
		return HttpResponse(json.dumps({'keys':keys,'data_list':data_list}))

@csrf_exempt
def notification_total(request):
	if(request.method == 'POST'):
		from_date = datetime.strptime(str(request.POST.get('from_time'))+"-1","%Y-%m-%d")
		end_date = datetime.strptime(str(request.POST.get('end_time')+"-28"),"%Y-%m-%d")
		temp = end_date.month
		while(end_date.month == temp):
			end_date = end_date + timedelta(days=1)
		keys = []
		data_list = []
		for noti_from,name in category_dict.items():
			keys.append(name)
			data_list.append(Notification.objects.filter(noti_from=noti_from,post_time__gte=from_date,post_time__lt=end_date).count())
		print(data_list)
		return HttpResponse(json.dumps({'keys': keys,'data_list':data_list}))


@csrf_exempt
def book_insert(request):
	if(request.method == 'POST'):
		data = request.POST
		title = str(data.get('title'))
		author = str(data.get('author'))
		rate = float(data.get('rate')) if float(data.get('rate')) != 0 else None
		comment = str(data.get('comment'))
		name = str(request.FILES['file'].name)
		book = Book(title=title,author=author,rate=rate,comment=comment)
		book.img = request.FILES['file']
		try:
			book.save()
			return HttpResponse(json.dumps({'code':0}))
		except Exception as e:
			return HttpResponse(json.dumps({'code':1}))

@csrf_exempt
def book_id_list(request):
	if(request.method == 'POST'):
		#result = list(Book.objects.all.values_list('id',flat=True))
		cursor.callproc('get_book_id')
		temp = cursor.fetchall()
		cursor.nextset()
		try:
			result = list(item[0] for item in temp)
			return HttpResponse(json.dumps({'id_list':result}))
		except Exception as e:
			print('error in get_book_id')
			return HttpResponse(json.dumps({'code': 1}))

@csrf_exempt
def book_info_list(request):
	if(request.method == 'POST'):
		info_list = []
		data = request.POST
		id_list = data.get('id_list')
		keys = ('title','author','rate','comment','img','post_time')
		if(',' in id_list):
			id_list = id_list[1:-1].split(',')
		else:
			id_list = [id_list[1:-1]]
		for item in id_list:
			item = int(item)
			#result = Book.objects.filter(id=item)
			cursor.callproc('get_book_info',[item])
			result = cursor.fetchone()
			cursor.nextset()
			#if(len(result) == 0):
			if(result == None):
				return HttpResponse(json.loads({'code':1}))
			#book = result.values('title','author','rate','comment','img','post_time')[0]
			book = dict(zip(keys,result))
			print(book)
			book['img'] = settings.MEDIA_URL + str(book['img'])
			info_list.append(book)
		return HttpResponse(json.dumps({'info_list':info_list},cls=Customized_Encoder))

@csrf_exempt
def book_delete(request):
	if(request.method == 'POST'):
		data = request.POST
		target_id = int(data.get('id'))
		try:
			target = Book.objects.get(id = target_id)
			target.delete()
			return HttpResponse(json.dumps({'code':0}))
		except:
			return HttpResponse(json.dumps({'code':1}))

@csrf_exempt
def book_modify(request):
	if(request.method == 'POST'):
		data = request.POST
		target_id = data.get('id')
		try:
			target = Book.objects.get(id=target_id)
			target.title = str(data.get('title'))
			target.author = str(data.get('author'))
			target.rate = float(data.get('rate'))
			target.comment = str(data.get('comment'))
			target.img = request.FILES['file']
			target.save()
			return HttpResponse(json.dumps({'code':0}))
		except Exception as e:
			print(e)
			return HttpResponse(json.dumps({'code':1}))

@csrf_exempt
def book_per_year(request):
	if(request.method == 'POST'):
		keys = []
		data_list = []
		temp = Book.objects.order_by('post_time')
		begin_time = temp[0].post_time.year
		end_time = temp[temp.count() - 1].post_time.year
		while(begin_time <= end_time):
			keys.append(str(begin_time))
			data_list.append(str(Book.objects.filter(post_time__year=begin_time).count()))
			begin_time += 1
		print(data_list)
		return HttpResponse(json.dumps({'keys':keys,'data_list':data_list}))

@csrf_exempt
def journal_id_list(request):
	if(request.method == 'POST'):
		keys = ('id','category','title','post_time')
		try:
			cursor.callproc('get_journal_id')
			temp = cursor.fetchall()
			cursor.nextset()
			id_list = []
			for item in temp:
				id_list.append(dict(zip(keys,item)))
				id_list[-1]['category'] = journal_category_dict[id_list[-1]['category']]
			return HttpResponse(json.dumps({'id_list':id_list},cls=Customized_Encoder))
		except Exception as e:
			return HttpResponse(json.dumps({'id_list': []}))

@csrf_exempt
def journal_info(request):
	if(request.method == 'POST'):
		target_id = int(request.POST.get('id'))
		try:
			cursor.callproc('get_journal_info',[target_id])
			content = cursor.fetchone()[0]
			cursor.nextset()
			return HttpResponse(json.dumps({'content':content}))
		except Exception as e:
			return HttpResponse(json.dumps({'content':''}))

@csrf_exempt
def journal_info_all(request):
	if(request.method == 'POST'):
		target_id = int(request.POST.get('id'))
		try:
			journal = Journal.objects.filter(id=target_id).values('title','content','category','post_time')[0]
			journal['category'] = journal_category_dict[journal['category']]
			return HttpResponse(json.dumps({'info':journal},cls=Customized_Encoder))
		except Exception as e:
			return HttpResponse(json.dumps({'info': ''}))


@csrf_exempt
def journal_insert(request):
	if(request.method == 'POST'):
		data = request.POST
		title = str(data.get('title'))
		category = int(data.get('category'))
		content = str(data.get('content'))
		#user_id = int(request.user.id)
		user_id = 1
		journal = Journal(title=title,category=category,content=content,user_id = user_id)
		try:
			journal.save()
			return HttpResponse(json.dumps({'code': 0}))
		except Exception as e:
			print(e)
			return HttpResponse(json.dumps({'code': 1}))

@csrf_exempt
def journal_modify(request):
	if(request.method == 'POST'):
		data = request.POST
		title = str(data.get('title'))
		category = int(data.get('category'))
		content = str(data.get('content'))
		target_id = int(data.get('id'))
		try:
			journal = Journal.objects.get(id=target_id)
			journal.title = title
			journal.category = category
			journal.content = content
			journal.save()
			return HttpResponse(json.dumps({'code': 0}))
		except Exception as e:
			return HttpResponse(json.dumps({'code': 1}))

@csrf_exempt
def journal_delete(request):
	if(request.method == 'POST'):
		target_id = int(request.POST.get('id'))
		try:
			journal = Journal.objects.get(id=target_id)
			journal.delete()
			return HttpResponse(json.dumps({'code': 0}))
		except Exception as e:
			return HttpResponse(json.dumps({'code': 1}))