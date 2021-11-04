from django.conf.urls import url
from django.urls.resolvers import URLPattern
from DisplayData import views

urlpatterns = [
    url(r'^formInput/$', views.formInputAPI)
]