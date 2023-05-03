from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def send_verification_email(request,user):
    pass
    from_email = settings.DEFAULT_FORM_EMAIL
    current_site = get_current_site(request)
    mail_subject = 'Please activate your account'
    message = render_to_string(
        'email/account_verification_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
    to_email = user.email
    mail = EmailMessage(mail_subject, message,from_email, to=[to_email])
    mail.send()


def send_password_reset_email(request,user):
    from_email = settings.DEFAULT_FORM_EMAIL
    current_site = get_current_site(request)
    mail_subject = 'Reset Your Password'
    message = render_to_string(
        'email/reset_password_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
    to_email = user.email
    mail = EmailMessage(mail_subject, message,from_email, to=[to_email])
    mail.send()
