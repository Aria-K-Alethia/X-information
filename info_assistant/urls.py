"""info_assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView
from backend import views as backend_views
from django.conf.urls.static import static

urlpatterns = [
	#pages
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html')), # NEW
    url(r'^index/$', backend_views.home, name='index'),
    url(r'^book/$',backend_views.home,name="book"),
    #API
    ##user
    url(r'^user/login/$',backend_views.user_login,name="user_login"),
    url(r'^user/logout/$',backend_views.user_logout,name="user_logout"),
    url(r'^user/logged_in/$',backend_views.user_logged_in,name="user_logged_in"),
    ##notification
    url(r'^notification/refresh/$',backend_views.notification_refresh,name="notification_refresh"),
    url(r'^notification/newest/$',backend_views.notification_newest,name="notification_newest"),
    url(r'^notification/history/$',backend_views.notification_history,name="notification_history"),
    url(r'^notification/delete/$',backend_views.notification_delete,name="notifiaction_delete"),
    url(r'^notification/per_month/$',backend_views.notification_per_month,name="notification_per_month"),
    url(r'^notification/total/$',backend_views.notification_total,name="notification_total"),
    ##book
    url(r'^book/insert/$',backend_views.book_insert,name="book_insert"),
    url(r'^book/modify/$',backend_views.book_modify,name="book_modify"),
    url(r'^book/delete/$',backend_views.book_delete,name="book_delete"),
    url(r'^book/info_list/$',backend_views.book_info_list,name="book_info_list"),
    url(r'^book/id_list/$',backend_views.book_id_list,name="book_id_list"),
    url(r'^book/per_year/$',backend_views.book_per_year,name="book_per_year"),
    ##journal
    url(r'^journal/insert/$',backend_views.journal_insert,name="journal_insert"),
    url(r'^journal/modify/$',backend_views.journal_modify,name="journal_modify"),
    url(r'^journal/delete/$',backend_views.journal_delete,name="journal_delete"),
    url(r'^journal/info/$',backend_views.journal_info,name="journal_info"),
    url(r'^journal/id_list/$',backend_views.journal_id_list,name="journal_id_list"),
    url(r'^journal/info_all/$',backend_views.journal_info_all,name="journal_info_all")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
