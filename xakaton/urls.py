from django.urls import path, include
from xakaton.views import (
    aboutproject, xaki, registcommand, aboutmirea, aboutcommand, 
    teamaccept, createteam, hackathon_list, hackathon_detail, admin_hack
)

app_name = 'xakaton'

urlpatterns = [
    path('aboutproject/', aboutproject, name='aboutproject'),
    path('', xaki, name='xaki'),
    path('registcommand', registcommand, name='registcommand'),
    path('aboutmirea', aboutmirea, name='aboutmirea'),
    path('aboutcommand', aboutcommand, name='aboutcommand'),
    path('teamaccept', teamaccept, name='teamaccept'),
    path('createteam', createteam, name='createteam'),
    path('admin/hack/', admin_hack, name='admin_hack'),
    
    # API endpoints
    path('api/hackathons/', hackathon_list, name='hackathon_list'),
    path('api/hackathons/<int:pk>/', hackathon_detail, name='hackathon_detail'),
]