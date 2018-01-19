import requests
import json
import hashlib
import re
import copy
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from .models import Notification

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36','Connection':'keep-alive'}

def get_buaa_noti(access):
	out = Notification()
	try:
		out.overview = access.attrs['title']
	except Exception as e:
		out.overview = access.string
	out.link = access.attrs['href']
	out.noti_from = 1
	res = requests.get(out.link,headers=headers)
	res.encoding = 'utf8'
	soup = BeautifulSoup(res.text)
	try:
		node = soup.select('body > div.main.w1102 > form > div.newsleft.auto > div.newsleftcon.auto > div.newsleftconmes.auto > p > span.ri')[0]
	except Exception as e:
		print('No post time in ',out)
	node = node.get_text()
	reg = r'\d{4}-\d{1,2}-\d{1,2}'
	match = re.search(reg,node)
	if(match != None):
		date = match.group(0).split('-')
		out.post_time = datetime(int(date[0]),int(date[1]),int(date[2]))
	else:
		print('No post time in ',out)
		out = None
	return out



def buaa_index_feeder():
	filename="buaa_index.time"
	url="http://www.buaa.edu.cn"
	reg1 = re.compile(r'http://news.buaa.edu.cn/info/(1011|1010|1002)/.+')
	if(not os.path.isfile(filename)):
		file = open(filename,"w")
		now = datetime.now()
		date = [str(now.year),str(now.month),str(now.day)]
		file.write(" ".join(date))
		file.close()
	with open(filename,"r") as file:
		date = file.readline().split(' ')
		last_date = datetime(int(date[0]),int(date[1]),int(date[2]))
		print(last_date)
		res = requests.get(url,headers=headers)
		res.encoding = "utf8"
		#获得所有新闻url -> 获得除了时间以外的数据 -> 获得时间并判断时间戳,同时更新时间戳
		soup = BeautifulSoup(res.text)
		accesses = soup.find_all("a",attrs={'href':reg1})
		output = []
		latest = last_date
		for item in accesses:
			temp = get_buaa_noti(item)
			time.sleep(1)
			if(temp != None and temp.post_time > last_date):
				if(temp.post_time > latest):
					latest = temp.post_time
				output.append(temp)
			elif(temp != None and temp.post_time == last_date):
				queryset = Notification.objects.filter(link=temp.link)
				if(len(queryset) == 0):
					output.append(temp)
			else:
				print('ignore noti because it is old:',temp)
	if(latest != last_date):
		with open(filename,"w") as file:
			date = [str(latest.year),str(latest.month),str(latest.day)]
			file.write(" ".join(date))
	return output

def get_jiaowu_noti(access,code_now):
	url = 'http://jiaowu.buaa.edu.cn/bhjwc2.0/index/newsView.do?xwid='
	reg = r'\d+'
	out = Notification()
	code = re.findall(reg,access.attrs['onclick'])[0]
	if(int(code) <= code_now):
		return None,None
	url += code
	if(len(Notification.objects.filter(link__endswith=code)) != 0):
		return None,None
	out.link = url
	out.overview = access.attrs['title']
	out.noti_from = 0
	out.post_time = datetime.now()
	return out,int(code)

def buaa_jiaowu_feeder():
	#0502:学生相关
	#0201:通知
	reg1 = re.compile(r'javascript:onNewsView\(\'\d+\',\'(0502)|(0201)\'\);return false;')
	url1 = 'http://jiaowu.buaa.edu.cn'
	filename = "buaa_jiaowu.time"
	if(not os.path.isfile(filename)):
		file = open(filename,"w")
		file.write("0")
		file.close()
	file = open(filename,"r")
	code = int(file.readline())
	file.close()
	res = requests.get(url1,headers=headers)
	res.encoding = 'utf8'
	soup = BeautifulSoup(res.text)
	accesses = soup.find_all("a",attrs={'onclick':reg1})
	output = []
	latest = code
	for item in accesses:
		temp,temp_code = get_jiaowu_noti(item,code)
		if(temp != None):
			output.append(temp)
			if(temp_code > latest):
				latest = temp_code
	if(latest != code):
		with open(filename,"w") as file:
			file.write(str(latest))
	return output

