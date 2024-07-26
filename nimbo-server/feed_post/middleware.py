# For Testing Purpose:
import json
from django.http import JsonResponse
from health_goals.models import HealthGoal

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token_validators = {
            '/api/health-goals/': self.validate_tokens,
        }

    def __call__(self, request):
        path = request.path

        if path in self.token_validators:
            return self.token_validators[path](request)

        # Continue processing other middleware and view
        response = self.get_response(request)
        return response

    def validate_tokens(self, request):
        # Check for user_token or login_token authentication
        if 'user_token' in request.POST:
            user_token = request.POST['user_token']
            if not self.authenticate_user_token(user_token):
                return JsonResponse({
                    "status": False,
                    "error": "Authentication error",
                    "details": "Invalid user_token."
                }, status=401)  # Unauthorized

        if 'login_token' in request.POST:
            login_token = request.POST['login_token']
            if not self.authenticate_login_token(login_token):
                return JsonResponse({
                    "status": False,
                    "error": "Authentication error",
                    "details": "Invalid login_token."
                }, status=401)  # Unauthorized

        # Check for access_token authentication from headers
        access_token = request.headers.get('Authorization')
        if not access_token:
            return JsonResponse({
                "status": False,
                "error": "Authentication error",
                "details": "Access token is missing in headers."
            }, status=401)  # Unauthorized

        # Extract the token from the 'Authorization' header (Bearer token)
        if not self.authenticate_access_token(access_token):
            return JsonResponse({
                "status": False,
                "error": "Authentication error",
                "details": "Invalid access token."
            }, status=401)  # Unauthorized

        # Continue processing other middleware and view
        response = self.get_response(request)
        return response

    def authenticate_user_token(self, user_token):
        # Implement user_token authentication logic
        return HealthGoal.objects.filter(user_token=user_token).exists()

    def authenticate_login_token(self, login_token):
        # Implement login_token authentication logic
        return False  # Example implementation

    def authenticate_access_token(self, access_token):
        # Implement access_token authentication logic (from header)
        if access_token.startswith('Bearer '):
            access_token = access_token.split('Bearer ')[1].strip()

        # Example:
        # return AccessToken.objects.filter(token=access_token).exists()
        return False  # Example implementation