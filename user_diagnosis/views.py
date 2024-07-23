from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.views.decorators.http import require_http_methods # type: ignore
import json
from django.http import JsonResponse # type: ignore
from django.utils.dateparse import parse_datetime # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from nib.models import nimbo_users, diagonsis,user_diagonsis
import traceback


# For Health Goals Correct Code:
@csrf_exempt
@require_http_methods(["POST"])
def create_diagnosis(request):
    try:
        user_token = request.POST.get('user_token')
        title = request.POST.get('title')
        request_errors = {}
        
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        if not title:
            request_errors['title'] = "Please provide diagnosis title"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
    
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            })
        
        # Check if the diagnosis already exists for any user
        existing_diagnosis = diagonsis.objects.filter(title=title).first()
        if existing_diagnosis:
            # Check if the diagnosis already exists for the current user
            diagnosis_for_user = user_diagonsis.objects.filter(user_token=user_token, diagnosis=existing_diagnosis).first()
            if diagnosis_for_user:
                message = "Diagnosis already exists for this user."
            else:
                # Assign the existing diagnosis to the current user
                user_diagonsis.objects.create(
                    user_token=user_token,
                    diagnosis=existing_diagnosis
                )
                message = "Diagnosis assigned to current user."
        else:
            # Save new diagnosis record
            diagnosis = diagonsis.objects.create(
                user_token=user_token,
                title=title
            )
            user_diagonsis.objects.create(
                user_token=user_token,
                diagnosis=diagnosis
            )
            message = "Diagnosis created successfully"
        
        # Retrieve current user's diagnoses
        user_diagnoses = user_diagonsis.objects.filter(user_token=user_token).select_related('diagnosis')
        diagnosis_list = [
            {
                'id': ud.diagnosis.id,
                'title': ud.diagnosis.title,
                'created_at': ud.diagnosis.created_at,
                'updated_at': ud.diagnosis.updated_at,
                'status': ud.diagnosis.status,
            } for ud in user_diagnoses
        ]
        response = {
            'status': True,
            'diagnosis_list': diagnosis_list,
            # 'diagnosis_list': 
        }
        return JsonResponse(response, status=201)
        
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)
    
# For selecting existing diagnosis for new user:
@csrf_exempt
@require_http_methods(["POST"])
def select_diagnosis_by_new_user(request):
    try:
        user_token = request.POST.get('user_token')
        diagnosis_id = request.POST.get('diagnosis_id')
        request_errors = {}
        
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        if not diagnosis_id:
            request_errors['diagnosis_id'] = "Please provide diagnosis ID"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            })
                # Retrieve the diagnosis based on diagnosis_id
        try:
            diagnosis = diagonsis.objects.get(id=diagnosis_id)
        except diagonsis.DoesNotExist:
            return JsonResponse({
                'status': False,
                'errors': {'diagnosis_id': "Diagnosis with this ID does not exist"}
            })
        
        # Check if the diagnosis already exists for the current user
        if user_diagonsis.objects.filter(user_token=user_token, diagnosis=diagnosis).exists():
            message = "Diagnosis already exists for this user."
        else:
            # Save the diagnosis for the current user
            user_diagnosis = user_diagonsis.objects.create(user_token=user_token, diagnosis=diagnosis)
            message = "Diagnosis added to current user."

        
        # Fetch updated diagnosis list for the user
        user_diagnoses = user_diagonsis.objects.filter(user_token=user_token).select_related('diagnosis')
        diagnosis_list = [{'id': ud.diagnosis.id, 'title': ud.diagnosis.title} for ud in user_diagnoses]

        response = {
            'status': True,
            'message': message,
            'diagnosis_list': diagnosis_list,
        }
        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def diagnosis_list(request):
    try:
        user_token = request.POST.get('user_token')
        # login_token = request.POST.get('login_token')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        # if not login_token:
        #     request_errors['login_token'] = "Please provide login token"
       
        if nimbo_users.check_user_token(nimbo_users):
            request_errors['user_token'] = "User is not valid"
    
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : [request_errors]
        })
        # Save OTP record
        # # Fetch updated diagnosis list for the user
        # user_diagnoses = user_diagonsis.objects.filter(user_token=user_token).select_related('diagnosis')
        # diagnosis_list = [{'id': ud.diagnosis.id, 'title': ud.diagnosis.title} for ud in user_diagnoses]

        # response = {
        #     'status': True,
        #     'message': 'added successful',
        #     'diagnosis_list': diagnosis_list,
        # }
        # return JsonResponse(response, status=201)
        diagonsis_row = diagonsis.get_list(diagonsis, user_token, request.POST.get('query_string'))

        return JsonResponse({
            'status': True,
            'message': list(diagonsis_row.values())
        })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)

# Get Diagnosis List for Particular User:
@csrf_exempt
@require_http_methods(["POST"])
def get_diagnosis_list_by_user(request):
    try:
        user_token = request.POST.get('user_token')
        # login_token = request.POST.get('login_token')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        # if not login_token:
        #     request_errors['login_token'] = "Please provide login token"
       
        if nimbo_users.check_user_token(nimbo_users):
            request_errors['user_token'] = "User is not valid"
    
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : [request_errors]
        })
        # Save OTP record
        # Fetch updated diagnosis list for the user
        user_diagnoses = user_diagonsis.objects.filter(user_token=user_token).select_related('diagnosis')
        diagnosis_list = [{'id': ud.diagnosis.id, 'title': ud.diagnosis.title} for ud in user_diagnoses]

        response = {
            'status': True,
            'message': 'Added Successfully',
            'diagnosis_list': diagnosis_list,
        }
        return JsonResponse(response, status=201)
        # diagonsis_row = diagonsis.get_list_by_user(diagonsis, user_token)

        # return JsonResponse({
        #     'status': True,
        #     'diagnosis_list': list(diagonsis_row.values())
        # })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)


# Delete Diagnosis from Main And User Tables:
@csrf_exempt
@require_http_methods(["POST"])
def delete_diagnosis_list_by_user(request):
    try:
        user_token = request.POST.get('user_token')
        diagnosis_id = request.POST.get('diagnosis_id')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
       
        if nimbo_users.check_user_token(nimbo_users):
            request_errors['user_token'] = "User is not valid"
    
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : [request_errors]
        })
        # Save Diagnosis record:
        deleted_diagonsis = diagonsis.soft_delete_by_user(diagnosis_id, user_token)
        user_diagnosis_record = user_diagonsis.objects.get(user_token=user_token, diagnosis_id=diagnosis_id)
        user_diagnosis_record.delete()
        user_diagnoses = user_diagonsis.objects.filter(user_token=user_token).select_related('diagnosis')
        diagnosis_list = [{'id': ud.diagnosis.id, 'title': ud.diagnosis.title, 'soft_delete': ud.diagnosis.soft_delete} for ud in user_diagnoses]
        print(diagnosis_list)
     
        if deleted_diagonsis and user_diagnosis_record:
            return JsonResponse({
                'status': True,
                'message': "Diagnosis soft-deleted and user-diagnosis successfully",
                'diagnosis_list':diagnosis_list
                 })
        else:
            return JsonResponse({
                'status': True,
                'message': "Diagnosis not found or already soft deleted",
                'diagnosis_list':diagnosis_list
            })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)





