from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.views.decorators.http import require_http_methods # type: ignore
import json
from django.http import JsonResponse # type: ignore
from django.utils.dateparse import parse_datetime # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from django.core.serializers.json import DjangoJSONEncoder # type: ignore

from nib.models import nimbo_users, health_goal
import traceback
# from nimbo.settings import SERVICE_ACCOUNT_KEY
# import firebase_admin # type: ignore
from firebase_admin import auth # type: ignore
# from firebase_admin import credentials # type: ignore

# # Firebase Admin SDK initialization
# cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
# firebase_admin.initialize_app(cred)


# For Health Goals Correct Code:
@csrf_exempt
@require_http_methods(["POST"])
def create_health_goal(request):
    try:
        user_token = request.POST.get('user_token')
        # login_token = request.POST.get('login_token')
        goal_id = request.POST.get('goal_id')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide login token"
        if not goal_id:
            request_errors['goal_id'] = "Please provide goal"
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : request_errors
        })
            
        user_token = request.POST.get('user_token')
        try:
            user = auth.get_user(user_token)
            save_user = {
                'user_token': user.uid,
                'email': user.email,
                'phone_number': user.phone_number,
                'display_name': user.display_name,
                'photo_url': user.photo_url,
                'email_verified': user.email_verified,
                'custom_claims': user.custom_claims,
                'provider_id': user.provider_id,
            }
            
            NIMBO_USERS = nimbo_users()
            if nimbo_users.objects.filter(user_token=user_token).count() == 0:
                NIMBO_USERS.save_user(user.uid, user.display_name, user.email, None, None, user.photo_url, save_user)
            
        except auth.UserNotFoundError:
            return JsonResponse({
                'status' : False,
                'errors' : {'user_token' : "No user found."}
        }   )
       
        # Save Health Goal Record:
        if health_goal.goal_exists(health_goal, user_token):
            health_goal_row = health_goal.objects.get(user_token=user_token)
            health_goal_row.goal_id = goal_id
            health_goal_row.save()
        else:
            health_goal_row = health_goal(
                user_token=user_token,
                goal_id=goal_id
            )
            health_goal_row.save()

        return JsonResponse({
            'status': True,
            'message': 'Health goal added successfully'
        })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)











