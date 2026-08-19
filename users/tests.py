from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from full_auth import settings as project_settings
from .authentication import CustomJWTAuthentication


class CustomJWTAuthenticationTests(TestCase):
    def test_authenticate_uses_access_cookie_when_no_authorization_header(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='strongpass123',
            is_active=True,
        )

        token = str(AccessToken.for_user(user))
        factory = APIRequestFactory()
        request = factory.get('/api/users/me/')
        request.COOKIES['access'] = token

        authenticated_user, authenticated_token = CustomJWTAuthentication().authenticate(request)

        self.assertEqual(authenticated_user, user)
        self.assertEqual(str(authenticated_token), token)

    @override_settings(DEBUG=True)
    def test_cookie_defaults_are_browser_compatible_in_development(self):
        cookie_settings = project_settings.get_cookie_settings()

        self.assertFalse(cookie_settings['secure'])
        self.assertEqual(cookie_settings['samesite'], 'Lax')
