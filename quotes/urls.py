from django.urls import path
from . import views


app_name = 'quotes'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_quote, name='add_quote'),  # Добавление цитаты
    path('top/', views.top_quotes, name='top_quotes'),  # Топ цитат
    path('vote/', views.vote, name='vote'),  # Голосование
]
