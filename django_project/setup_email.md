# Email Setup Guide for Tecosoft

## Option 1: Gmail SMTP (Recommended for testing)

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Enable 2-Factor Authentication if not already enabled

### Step 2: Generate App Password
1. Go to Google Account → Security → 2-Step Verification
2. Scroll down to "App passwords"
3. Select "Mail" and "Other (Custom name)"
4. Enter "Tecosoft Django" as the name
5. Copy the generated 16-character password

### Step 3: Update Django Settings
In `mysite/settings.py`, replace these values:

```python
EMAIL_HOST_USER = 'your-actual-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-character-app-password'
DEFAULT_FROM_EMAIL = 'Tecosoft <your-actual-email@gmail.com>'
```

And in the contact view, replace:
```python
['admin@tecosoft.com']  # Replace with your actual email
```

### Step 4: Test Email
1. Fill out the contact form on your website
2. Check your Gmail inbox for the notification
3. Check if the user receives a confirmation email

## Option 2: Alternative Email Services

### SendGrid (Production recommended)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

### Outlook/Hotmail
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## Testing Email Functionality

### Test Script
Create a test file to verify email setup:

```python
# test_email.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

try:
    send_mail(
        'Test Email from Tecosoft',
        'This is a test email to verify email configuration.',
        settings.DEFAULT_FROM_EMAIL,
        ['your-email@gmail.com'],  # Replace with your email
        fail_silently=False,
    )
    print("✓ Email sent successfully!")
except Exception as e:
    print(f"✗ Email failed: {e}")
```

Run with: `python test_email.py`

## Security Notes

1. **Never commit passwords to Git**
2. **Use environment variables for production**
3. **Consider using email services like SendGrid for production**
4. **Enable rate limiting for contact forms**

## Troubleshooting

### Common Issues:
1. **"Authentication failed"** - Check app password
2. **"Connection refused"** - Check firewall/network
3. **"Emails not received"** - Check spam folder
4. **"SSL errors"** - Verify EMAIL_USE_TLS = True

### Debug Mode:
To see detailed email errors, temporarily add to settings:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```