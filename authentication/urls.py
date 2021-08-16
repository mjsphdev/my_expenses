from django.urls import path

from . import views

urlpatterns = [
    path('sign_in/', views.SignIn.as_view(), name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('sign_up/', views.sign_up, name='sign_up')
]