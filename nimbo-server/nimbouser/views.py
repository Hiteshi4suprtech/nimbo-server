
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.views.decorators.http import require_http_methods # type: ignore
from django.http import JsonResponse # type: ignore
from nimbo.settings import SERVICE_ACCOUNT_KEY
from validate_email import validate_email # type: ignore
from nib.models import nimbo_users, otp_verify
from django.utils.dateparse import parse_datetime # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from django.core.mail import send_mail # type: ignore
from datetime import datetime # type: ignore
from django.conf import settings # type: ignore
import random
from django.core.serializers import serialize # type: ignore
from django.views.decorators.http import require_http_methods
import json
from django.http import JsonResponse # type: ignore
import firebase_admin # type: ignore
from firebase_admin import auth # type: ignore
from django.forms.models import model_to_dict
import base64
import os
# from nib.models import nimbo_users
# from nib.nimbo_users import email_exists



@csrf_exempt
@require_http_methods(["POST"])
def request_otp(request):
    try:
        email = request.POST.get('email')
        # print(email)
        otp_type = request.POST.get('otp_type')
        # print(otp_type)
        request_errors = {}
        # Validate fields
        if not email:
            request_errors['email'] = "Please provide an email address"
        
        if not validate_email(email):
            request_errors['email'] = "Please enter a valid email address"
        
        if not otp_type:
             request_errors['otp_type'] = "Please enter a valid otp type"
             
        if otp_type == 'reset_password':
            if not nimbo_users.email_exists(nimbo_users, email):
                request_errors['email'] = "Account does not exist"

        # Check if email is provided
        if not email:
            request_errors['email'] = "Email is required"
        else:
            # Check if the otp_type is 'set_password' and email exists
            if otp_type == 'set_password':
                if nimbo_users.email_exists(nimbo_users, email):
                    request_errors['email'] = "Account already exists. Please login to your account."

        # if otp_type == 'set_password':
        #     if nimbo_users.email_exists(email):
        #         request_errors['email'] = "Account already exist Please login your account"
                  
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : request_errors
        })

        
        # Generate OTP
        random_number = random.randint(1000, 9999)
       
        # Send email
        subject = 'Test OTP'
        message = 'This new  OTP:' + str(random_number) + "."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        otp_verify.delete_otp(otp_verify, email, otp_type)
        # Save OTP record
        otp_record = otp_verify(
            email=email,
            otp=random_number,
            otp_type=otp_type,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        otp_record.save()

        return JsonResponse({
            'status': True,
            'message': 'Please check your email address for OTP'
        })

    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def verify_otp(request):
    try:
        email = request.POST.get('email')
        otp_type = request.POST.get('otp_type')
        otp = request.POST.get('otp')
        request_errors = {}
        
        request_errors = {}
        # Validate fields
        if not email:
            request_errors['email'] = "Please provide an email address"
        
        if not validate_email(email):
            request_errors['email'] = "Please enter a valid email address"
        
        if not otp_type:
             request_errors['otp_type'] = "Please enter a valid otp type"
             
        if not otp:
             request_errors['otp'] = "Please enter a opt"
             
       
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : request_errors
        })
        
        otp_record = otp_verify.check_otp(otp_verify, email, otp_type, otp)
        
        if otp_record:
            # Convert the object to a dictionary
            return JsonResponse({
                'status': True
            })
        else:
             return JsonResponse({
                'status': False,
                'message': 'Otp Not Matched'
            })

    except Exception as e:
        return JsonResponse({'status': False, 'try': str(e)}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    try:
        uid = request.POST.get('user_token')
        nick_name = request.POST.get('nick_name')
        d_o_b = request.POST.get('d_o_b')
        # user = auth.get_user(uid)

        if not uid:
            return JsonResponse({'status': 'Error', 'message': 'User Token is required'}, status=400)
        if not nick_name:
            return JsonResponse({'status': 'Error', 'message': 'Nick Name is required'}, status=400)
        if not d_o_b:
            return JsonResponse({'status': 'Error', 'message': 'Date of Birth is required'}, status=400)
        
        # Get the base64 image data from request
        base64_image = request.POST.get('image_url', None)
        if base64_image:
            # Extract base64 part from the data URL
            header, base64_image = base64_image.split(',', 1)
            # Decode the base64 image
            image_data = base64.b64decode(base64_image)
            # Create the file path
            image_name = int(datetime.now().timestamp())
            file_path = os.path.join(settings.MEDIA_ROOT, 'images/users', f'{image_name}.png')
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # Write the image data to a file
            with open(file_path, 'wb') as f:
                f.write(image_data)
            image_url = f'{image_name}.png'
        else:
            image_url = None
        
        nimbo_user = nimbo_users.objects.update_or_create(user_token=uid, defaults = {
            "name" : request.POST.get('name', None),
            "d_o_b" : request.POST.get('d_o_b', None),
            "nick_name" : request.POST.get('nick_name', None),
            "image_url" :image_url,
        })
       # nimbo_user_dict = model_to_dict(nimbo_user)
        return JsonResponse({'status': 'True', 'message': "User Update Profile Successfully"})     
        
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)

