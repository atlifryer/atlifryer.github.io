from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.http import HttpResponse

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def send_test_email(request):
    send_mail(
        'Test Email',
        'This is a test email sent from Django.',
        'atlifreyr666@gmail.com',
        ['recipient@example.com'],
        fail_silently=False,
    )
    return HttpResponse('Email sent!')