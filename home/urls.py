from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('welcome/',views.Welcome.as_view(),name='welcome'),
    path('userDetails/<int:pk>/',views.UserDetails.as_view(),name='userDetails'),
    path('paginationapi',views.paginationApi.as_view(),name="paginationapi")
]