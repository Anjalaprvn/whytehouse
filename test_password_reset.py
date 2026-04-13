"""
Test script to verify password reset flow
Run with: python manage.py shell < test_password_reset.py
"""
from django.test import Client
from django.contrib.auth.models import User

# Create a test client
client = Client()

# Check if test user exists, create if not
email = "test@example.com"
try:
    user = User.objects.get(email=email)
    print(f"✓ Test user exists: {email}")
except User.DoesNotExist:
    user = User.objects.create_user(
        username="testuser",
        email=email,
        password="testpass123"
    )
    print(f"✓ Created test user: {email}")

# Test 1: Access forgot password page
response = client.get('/forgot-password/')
print(f"\n1. Forgot Password Page: {response.status_code} (expected 200)")

# Test 2: Submit email to get OTP
response = client.post('/forgot-password/', {'email': email})
print(f"2. Submit Email: {response.status_code} (expected 302 redirect)")

# Test 3: Access verify OTP page
response = client.get('/verify-reset-otp/')
print(f"3. Verify OTP Page: {response.status_code} (expected 200)")

# Get OTP from session
session = client.session
otp = session.get('reset_otp')
print(f"4. OTP in session: {otp}")

# Test 4: Submit OTP
if otp:
    response = client.post('/verify-reset-otp/', {'otp': otp})
    print(f"5. Submit OTP: {response.status_code} (expected 302 redirect)")
    
    # Test 5: Access reset password page
    response = client.get('/reset-password/')
    print(f"6. Reset Password Page: {response.status_code} (expected 200)")
    
    # Test 6: Submit new password
    response = client.post('/reset-password/', {
        'new_password': 'newpass123',
        'confirm_password': 'newpass123'
    })
    print(f"7. Submit New Password: {response.status_code} (expected 302 redirect)")
    
    # Test 7: Verify password was changed
    user.refresh_from_db()
    if user.check_password('newpass123'):
        print("✓ Password successfully changed!")
    else:
        print("✗ Password change failed")
else:
    print("✗ No OTP in session - email sending might have failed")

print("\nTest complete!")
