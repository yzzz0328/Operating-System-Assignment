from django.urls import path
from . import views

app_name = 'CPUrr'

urlpatterns = [
    path('',views.home,name='rrhome'),
    path('getrr',views.getrr, name='rr'),  
]
