import base64
from datetime import datetime
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.views.decorators.http import require_http_methods # type: ignore
import json
from django.http import JsonResponse # type: ignore
from django.utils.dateparse import parse_datetime # type: ignore
from django.core.exceptions import ValidationError # type: ignore

from nib.models import nimbo_users, feed_post,post
import traceback
from uuid import uuid4
from django.utils import timezone


# # For Creating Post:
@csrf_exempt
@require_http_methods(["POST"])
def create_post(request):
    try:
        user_token = request.POST.get('user_token')
        media_type = request.POST.get('media_type')
        private_post = request.POST.get('private_post', 'false').lower() == 'true'
        post_description = request.POST.get('post_description')
        status = request.POST.get('status', False)
        post_video = request.FILES.get('post_video', None)
        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        if not media_type:
            request_errors['media_type'] = "Please provide media Type"

        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"

        if request_errors:
            return JsonResponse({'status': False, 'errors': request_errors})

        images = request.POST.getlist('post_image_urls')
        files = request.FILES.getlist('post_image_urls')
        saved_image_urls = []
        print(saved_image_urls)

        # Handle base64 encoded images
        for image_data in images:
            if image_data.startswith("data:image"):
                format, imgstr = image_data.split(';base64,') 
                ext = format.split('/')[-1]
                image_name = f'{int(datetime.now().timestamp())}_{uuid4().hex}.{ext}'
                file_path = os.path.join(settings.MEDIA_ROOT, 'images/post', image_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(base64.b64decode(imgstr))
                saved_image_url = f'images/post/{image_name}'
                saved_image_urls.append(saved_image_url)

        # Handle file uploads
        for file in files:
            image_name = f'{int(datetime.now().timestamp())}_{uuid4().hex}_{file.name}'
            file_path = os.path.join(settings.MEDIA_ROOT, 'images/post', image_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(file.read())
            saved_image_url = f'images/post/{image_name}'
            saved_image_urls.append(saved_image_url)

        try:
            user_post_row = post.objects.get(user_token=user_token)
            # Update existing record
            user_post_row.media_type = media_type
            user_post_row.post_description = post_description
            user_post_row.post_image_urls = saved_image_urls
            user_post_row.post_video = post_video
            user_post_row.private_post = private_post
            user_post_row.status = status
            user_post_row.save()
        except post.DoesNotExist:
            # Create new record if user_token does not exist
            user_post_row = post.objects.create(
                user_token=user_token,
                media_type=media_type,
                post_description=post_description,
                post_image_urls=saved_image_urls,
                post_video=post_video,
                private_post=private_post,
                status=status
            )
        print(saved_image_urls)
        return JsonResponse({'status': True, 'message': 'Post created successfully!', 'post_id': user_post_row.id}, status=201)

    except KeyError as e:
        return JsonResponse({'status': False, 'error': f'Missing field: {str(e)}'}, status=400)

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)

# @csrf_exempt
# @require_http_methods(["POST"])
# def create_post(request):
#     try:
#         user_token = request.POST.get('user_token')
#         media_type = request.POST.get('media_type')
#         # private_post = request.POST.get('private_post')  # Ensure 'private_post' is provided in the request
#         post_description = request.POST.get('post_description')
#         status = request.POST.get('status', False)
#         # post_image_urls = request.POST.get('post_image_urls')
#         # print(post_image_urls)
#         post_video = request.FILES.get('post_video', None)  # Use FILES for file uploads
#         request_errors = {}

#         # Validate fields
#         if not user_token:
#             request_errors['user_token'] = "Please provide user token"
#         if not media_type:
#             request_errors['media_type'] = "Please provide media Type"
#         # if not private_post:
#         #     request_errors['private_post'] = "Please provide private post status"
        
#         # Validate user token using nimbo_users utility function
#         if not nimbo_users.check_user_token(user_token):
#             request_errors['user_token'] = "User token is not valid"

#         if request_errors:
#             return JsonResponse({'status': False, 'errors': request_errors})
        
#                 # Process base64 image data if available
#         images = request.POST.getlist('post_image_urls')  # Assuming base64 encoded images
#         files = request.FILES.getlist('post_image_urls')  # For file uploads
#         saved_image_urls = []
#         print(saved_image_urls)

#         # Handle base64 encoded images
#         for image_data in images:
#             if image_data.startswith("data:image"):
#                 format, imgstr = image_data.split(';base64,') 
#                 ext = format.split('/')[-1]
#                 image_name = f'{int(datetime.now().timestamp())}.{ext}'
#                 file_path = os.path.join(settings.MEDIA_ROOT, 'images/post', image_name)
#                 os.makedirs(os.path.dirname(file_path), exist_ok=True)
#                 with open(file_path, 'wb') as f:
#                     f.write(base64.b64decode(imgstr))
#                 saved_image_url = f'images/post/{image_name}'
#                 saved_image_urls.append(saved_image_url)

#         # Handle file uploads
#         for file in files:
#             image_name = f'{int(datetime.now().timestamp())}_{file.name}'
#             file_path = os.path.join(settings.MEDIA_ROOT, 'images/post', image_name)
#             os.makedirs(os.path.dirname(file_path), exist_ok=True)
#             with open(file_path, 'wb') as f:
#                 f.write(file.read())
#             saved_image_url = f'images/post/{image_name}'
#             saved_image_urls.append(saved_image_url)
#         print(saved_image_urls)
#         try:
#             user_post_row = post.objects.get(user_token=user_token)
#             # Update existing record
#             user_post_row.media_type = media_type
#             # user_post_row.private_post = private_post
#             user_post_row.post_description = post_description
#             user_post_row.post_image_urls = saved_image_urls  # Store list of image URLs
#             user_post_row.post_video = post_video
#             user_post_row.status = status
#             user_post_row.save()
#         except post.DoesNotExist:
#             # Create new record if user_token does not exist
#             user_post_row = post.objects.create(
#                 user_token=user_token,
#                 media_type=media_type,
#                 # private_post=private_post,
#                 post_description=post_description,
#                 post_image_urls=saved_image_urls,  # Store list of image URLs
#                 post_video=post_video,
#                 status=status
#             )

#         return JsonResponse({'status': True, 'message': 'Post created successfully!', 'post_id': user_post_row.id}, status=201)

#     except KeyError as e:
#         return JsonResponse({'status': False, 'error': f'Missing field: {str(e)}'}, status=400)

#     except Exception as e:
#         tb = traceback.format_exc()
#         return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)



# @csrf_exempt
# @require_http_methods(["POST"])
# def create_post(request):
#     try:
#         user_token = request.POST.get('user_token')
#         media_type = request.POST.get('media_type')
#         private_post = request.POST.get('private_post')  
#         post_description = request.POST.get('post_description')
#         post_image_url = request.POST.get('post_image_url')
#         post_video = request.POST.get('post_video')
#         status = request.POST.get('status', False)
#         request_errors = {}

#         # Validate fields
#         if not user_token:
#             request_errors['user_token'] = "Please provide user token"
#         if not media_type:
#             request_errors['media_type'] = "Please provide media Type"
#         if not post_image_url:
#             request_errors['post_image_url'] = "Please provide Post Image Url"
#         # Validate user token using nimbo_users utility function
#         if not nimbo_users.check_user_token(user_token):
#             request_errors['user_token'] = "User token is not valid"

#         if request_errors:
#             return JsonResponse({'status': False, 'errors': request_errors})
        
#         # Process base64 image data if available
#         images = request.FILES.getlist('post_image_url')  # assuming 'post_images' is the name of the field for multiple images
        
#        # List to store URLs of saved images
#         saved_image_urls = []

#         for image in images:
#             # Read image data
#             image_data = image.read()
#             # Create the file path
#             image_name = f'{int(datetime.now().timestamp())}_{image.name}'
#             file_path = os.path.join(settings.MEDIA_ROOT, 'images/post', image_name)
#             # Ensure the directory exists
#             os.makedirs(os.path.dirname(file_path), exist_ok=True)
#             # Write the image data to a file
#             with open(file_path, 'wb') as f:
#                 f.write(image_data)
#             saved_image_url = f'images/post/{image_name}'
#             saved_image_urls.append(saved_image_url)

#                 # Save new Post record with multiple images
#         try:
#             user_post_row = post.objects.get(user_token=user_token)
#             # Update existing record
#             user_post_row.media_type = media_type
#             user_post_row.private_post = private_post
#             user_post_row.post_description = post_description
#             user_post_row.post_video = post_video
#             user_post_row.save()
#         except post.DoesNotExist:
#             # Create new record if user_token does not exist
#             user_post_row = post.objects.create(
#                 user_token=user_token,
#                 media_type=media_type,
#                 private_post=private_post,
#                 post_description=post_description,
#                 post_video=post_video
#             )
        
#         # Create or update related images for the post
#         for saved_image_url in saved_image_urls:
#             post.objects.create(post=user_post_row, image_url=saved_image_url)

#         return JsonResponse({'status': True, 'message': 'Post created successfully!'}, status=201)

#     except KeyError as e:
#         return JsonResponse({'status': False, 'error': f'Missing field: {str(e)}'}, status=400)

#     except Exception as e:
#         tb = traceback.format_exc()
#         return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)

# Views file for Create Story Post:

@csrf_exempt
@require_http_methods(["POST"])
def create_story_post(request):
    try:
        
        user_token = request.POST.get('user_token')
        story_post_url = request.POST.get('story_post_url')

        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"


        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"

        if request_errors:
            return JsonResponse({'status': False, 'errors': request_errors})
        
        # Process base64 image data if available
        base64_image = request.POST.get('post_image_url', None)

        if base64_image:
            # Check if the base64 image data is in the correct format
            if ',' in base64_image:
                header, base64_image = base64_image.split(',', 1)
                # Decode the base64 image
                image_data = base64.b64decode(base64_image)
                # Create the file path
                image_name = int(datetime.now().timestamp())
                file_path = os.path.join(settings.MEDIA_ROOT, 'images/post', f'{image_name}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Write the image data to a file
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                post_image_url = f'images/post/{image_name}.png'
            else:
                request_errors['post_image_url'] = "Invalid base64 image format"
                
        # Save new Symptoms record
        try:
            user_post_row = post.objects.get(user_token=user_token)
            # Update existing record
            user_post_row.media_type = media_type
            user_post_row.post_image_url = post_image_url
            user_post_row.post_description = post_description
            user_post_row.post_video = post_video
            user_post_row.save()
        except user_post_row.DoesNotExist:
            # Create new record if user_token does not exist
            user_post_row = post.objects.create(
                user_token=user_token,
                media_type=media_type,
                post_image_url=post_image_url,
                post_description=post_description,
                post_video=post_video
            )
        return JsonResponse({'status': True, 'message': 'Post created successfully!'}, status=201)
    except KeyError as e:
        return JsonResponse({'status': False, 'error': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)



# For Creating Symptoms:
# @csrf_exempt
# @require_http_methods(["POST"])
# def create_posts(request):
#     try:
#         user_token = request.POST.get('user_token')
#         post_type = request.POST.get('post_type')
#         private_post = request.POST.get('private_post')

#         request_errors = {}
        
#         # Validate fields
#         if not user_token:
#             request_errors['user_token'] = "Please Provide User token"
        
#         if not post_type:
#             request_errors['post_type'] = "Please Provide Post Type"
        
#         if not private_post:
#             request_errors['private_post'] = "Please Provide Private Post"
        
#         # Validate user token using nimbo_users utility function
#         if not nimbo_users.check_user_token(user_token):
#             request_errors['user_token'] = "User token is not valid"
    
#         if request_errors:
#             return JsonResponse({
#                 'status': False,
#                 'errors': request_errors
#             })
        
        # user_post_row = post(
        #     user_token=user_token,
        #     post_type=post_type,
        #     private_post=private_post
        # )
        # For saving records:
        # user_post_row = post.objects.create(
        #     user_token=user_token

        # )

        
        # # Check if the Symptoms already exists for any user
        # existing_symptoms = symptoms.objects.filter(title=title).first()
        # if existing_symptoms:
        #     # Check if the Symptoms already exists for the current user
        #     symptoms_for_user = user_symptoms.objects.filter(user_token=user_token).select_related('symptoms')
        #     # symptoms_for_user = user_symptoms.objects.filter(user_token=user_token, diagnosis=existing_symptoms).first()
        #     if symptoms_for_user:
        #         message = "Symptoms already exists for this user."
        #     else:
        #         # Assign the existing Symptoms to the current user
        #         user_symptoms.objects.create(
        #             user_token=user_token,
        #             symptoms=existing_symptoms
        #         )
        #         message = "Symptoms assigned to current user."
        # else:
        #     # Save new Symptoms record
        #     new_symptoms = symptoms.objects.create(
        #         user_token=user_token,
        #         title=title
        #     )
        #     user_symptoms.objects.create(
        #         user_token=user_token,
        #         symptoms=new_symptoms
        #     )
        #     message = "Symptoms created successfully"
        
        # # Retrieve current user's diagnoses
        # users_symptoms = user_symptoms.objects.filter(user_token=user_token).select_related('symptoms')
        # symptoms_list = [
        #     {
        #         'id': ud.symptoms.id,
        #         'title': ud.symptoms.title,
        #         'created_at': ud.symptoms.created_at,
        #         'updated_at': ud.symptoms.updated_at,
        #         'status': ud.symptoms.status,
        #     } for ud in users_symptoms
        # ]
    #     response = {
    #         'status': True,
    #         'message': 'Post Added Successfully'
    #         'symptoms_list': symptoms_list,
             
    #     }
    #     return JsonResponse(response, status=201)
        
    # except Exception as e:
    #     tb = traceback.format_exc()
    #     return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)






# For Health Goals Correct Code:
@csrf_exempt
@require_http_methods(["POST"])
def create_post_feed(request):
    try:
        user_token = request.POST.get('user_token')
        post_type = request.POST.get('post_type')
        private_post = request.POST.get('private_post')
        post_template = request.POST.get('post_template')
        description = request.POST.get('description')
        post_media = request.POST.get('post_media')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please Provide user token"
        if not post_type:
            request_errors['post_type'] = "Please Provide post type"
        if not private_post:
            request_errors['private_post'] = "Please Provide private post"
        if not post_template:
            request_errors['post_template'] = "Please Provide post template"
        if not description:
            request_errors['description'] = "Please Provide description"
        if not post_media:
            request_errors['post_media'] = "Please Provide post media"
        
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User is not valid"
    
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : request_errors
        })
        # Save OTP record
        feed_post_row = feed_post(
            user_token=user_token,
            post_type=post_type,
            private_post=private_post,
            post_template=post_template,
            description=description,
            post_media=post_media,
        )
        feed_post_row.save()

        return JsonResponse({
            'status': True,
            'message': 'Post addded successfully.'
        })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)











