from nib.models import user_diagonsis,user_symptoms

def get_user_symptoms_and_diagnosis(user_token):
    user_symptom_list = user_symptoms.objects.filter(user_token=user_token).select_related('symptoms')
    symptoms_list = [{'id': str(us.symptoms.id), 'title': us.symptoms.title, 'soft_delete': us.symptoms.soft_delete, 'type': 'symptom', 'severity': 0} for us in user_symptom_list]

    user_diagnosis_list = user_diagonsis.objects.filter(user_token=user_token).select_related('diagnosis')
    diagnosis_list = [{'id': str(ud.diagnosis.id), 'title': ud.diagnosis.title, 'soft_delete': ud.diagnosis.soft_delete, 'type': 'diagnosis', 'severity': 0} for ud in user_diagnosis_list]

    symptom_diagnosis_list = symptoms_list + diagnosis_list
    return symptom_diagnosis_list

