from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.http import JsonResponse
from user_profile.models import Profile
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_date
from django.utils import timezone

# For Profiles:
@csrf_exempt
@require_http_methods(["POST"])
def create_profile(request):
    try:
        data = json.loads(request.body)

        # Validation (simplified example)
        if 'user_token' not in data or 'login_token' not in data:
            return JsonResponse({
                "status" : False,
                "error": "Validation error",
                "details": {
                    "user_token": ["This field is required."] if 'user_token' not in data else [],
                    "login_token": ["This field is required."] if 'login_token' not in data else []
                }
            }, status=422)



        # Validation
        # missing_fields = []
        # if 'user_token' not in data or not data['user_token'].strip():
        #     missing_fields.append('user_token')
        # if 'name' not in data or not data['name'].strip():
        #     missing_fields.append('name')
        # if 'd_o_b' not in data:
        #     missing_fields.append('d_o_b')
        # if 'nick_name' not in data or not data['nick_name'].strip():
        #     missing_fields.append('nick_name')
        # if 'image_url' not in data or not data['image_url'].strip():
        #     missing_fields.append('image_url')

        # if missing_fields:
        #     return JsonResponse({
        #         "status": False,
        #         "error": "Validation error",
        #         "details": {field: ["This field is required."] for field in missing_fields}
        #     }, status=422)

        # Parse date of birth
        d_o_b = parse_date(data['d_o_b'])
        if not d_o_b:
            return JsonResponse({
                "status": False,
                "error": "Validation error",
                "details": {"d_o_b": ["Invalid date format."]}
            }, status=422)

        profile = Profile(
            user_token=data['user_token'],
            login_token=data['login_token'],
            name=data['name'],
            d_o_b=d_o_b,
            nick_name=data['nick_name'],
            image_url=data['image_url'],
            soft_delete=data.get('soft_delete', False),
            status=data.get('status', False),
            created_at=parse_datetime(data.get('created_at', timezone.now().isoformat())),
            updated_at=parse_datetime(data.get('updated_at', timezone.now().isoformat()))
        )
        profile.save()

        response_data = {
            "id": profile.id,
            "user_token": profile.user_token,
            "login_token":profile.login_token,
            "name": profile.name,
            "d_o_b": profile.d_o_b.isoformat(),
            "nick_name": profile.nick_name,
            "image_url": profile.image_url,
            "soft_delete": profile.soft_delete,
            "status": profile.status,
            "created_at": profile.created_at.isoformat(),
            "updated_at": profile.updated_at.isoformat()
        }
        return JsonResponse({
            'status': True,
            'data': response_data
        }, status=201)
        # return JsonResponse(response_data, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            "status": False,
            "error": "Invalid request data",
            "details": "Request body is not valid JSON."
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "status": False,
            "error": "Internal Server Error",
            "details": str(e)
        }, status=500)

