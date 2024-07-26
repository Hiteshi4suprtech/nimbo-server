from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.views.decorators.http import require_http_methods # type: ignore
import json
from django.http import JsonResponse # type: ignore
from django.utils.dateparse import parse_datetime # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from nib.models import nimbo_users, symptoms, user_severity, health_style,user_symptoms,diagonsis,user_diagonsis
import traceback
import spacy
from django.core.exceptions import ObjectDoesNotExist
from user_symptoms.utils import get_user_symptoms_and_diagnosis


# Using NLP:
nlp = spacy.load("en_core_web_md")

# For Creating Symptoms:
@csrf_exempt
@require_http_methods(["POST"])
def create_symptoms(request):
    try:
        user_token = request.POST.get('user_token')
        title = request.POST.get('title')
        request_errors = {}
        
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        if not title:
            request_errors['title'] = "Please provide symptoms title"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
    
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            })
        
        # Check if the Symptoms already exists for any user
        existing_symptoms = symptoms.objects.filter(title=title).first()
        if existing_symptoms:
            # Check if the Symptoms already exists for the current user
            symptoms_for_user = user_symptoms.objects.filter(user_token=user_token).select_related('symptoms')
            # symptoms_for_user = user_symptoms.objects.filter(user_token=user_token, diagnosis=existing_symptoms).first()
            if symptoms_for_user:
                message = "Symptoms already exists for this user."
            else:
                # Assign the existing Symptoms to the current user
                user_symptoms.objects.create(
                    user_token=user_token,
                    symptoms=existing_symptoms
                )
                message = "Symptoms assigned to current user."
        else:
            # Save new Symptoms record
            new_symptoms = symptoms.objects.create(
                user_token=user_token,
                title=title
            )
            user_symptoms.objects.create(
                user_token=user_token,
                symptoms=new_symptoms
            )
            message = "Symptoms created successfully"
        
        # Retrieve current user's diagnoses
        users_symptoms = user_symptoms.objects.filter(user_token=user_token).select_related('symptoms')
        symptoms_list = [
            {
                'id': ud.symptoms.id,
                'title': ud.symptoms.title,
                'created_at': ud.symptoms.created_at,
                'updated_at': ud.symptoms.updated_at,
                'status': ud.symptoms.status,
            } for ud in users_symptoms
        ]
        response = {
            'status': True,
            'symptoms_list': symptoms_list,
             
        }
        return JsonResponse(response, status=201)
        
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)
    

# Code for Selecting symptom by user:
@csrf_exempt
@require_http_methods(["POST"])
def select_symptoms_by_new_user(request):
    try:
        user_token = request.POST.get('user_token')
        symptoms_id = request.POST.get('symptoms_id')
        request_errors = {}
        
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        if not symptoms_id:
            request_errors['symptoms_id'] = "Please provide symptoms ID"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            })
                # Retrieve the symptoms based on symptoms_id
        try:
            symptom = symptoms.objects.get(id=symptoms_id)
        except symptoms.DoesNotExist:
            return JsonResponse({
                'status': False,
                'errors': {'_id': "Symptoms with this ID does not exist"}
            })
        
        # Check if the symptoms already exists for the current user
        if user_symptoms.objects.filter(user_token=user_token, symptoms=symptom).exists():
            message = "symptoms already exists for this user."
        else:
            # Save the symptoms for the current user
            user_symptom = user_symptoms.objects.create(user_token=user_token, symptoms=symptom)
            message = "Symptom added to current user."

        
        # Fetch updated symptoms list for the user
        user_symptom = user_symptoms.objects.filter(user_token=user_token).select_related('symptoms')
        symptoms_list = [{'id': ud.symptoms.id, 'title': ud.symptoms.title} for ud in user_symptom]

        response = {
            'status': True,
            'message': message,
            'symptoms_list': symptoms_list,
        }
        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)
    

# For Symptom-List:
@csrf_exempt
@require_http_methods(["POST"])
def symptoms_list(request):
    try:
        user_token = request.POST.get('user_token')
        query_string  = request.POST.get('query_string')
        limit = 9
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide login token"
       
        if nimbo_users.check_user_token(nimbo_users):
            request_errors['user_token'] = "User is not valid"
         
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : [request_errors]
        })
        # Save Symptom row:
        symptoms_row = symptoms.get_list(symptoms, user_token, query_string,limit)
        # symptoms_row = symptoms.get_list(symptoms, user_token, request.POST.get('query_string'))

        return JsonResponse({
            'status': True,
            'symptoms_list': list(symptoms_row.values())
        })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)


