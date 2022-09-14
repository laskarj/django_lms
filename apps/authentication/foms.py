from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings

from apps.authentication.models import ActivationToken

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name']

    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label=_('Repeat password'))

    def clean_password2(self):
        if not self.data['password2'] == self.data['password']:
            raise forms.ValidationError(_('Password mismatch'))

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.is_active = False
            user.set_password(self.data['password'])
            user.save()
            activation_token = ActivationToken.objects.create(user=user)
            message_context = {
                'user': user,
                'activation_token': activation_token,
                'site_url': settings.SITE_URL,
            }
            text = render_to_string('email/registration/user_activation.txt', context=message_context)
            html = render_to_string('email/registration/user_activation.html', context=message_context)
            mail = EmailMultiAlternatives(
                subject='Please activate your account',
                body=text,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            mail.attach_alternative(html, "text/html")
            mail.send()
        return user


"""activation_token = ActivationToken.objects.create(user=user)
            message_context = {
                'user': user,
                'activation_token': activation_token,
                'site_url': settings.SITE_URL
            }

            text = render_to_string('email/registration/user_activation.txt', context=message_context)
            html = render_to_string('email/registration/user_activation.html', context=message_context)
            mail = EmailMultiAlternatives(
                'Activate your account please.',
                text,
                to=[user.email]
            )
            mail.attach_alternative(html, "text/html")
mail.send()"""

