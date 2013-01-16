from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gtd.views.home', name='home'),
    # url(r'^gtd/', include('gtd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'todo.views.status_report'),
    url(r'^list/(?P<list_id>\d+)/$', 'todo.views.list_detail'),
    url(r'^item/(?P<item_id>\d+)/$', 'todo.views.item_detail'),
    #url(r'^item/(?P<item_id>\d+)/complete/$', 'todo.views.complete_item'),
    url(r'^list/(?P<list_id>\d+)/delete/$', 'todo.views.list_delete'),
    url(r'^item/(?P<item_id>\d+)/delete/$', 'todo.views.item_delete'),
)
