from django.urls import path
from . views import index,home

app_name = 'app'

urlpatterns = [
    path("", home, name="home"),
    
]
