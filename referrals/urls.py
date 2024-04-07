from django.urls import path
from .views import user_registration, user_details, user_referrals

urlpatterns = [
    path('register/', user_registration),
    path('details/', user_details),
    path('referrals/', user_referrals),
]
