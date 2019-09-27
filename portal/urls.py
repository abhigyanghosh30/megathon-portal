from django.urls import path, include
from . import views

app_name = 'portal'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('err/', views.error, name='error')
]
