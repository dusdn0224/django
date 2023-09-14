from django.urls import path
from . import views

app_name = 'fruits'
urlpatterns = [
    path('fruit/', views.fruit, name='fruit'),
]
