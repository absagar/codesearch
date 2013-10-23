from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'whooshter.views.home', name='home'),
    # url(r'^whooshter/', include('whooshter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^whooster/$', 'woosterapp.views.index'),
    url(r'^whooster/file/(?P<docnum>\d+)/$', 'woosterapp.views.showfile'),
    url(r'^whooster/results/$', 'woosterapp.views.formResults'),
    url(r'^whooster/(?P<query_term>\D+)/(?P<filetype>\D+)/$', 'woosterapp.views.filteredresults'),
    url(r'^whooster/(?P<query_term>\D+)/$', 'woosterapp.views.results'),
)