from django.urls import path
from . import views

app_name='dump_data'
urlpatterns = [
    path('',views.home,name='home'),
    path('data-point/', views.DataPoint.as_view(), name='data_point')
]