from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from Market.views import createNewUser
from django.conf import settings

urlpatterns = [
	url(r'^Top/', TemplateView.as_view(template_name='Market/Top.html')),
    url(r'^login/', TemplateView.as_view(template_name='Market/login.html')),
    url(r'^create_new_user/', TemplateView.as_view(template_name='Market/create_new_user.html')),
    url(r'^create_new_user_confirm/', createNewUser),
    url(r'^tutorial/', TemplateView.as_view(template_name='Market/tutorial.html')),
    url(r'^market/', include('Market.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
