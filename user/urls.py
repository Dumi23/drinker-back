from django.urls import path
from .views import Login, Register, EmailVerify, Logout, Google, Me, UpdateUser
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns= [
    path('email-verify/<token>', EmailVerify.as_view(), name='email-verify'),
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view()),
    path('google', Google.as_view()),
    path('me', Me.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('update', UpdateUser.as_view()),
]