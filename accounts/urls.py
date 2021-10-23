from django.urls import path
from .views import RegisterLoginAPIView , VerifyAuthenticationCodeAPIView,UserProfileAPIView,ReferralAPIView

app_name = 'Accounts'

urlpatterns = [
    path('register-login', RegisterLoginAPIView.as_view(), name='Register-Login'),
    path('verify-code', VerifyAuthenticationCodeAPIView.as_view(), name='Verify-Code'),
    path('user-profile', UserProfileAPIView.as_view(), name='User Profile'),
    path('referral', ReferralAPIView.as_view(), name='Referral'),

]
