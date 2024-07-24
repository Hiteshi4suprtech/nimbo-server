from django.urls import path # type: ignore
from user_diagnosis.views import create_diagnosis, diagnosis_list,get_diagnosis_list_by_user,delete_diagnosis_list_by_user,select_diagnosis_by_new_user

urlpatterns=[
    path('create-diagnosis/', create_diagnosis,name='create_diagnosis'),
    path('add-user-diagonsis/',select_diagnosis_by_new_user,name='select_diagnosis_by_new_user'),
    path('diagnosis-list/', diagnosis_list,name='diagnosis_list'),
    path('user-diagonsis-list/', get_diagnosis_list_by_user,name='get_diagnosis_list_by_user'),
    path('delete-user-diagonsis/',delete_diagnosis_list_by_user,name='delete_diagnosis_list_by_user'),
]