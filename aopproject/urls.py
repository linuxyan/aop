from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('aop.views',
    # Examples:
    # url(r'^$', 'aopproject.views.home', name='home'),
    # url(r'^aopproject/', include('aopproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'login'),
    url(r'^loginout/$', 'loginout'),
    url(r'^$', 'index'),
    url(r'^svnadd/$', 'svnadd'),
    url(r'^hostadd/$', 'hostadd'),
    url(r'^hostedit/(?P<host_id>[^/]+)$', 'hostedit'),
    url(r'^hostdel/(?P<host_id>[^/]+)$', 'hostdel'),
    url(r'^confirm_del/(?P<host_id>[^/]+)$', 'confirm_del'),
    url(r'^showsvn/$', 'showsvn'),
    url(r'^showsvnlog/$', 'showsvnlog'),
    url(r'^svnedit/(?P<svn_id>[^/]+)$', 'svnedit'),
    url(r'^svnupdate/(?P<svn_id>[^/]+)/(?P<u_type>[^/]+)$', 'svnupdate'),
    url(r'^group/$', 'group'),
    url(r'^task/$', 'task'),
    url(r'^task_del/(?P<task_id>[^/]+)$', 'task_del'),
    url(r'^task_status/(?P<task_id>[^/]+)$', 'task_status'),
    url(r'^task_run/$', 'task_run'),
    url(r'^addtogroup/$', 'addtogroup'),
    url(r'^addscript/$', 'addscript'),
    url(r'^showscript/$', 'showscript'),
    url(r'^delscript/(?P<script_id>[^/]+)$', 'delscript'),
    url(r'^hostgroup_detail/(?P<group_id>[^/]+)$', 'hostgroup_detail'),
    url(r'^hostgroup_del/(?P<group_id>[^/]+)$', 'hostgroup_del'),
    url(r'^scriptgroup_detail/(?P<group_id>[^/]+)$', 'scriptgroup_detail'),
    url(r'^scriptgroup_del/(?P<group_id>[^/]+)$', 'scriptgroup_del'),
    url(r'^hostgroup_del_host/$', 'hostgroup_del_host'),
    url(r'^scriptgroup_del_script/$', 'scriptgroup_del_script'),
    url(r'^test/$', 'test'),
    
)
