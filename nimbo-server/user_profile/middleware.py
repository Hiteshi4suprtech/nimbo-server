# For testing Purpose manually access_token = 'i4consulting'
import os
import json
from django.http import JsonResponse
from user_profile.models import Profile
import firebase_admin
from django.conf import settings
from firebase_admin import auth, initialize_app, credentials

# Absolute path to the JSON file
FIREBASE_CREDENTIALS_PATH = os.path.join(settings.BASE_DIR, 'nimbo-health-dev-firebase-adminsdk-ezqe2-ca0ac754b1.json')

# Ensure Firebase is initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    initialize_app(cred)

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token_validators = {
            '/api/profiles/': self.validate_tokens,
            '/api/add-user/': self.validate_tokens,
        }

    def __call__(self, request):
        path = request.path

        if path in self.token_validators:
            return self.token_validators[path](request)

        # Continue processing other middleware and view
        response = self.get_response(request)
        return response

    def validate_tokens(self, request):
        try:
            if request.method == 'POST':
                # Determine content type and load data accordingly
                if request.content_type == 'application/json':
                    data = json.loads(request.body)
                else:
                    data = request.POST

                # Initialize error dictionary
                error_dict = {}

                # Check for user_token or login_token authentication
                if 'user_token' in data:
                    user_token = data['user_token']
                    if not self.authenticate_user_token(user_token):
                        error_dict["user_token"] = "Invalid user_token"

                if 'login_token' in data:
                    login_token = data['login_token']
                    if not self.authenticate_login_token(login_token):
                        error_dict["login_token"] = "Invalid login_token"

                # Check for auth_key authentication from headers (Bearer token)
                auth_key = request.headers.get('Authorization')
                if not auth_key or not auth_key.startswith('Bearer '):
                    error_dict["Authorization"] = "Invalid or missing access token"
                else:
                    # Extract the token from the 'Authorization' header
                    access_token = auth_key.split('Bearer ')[1].strip()

                    # Check if the token is the hardcoded testing token
                    if access_token == 'i4consulting':
                        request.user = {'user_id': 'test_user'}
                    else:
                        # Validate the access token using Firebase Admin SDK
                        is_valid, error_message = self.authenticate_access_token(access_token)
                        if not is_valid:
                            error_dict["Authorization"] = error_message

                if error_dict:
                    response_data = {
                        "status": False,
                        "error": [error_dict]
                    }
                    return JsonResponse(response_data, status=401)  # Unauthorized

        except json.JSONDecodeError:
            response_data = {
                "status": False,
                "error": {"request": "Invalid request data"},
                "details": ["Request body is not valid JSON."]
            }
            return JsonResponse(response_data, status=400)  # Bad Request

        # Continue processing other middleware and view
        response = self.get_response(request)
        return response

    def authenticate_user_token(self, user_token):
        # Implement user_token authentication logic (example)
        return Profile.objects.filter(user_token=user_token).exists()

    def authenticate_login_token(self, login_token):
        # Implement login_token authentication logic (example)
        return Profile.objects.filter(login_token=login_token).exists()

    def authenticate_access_token(self, access_token):
        # Implement access_token authentication logic using Firebase Admin SDK
        try:
            decoded_token = auth.verify_id_token(access_token)
            # Optionally, you can retrieve user details or perform additional checks here
            return True, None  # Token is valid
        except auth.InvalidIdTokenError:
            return False, "Invalid access token"
        except auth.ExpiredIdTokenError:
            return False, "Access token has expired"
        except auth.RevokedIdTokenError:
            return False, "Access token has been revoked"
        except Exception as e:
            return False, str(e)



# Correct code for Dynamic access_token:
# import json
# from django.http import JsonResponse
# from user_profile.models import Profile

# class TokenAuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.token_validators = {
#             '/api/profiles/': self.validate_tokens,
#         }

#     def __call__(self, request):
#         path = request.path

#         if path in self.token_validators:
#             return self.token_validators[path](request)

#         # Continue processing other middleware and view
#         response = self.get_response(request)
#         return response

#     def validate_tokens(self, request):
#         try:
#             if request.method == 'POST':
#                 # Determine content type and load data accordingly
#                 if request.content_type == 'application/json':
#                     data = json.loads(request.body)
#                 else:
#                     data = request.POST

#                 # Initialize error dictionary
#                 error_dict = {}

#                 # Check for user_token or login_token authentication
#                 if 'user_token' in data:
#                     user_token = data['user_token']
#                     if not self.authenticate_user_token(user_token):
#                         error_dict["user_token"] = "Invalid user_token"

