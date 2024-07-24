from django.urls import path # type: ignore
from user_symptoms.views import create_symptoms, symptoms_list, add_severity, add_health_action,get_symptoms_list_by_user,select_symptoms_diagnosis,select_symptoms_by_new_user,symptoms_diagnosis_list,delete_symptoms_list_by_user,delete_symptoms_diagnosis,selected_food_diets,selected_supplements,selected_movement_exercise,selected_body_therapies

urlpatterns=[
    path('create-symptoms/', create_symptoms,name='create_symptoms'),
    path('user-symptoms-list/', get_symptoms_list_by_user,name='get_symptoms_list_by_user'),
    path('add-user-symptoms/', select_symptoms_by_new_user,name='select_symptoms_by_new_user'),
    path('symptoms-list/', symptoms_list,name='symptoms_list'),
    path('delete-user-symptoms/',delete_symptoms_list_by_user,name='delete_symptoms_list_by_user'),
    # -----------------Symptoms Diagnosis List--------------------------------------------------:
    path('symptoms-diagnosis-list/',symptoms_diagnosis_list,name='symptoms_diagnosis_list'),
    path('add-symptoms-diagnosis/',select_symptoms_diagnosis,name='select_symptoms_diagnosis'),
    path('delete-symptoms-diagnosis/',delete_symptoms_diagnosis,name='delete_symptoms_diagnosis'),
    # -----------------Add Severity --------------------------------------------------:
    path('add-severity/', add_severity,name='add_severity'),
    # -----------------Add Health Actions----------------------------------------------:
    path('add-health-style/', add_health_action,name='add_health_action'),
    path('add-food-diets/',selected_food_diets,name='selected_food_diets'),
    path('add-supplements/',selected_supplements,name='selected_supplements'),
    path('add-movements-exercises/',selected_movement_exercise,name='selected_movement_exercise'),
    path('add-body-therapies/',selected_body_therapies,name='selected_body_therapies'),
    
]