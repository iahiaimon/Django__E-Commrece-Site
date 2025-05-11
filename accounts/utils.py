from django.conf import settings
from django.core.mail import send_mail , EmailMessage
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string


# ✅ 1. Function to send the email verification link
def send_verification_email(request, user):
    # Encode the user ID to base64 to safely include it in the URL
    uid = urlsafe_base64_encode(force_bytes(user.id))
    
    # Generate a unique token for the user using Django's built-in token generator
    token = default_token_generator.make_token(user)

    # Get the current site (e.g., example.com)
    current_site = get_current_site(request)

    # Build a full URL to the verification view using uid and token
    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )

    # Define the email content
    subject = 'Verify your email'
    message = render_to_string('emails/verify_email.html', {
        'user': user,
        'verification_link': verification_link,
    })

    # Send the email
    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = 'html'  # Mark the email as HTML
    email.send()


# ✅ 2. (Optional) Custom token generator class
# If you want a custom generator (instead of default_token_generator), define this:

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Token is based on user ID, time, and is_verified flag
        return str(user.pk) + str(timestamp) + str(user.is_verified)

# You could then use this instead of default_token_generator:
# token = account_activation_token.make_token(user)
account_activation_token = EmailVerificationTokenGenerator()
 



# Using Console


