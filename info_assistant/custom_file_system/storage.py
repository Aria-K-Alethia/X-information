# -*- coding: UTF-8 -*-
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
import random
class ImageStorage(FileSystemStorage):
	def __init(self,location=settings.MEDIA_ROOT,base_url=settings.MEDIA_URL):
		super(ImageStorage).__init__(location,base_url)
		def _save(self,name,content):
			ext_name = os.path.splitext(name)[1]
			dir_name = os.path.dirname(name)
			filename = datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")
			filename += "%d" % random.randint(0,100)
			name = os.path.join(dir_name,filename+ext)
			return super(ImageStorage,self),_save(name,content)