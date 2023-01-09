from django.urls import path
from .views import Login, Register, EmailVerify, Logout

urlpatterns= [
    path('email-verify/<token>', EmailVerify.as_view(), name='email-verify'),
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view()),
]