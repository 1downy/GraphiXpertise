from django.urls import path
from gpu import views


urlpatterns = [
    path('', views.home, name='home'),
    path('compare', views.compare, name='compare'),
    path('about', views.about, name='about')
]
