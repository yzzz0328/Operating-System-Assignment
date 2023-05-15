from django.urls import path
from . import views

app_name = 'CPUnpp'

urlpatterns = [
    path('',views.home,name='home'),
    path('getnpp',views.getnpp, name='npp'),  
]
