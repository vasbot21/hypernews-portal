from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view),
    path('<int:link>/', views.news_page),
    path('create/', views.create_article)
]
