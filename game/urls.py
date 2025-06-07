from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('jobs/', views.jobs_view, name='jobs'),
    path('do-job/<int:job_id>/', views.do_job_view, name='do_job'),
    path('equipment/', views.equipment_view, name='equipment'),
    path('buy-equipment/<int:item_id>/', views.buy_equipment_view, name='buy_equipment'),
    path('fight/', views.fight_view, name='fight'),
    path('attack/<int:target_id>/', views.attack_view, name='attack'),
    path('family/', views.family_view, name='family'),
]