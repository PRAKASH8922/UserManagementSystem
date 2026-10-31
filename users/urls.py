from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.index_view, name='index'),
    path('index.html', views.index_view, name='index_html'),
    path('login', views.login_view, name='login'),
    path('login/', views.login_view, name='login_slash'),
    path('login.html', views.login_view, name='login_html'),
    path('signup', views.signup_view, name='signup'),
    path('signup/', views.signup_view, name='signup_slash'),
    path('signup.html', views.signup_view, name='signup_html'),

    # REST API endpoints matching original Node.js paths
    path('user', views.user_list_create, name='user_list_create'),
    path('user/', views.user_list_create, name='user_list_create_slash'),
    path('user/login', views.user_login, name='user_login'),
    path('user/login/', views.user_login, name='user_login_slash'),
    path('user/<int:user_id>', views.user_detail, name='user_detail'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail_slash'),
]
