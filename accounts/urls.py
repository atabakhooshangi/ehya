from django.urls import path
from .views import RegisterLoginAPIView , VerifyAuthenticationCodeAPIView,UserProfileAPIView,ReferralAPIView

app_name = 'Accounts'

urlpatterns = [
    path('register_login', RegisterLoginAPIView.as_view(), name='Register-Login'),
    path('verify_code', VerifyAuthenticationCodeAPIView.as_view(), name='Verify-Code'),
    path('user_profile', UserProfileAPIView.as_view(), name='User Profile'),
    path('referral', ReferralAPIView.as_view(), name='Referral'),

]
