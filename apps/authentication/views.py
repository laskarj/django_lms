from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, CreateView, TemplateView
from django.urls import reverse_lazy
from apps.authentication.models import ActivationToken
from apps.authentication.foms import RegistrationForm

User = get_user_model


class RegisterView(CreateView):
    model = User
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('authentication:registration-success')

    def get_form_class(self):
        return RegistrationForm


class RegisterSuccessView(TemplateView):
    template_name = 'registration/registration-success.html'


class RegisterActivateEmailView(TemplateView):
    template_name = 'registration/registration-activate.html'

    def get_context_data(self, **kwargs):
        token = self.kwargs.get('token')
        activation_token = get_object_or_404(ActivationToken, token=token)
        activation_token.user.is_active = True
        activation_token.user.save()
        activation_token.delete()
