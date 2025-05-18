from django.conf import settings
from django.core.mail import send_mail , EmailMessage
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_verified)

account_activation_token = EmailVerificationTokenGenerator()
 
# Function to send the email verification link

def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)

    current_site = get_current_site(request)

    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Verify your email'
    message = render_to_string('verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })

    from_email = settings.EMAIL_HOST_USER 
    
    # print("Sending email to:", user.email)
    # print("From:", settings.DEFAULT_FROM_EMAIL)
    # Send the email
    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'
    try:
        email.send()
        print("Email sent successfully.")
    except Exception as e:
        print("Email failed:", e)