# For Symptom-List by Particular User:
@csrf_exempt
@require_http_methods(["POST"])
def get_symptoms_list_by_user(request):
    try:
        user_token = request.POST.get('user_token')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide login token"
       
        if nimbo_users.check_user_token(nimbo_users):
            request_errors['user_token'] = "User is not valid"
         
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : [request_errors]
        })
        # Save Symptom row:
        # Fetch updated symptoms list for the user
        user_symptom = user_symptoms.objects.filter(user_token=user_token).select_related('symptoms')
        symptoms_list = [{'id': ud.symptoms.id, 'title': ud.symptoms.title} for ud in user_symptom]

        response = {
            'status': True,
            'message': 'User Symptoms Added',
            'symptoms_list': symptoms_list,
        }
        return JsonResponse(response, status=201)
        # symptoms_row = symptoms.get_list_by_user(symptoms, user_token)

        # return JsonResponse({
        #     'status': True,
        #     'message': list(symptoms_row.values())
        # })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)


# Delete Symptoms from Main Table and User Tables:
@csrf_exempt
@require_http_methods(["POST"])
def delete_symptoms_list_by_user(request):
    try:
        user_token = request.POST.get('user_token')
        symptoms_id = request.POST.get('symptoms_id')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        if not symptoms_id:
            request_errors['symptoms_id'] = "Please provide Symptoms ID"
       
        if nimbo_users.check_user_token(nimbo_users):
            request_errors['user_token'] = "User is not valid"
    
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : [request_errors]
        })
        # Save Symptoms record:
        deleted_symptoms = symptoms.soft_delete_by_user(symptoms_id, user_token)
        user_symptoms_record = user_symptoms.objects.get(user_token=user_token, symptoms_id=symptoms_id)
        user_symptoms_record.delete()
        user_symptom = user_symptoms.objects.filter(user_token=user_token).select_related('symptoms')
        symptoms_list = [{'id': ud.symptoms.id, 'title': ud.symptoms.title} for ud in user_symptom]
        print(symptoms_list)
     
        if deleted_symptoms and user_symptoms_record:
            return JsonResponse({
                'status': True,
                'message': "Symptoms soft-deleted and user-symptoms successfully",
                'symptoms_list':symptoms_list
                 })
        else:
            return JsonResponse({
                'status': True,
                'message': "Symptoms not found or already soft deleted",
                'symptoms_list':symptoms_list
            })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)
    

# ----------------------Views for Symptoms and Diagnosis both-------------------------------------------------:
@csrf_exempt
@require_http_methods(["POST"])
def symptoms_diagnosis_list(request):
    try:
        user_token = request.POST.get('user_token')
        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            }, status=400)
        
        # Fetch updated symptoms and diagnosis lists for the user
        symptoms_diagnosis_list = get_user_symptoms_and_diagnosis(user_token)

        response = {
            'status': True,
            'message': 'Symptom and Diagnosis List Fetch Successfull',
            'symptom_diagnosis_list': symptoms_diagnosis_list
        }
        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)
    
# Function for Selecting Symptoms and Diagnosis from List:
@csrf_exempt
@require_http_methods(["POST"])
def select_symptoms_diagnosis(request):
    try:
        user_token = request.POST.get('user_token')
        selected_id = request.POST.get('selected_id')
        print(selected_id)
        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            }, status=400)
        
        # Fetch updated symptoms and diagnosis lists for the user
        symptoms_diagnosis_list = get_user_symptoms_and_diagnosis(user_token)

        # Select the item based on selected_id or other criteria
        selected_item = None
        if symptoms_diagnosis_list:
            for item in symptoms_diagnosis_list:
                if item.get('id') == selected_id:  # Adjust the condition as per your data structure
                    selected_item = item
                    break

        if selected_item is None:
            return JsonResponse({
                'status': False,
                'message': f"Selected item with ID '{selected_id}' not found",
            }, status=404)

        response = {
            'status': True,
            'message': 'Symptom and Diagnosis List Fetch Successful',
            'symptom_diagnosis_list': selected_item
        }

        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)
    
