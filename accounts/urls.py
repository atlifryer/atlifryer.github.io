from django.urls import path
from .views import SignUpView, send_test_email

urlpatterns = [
    path('send-test-email/', send_test_email, name='send_test_email'),
    path("signup/", SignUpView.as_view(), name="signup"),
]