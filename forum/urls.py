from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('topic/<int:topic_id>/new_post/', views.new_post, name='new_post'),
]