# For Soft-Delete from Selected List:
@csrf_exempt
@require_http_methods(["POST"])
def delete_symptoms_diagnosis(request):
    try:
        user_token = request.POST.get('user_token')
        selected_id = request.POST.get('selected_id')
        print(selected_id)
        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        if not selected_id:
            request_errors['selected_id'] = "Please provide Selected ID"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            }, status=400)
        
        # Fetch updated symptoms and diagnosis lists for the user
        symptoms_diagnosis_list = get_user_symptoms_and_diagnosis(user_token)

        # Select the item based on selected_id or other criteria
        selected_item = None
        for item in symptoms_diagnosis_list:
            if item.get('id') == selected_id and not item.get('soft_delete'):
                selected_item = item
                # Perform the update in the database
                user_symptoms.soft_delete_by_user(selected_id, user_token)
                user_diagonsis.soft_delete_by_user(selected_id, user_token)
                break

        if selected_item is None:
            return JsonResponse({
                'status': False,
                'message': f"Selected item with ID '{selected_id}' not found",
            }, status=404)

        response = {
            'status': True,
            'message': 'Symptom and Diagnosis List Fetch Successful',
            'symptom_diagnosis_list': selected_item
        }

        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)



# ----------------------------------------------For Adding Severity-------------------------------------------------------------------:
@csrf_exempt
@require_http_methods(["POST"])
def add_severity(request):
    try:
        user_token = request.POST.get('user_token')
        severity_1 = request.POST.get('severity_1')
        severity_2 = request.POST.get('severity_2')
        severity_3 = request.POST.get('severity_3')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide User token"
        if not severity_1:
            request_errors['severity_1'] = "Please provide severity 1"
        if not severity_2:
            request_errors['severity_2'] = "Please provide severity 2"
        if not severity_3:
            request_errors['severity_3'] = "Please provide severity 3"
        
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
    
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : request_errors
        })
        # Check if user_token already exists in the database
        try:
            user_severity_row = user_severity.objects.get(user_token=user_token)
            # Update existing record
            user_severity_row.severity_1 = severity_1
            user_severity_row.severity_2 = severity_2
            user_severity_row.severity_3 = severity_3
            user_severity_row.save()
        except user_severity.DoesNotExist:
            # Create new record if user_token does not exist
            user_severity_row = user_severity.objects.create(
                user_token=user_token,
                severity_1=severity_1,
                severity_2=severity_2,
                severity_3=severity_3
            )

        return JsonResponse({
            'status': True,
            'message': 'Severity added successfully.'
        })
        # if user_token:
        # # Save OTP record
        #     user_severity_row = user_severity.objects.update(severity_1=severity_1,severity_2=severity_2,severity_3=severity_3)
        # else:
        #     user_severity_row = user_severity(
        #         user_token=user_token,
        #         severity_1=severity_1,
        #         severity_2=severity_2,
        #         severity_3=severity_3
        #     )  
        #     user_severity_row.save()
            

        # return JsonResponse({
        #     'status': True,
        #     'message': 'Severity addded successfully.'
        # })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)


# --------------------------------------------------------For Adding Health Actions Code------------------------------------------------:
@csrf_exempt
@require_http_methods(["POST"])
def add_health_action(request):
    try:
        user_token = request.POST.get('user_token')
        foods_diets = request.POST.get('foods_diets')
        supplements = request.POST.get('supplements')
        movement_exercise = request.POST.get('movement_exercise')
        body_therapies = request.POST.get('body_therapies')
        request_errors = {}
        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        if not foods_diets:
            request_errors['foods_diets'] = "Please provide foods diets"
        if not supplements:
            request_errors['supplements'] = "Please provide supplements"
        if not movement_exercise:
            request_errors['movement_exercise'] = "Please provide movement exercise"
        if not body_therapies:
            request_errors['body_therapies'] = "Please provide body therapies"
        
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
    
        if len(request_errors) > 0:
            return JsonResponse({
                'status' : False,
                'errors' : request_errors
        })
        # Convert JSON strings to Python dictionaries
        # foods_diets = json.loads(foods_diets)
        # supplements = json.loads(supplements)
        # movement_exercise = json.loads(movement_exercise)
        # body_therapies = json.loads(body_therapies)

        # Check if user_token already exists in the database
        try:
            health_style_row = health_style.objects.get(user_token=user_token)
            # Update existing record
            health_style_row.foods_diets = foods_diets
            health_style_row.supplements = supplements
            health_style_row.movement_exercise = movement_exercise
            health_style_row.body_therapies = body_therapies
            health_style_row.save()
        except health_style.DoesNotExist:
            # Create new record if user_token does not exist
            health_style_row = health_style.objects.create(
                user_token=user_token,
                foods_diets=foods_diets,
                supplements=supplements,
                movement_exercise=movement_exercise,
                body_therapies=body_therapies
            )

        return JsonResponse({
            'status': True,
            'message': 'Health actions added successfully.'
        })

        # if user_token:
        #     health_style_row=health_style.objects.update(foods_diets=foods_diets,supplements=supplements,movement_exercise=movement_exercise,body_therapies=body_therapies)
        # else:
        #     # Save OTP record
        #     health_style_row = health_style(
        #         user_token=user_token,
        #         foods_diets=foods_diets,
        #         supplements=supplements,
        #         movement_exercise=movement_exercise,
        #         body_therapies=body_therapies
        #     )
        #     health_style_row.save()

        # return JsonResponse({
        #     'status': True,
        #     'message': 'Health actions addded successfully.'
        # })

    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'line': tb}, status=500)
    
