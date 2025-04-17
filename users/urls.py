from django.urls import path, include

from users.views import (
    login, registration, profile, editprofile, changelogin, addmail,
    addmailcorrect, restorepassword, logout_view, admin_hack,
    admin_list, user_detail, toggle_user_status
)

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('changelogin/', changelogin, name='changelogin'),
    path('editprofile/', editprofile, name='editprofile'),
    path('addmail/', addmail, name='addmail'),
    path('addmailcorrect/', addmailcorrect, name='addmailcorrect'),
    path('restorepassword/', restorepassword, name='restorepassword'),
    path('logout/', logout_view, name='logout'),
    path('admin-hack/', admin_hack, name='admin_hack'),
    path('admin/users/', admin_list, name='admin_list'),
    path('api/users/<int:user_id>/', user_detail, name='user_detail'),
    path('api/users/<int:user_id>/toggle_status/', toggle_user_status, name='toggle_user_status'),
]