#                 if 'login_token' in data:
#                     login_token = data['login_token']
#                     if not self.authenticate_login_token(login_token):
#                         error_dict["login_token"] = "Invalid login_token"

#                 # Check for auth_key authentication from headers
#                 auth_key = request.headers.get('Authorization')
#                 if not auth_key:
#                     error_dict["Authorization"] = "auth_key is missing in headers"
#                 else:
#                     # Extract the token from the 'Authorization' header (Bearer token)
#                     if auth_key.startswith('Bearer '):
#                         auth_key = auth_key.split('Bearer ')[1].strip()

#                     if not self.authenticate_access_token(auth_key):
#                         error_dict["Authorization"] = "Invalid access token"

#                 if error_dict:
#                     response_data = {
#                         "status": False,
#                         "error": [error_dict]
#                     }
#                     return JsonResponse(response_data, status=401, safe=False)  # Unauthorized

#         except json.JSONDecodeError:
#             response_data = {
#                 "status": False,
#                 "error": [{"request": "Invalid request data"}],
#                 "details": ["Request body is not valid JSON."]
#             }
#             return JsonResponse(response_data, status=400, safe=False)  # Bad Request

#         # Continue processing other middleware and view
#         response = self.get_response(request)
#         return response

#     def authenticate_user_token(self, user_token):
#         # Implement user_token authentication logic
#         return Profile.objects.filter(user_token=user_token).exists()

#     def authenticate_login_token(self, login_token):
#         # Implement login_token authentication logic
#         # return False  # Replace with actual implementation
#         return Profile.objects.filter(login_token=login_token).exists()

#     def authenticate_access_token(self, access_token):
#         # Implement access_token authentication logic (from header)
#         try:
#             token = access_token.objects.get(token=access_token)
#             if token.is_valid():
#                 return True, None
#         except access_token.DoesNotExist:
#             return False, 'unauthorized_error'
#         except ValueError:
#             return False, 'key_value_error'  # Handle ValueError
#         except Exception as e:
#             # Handle other exceptions (excluding RequestException)
#             return False, 'other_error'
#         return False, 'unauthorized_error'
    
# Correct code for Dynamic access_token:

# class TokenAuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.token_validators = {
#             '/api/profiles/': self.validate_tokens,
#         }

#     def __call__(self, request):
#         path = request.path

#         if path in self.token_validators:
#             return self.token_validators[path](request)

#         # Continue processing other middleware and view
#         response = self.get_response(request)
#         return response

#     def validate_tokens(self, request):
#         # Check for user_token or login_token authentication
#         if 'user_token' in request.POST:
#             user_token = request.POST['user_token']
#             if not self.authenticate_user_token(user_token):
#                 return JsonResponse({
#                     "status": False,
#                     "error": "Authentication error",
#                     "details": "Invalid user_token."
#                 }, status=401)  # Unauthorized

#         if 'login_token' in request.POST:
#             login_token = request.POST['login_token']
#             if not self.authenticate_login_token(login_token):
#                 return JsonResponse({
#                     "status": False,
#                     "error": "Authentication error",
#                     "details": "Invalid login_token."
#                 }, status=401)  # Unauthorized

#         # Check for access_token authentication from headers
#         access_token = request.headers.get('Authorization')
#         if not access_token:
#             return JsonResponse({
#                 "status": False,
#                 "error": "Authentication error",
#                 "details": "Access token is missing in headers."
#             }, status=401)  # Unauthorized

#         # Extract the token from the 'Authorization' header (Bearer token)
#         if not self.authenticate_access_token(access_token):
#             return JsonResponse({
#                 "status": False,
#                 "error": "Authentication error",
#                 "details": "Invalid access token."
#             }, status=401)  # Unauthorized

#         # Continue processing other middleware and view
#         response = self.get_response(request)
#         return response

#     def authenticate_user_token(self, user_token):
#         # Implement user_token authentication logic
#         return Profile.objects.filter(user_token=user_token).exists()

#     def authenticate_login_token(self, login_token):
#         # Implement login_token authentication logic
#         return False  # Example implementation

#     def authenticate_access_token(self, access_token):
#         # Implement access_token authentication logic (from header)
#         if access_token.startswith('Bearer '):
#             access_token = access_token.split('Bearer ')[1].strip()

#         # Example:
#         # return AccessToken.objects.filter(token=access_token).exists()
#         return False  # Example implementation