# Select Food_Diets from list of food:
@csrf_exempt
@require_http_methods(["POST"])
def selected_food_diets(request):
    try:
        user_token = request.POST.get('user_token')
        selected_id = request.POST.get('selected_id')
        print(selected_id)
        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            }, status=400)
        
        # Fetch all food diets for the user
        food_diets_list = health_style.get_foods_diets(user_token)
        print(food_diets_list)

        if not food_diets_list:
            return JsonResponse({
                'status': False,
                'message': "No food diets found for the user",
            }, status=404)

        response = {
            'status': True,
            'message': 'Food Diets List Fetch Successful',
            'food_diets_list': food_diets_list
        }


        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)
    

# Select Supplements from Supplements list:
@csrf_exempt
@require_http_methods(["POST"])
def selected_supplements(request):
    try:
        user_token = request.POST.get('user_token')
        selected_id = request.POST.get('selected_id')
        print(selected_id)
        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            }, status=400)
        
        # Fetch Supplements lists for the user
        supplements_list = health_style.get_supplements(user_token)

        if supplements_list is None:
            return JsonResponse({
                'status': False,
                'message': f"Selected item with ID '{selected_id}' not found",
            }, status=404)

        response = {
            'status': True,
            'message': 'Supplements List Fetch Successful',
            'suppliments_list': supplements_list
        }

        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)
    

# Select Food_Diets from list of food:
@csrf_exempt
@require_http_methods(["POST"])
def selected_movement_exercise(request):
    try:
        user_token = request.POST.get('user_token')
        selected_id = request.POST.get('selected_id')
        print(selected_id)
        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            }, status=400)
        
        # Fetch Movement Exercise lists for the user
        movement_exercise_list = health_style.get_movement_exercise(user_token)

        if movement_exercise_list is None:
            return JsonResponse({
                'status': False,
                'message': f"Selected item with ID '{selected_id}' not found",
            }, status=404)

        response = {
            'status': True,
            'message': 'Movement Exercise List Fetch Successful',
            'movement_exercise_list': movement_exercise_list
        }

        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)
    

# Select Food_Diets from list of food:
@csrf_exempt
@require_http_methods(["POST"])
def selected_body_therapies(request):
    try:
        user_token = request.POST.get('user_token')
        selected_id = request.POST.get('selected_id')
        print(selected_id)
        request_errors = {}

        # Validate fields
        if not user_token:
            request_errors['user_token'] = "Please provide user token"
        
        # Validate user token using nimbo_users utility function
        if not nimbo_users.check_user_token(user_token):
            request_errors['user_token'] = "User token is not valid"
        
        if request_errors:
            return JsonResponse({
                'status': False,
                'errors': request_errors
            }, status=400)
        
        # Fetch body_therepies_list for the user:
        body_therepies_list = health_style.get_body_therapies(user_token)

        if body_therepies_list is None:
            return JsonResponse({
                'status': False,
                'message': f"Selected item with ID '{selected_id}' not found",
            }, status=404)

        response = {
            'status': True,
            'message': 'Body therepies List Fetch Successful',
            'body_therepies_list': body_therepies_list
        }

        return JsonResponse(response, status=201)
    
    except Exception as e:
        tb = traceback.format_exc()
        return JsonResponse({'status': False, 'error': str(e), 'traceback': tb}, status=500)













