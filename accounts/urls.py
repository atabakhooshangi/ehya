from django.urls import path
from .views import RegisterLoginAPIView, VerifyAuthenticationCodeAPIView, UserProfileAPIView, ReferralAPIView, \
    GetRolesAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'Accounts'

urlpatterns = [
    path('register_login', RegisterLoginAPIView.as_view(), name='Register-Login'),
    path('verify_code', VerifyAuthenticationCodeAPIView.as_view(), name='Verify-Code'),
    path('refresh_token', TokenRefreshView.as_view(), name='Refresh-Token'),
    path('user_profile', UserProfileAPIView.as_view(), name='User Profile'),
    path('referral', ReferralAPIView.as_view(), name='Referral'),
    path('roles', GetRolesAPIView.as_view(), name='Roles'),

]
