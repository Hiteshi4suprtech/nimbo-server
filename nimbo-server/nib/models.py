from django.db import models # type: ignore
from django.utils import timezone # type: ignore
import spacy

nlp = spacy.load('en_core_web_md')  # Load spaCy model
# Create your models here.


# Models for Nimbo Users:
class nimbo_users(models.Model):
    user_token = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    d_o_b = models.TextField(null=True)
    nick_name = models.CharField(max_length=150, null=True, unique=True)
    image_url = models.TextField(null=True)
    firebase_json = models.JSONField(null=True)
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def email_exists(cls, email):
        return cls.objects.filter(email=email).exists()
    @classmethod
    def check_user_token(cls, user_token, login_token=None):
        return cls.objects.filter(user_token=user_token).exists()
    def save_user(self, user_token, name, email, d_o_b, nick_name, image_url, firebase_json):
        if user_token:
            self.user_token = user_token
        if name:
            self.name = name
        if email:
            self.email = email
        if d_o_b:
            self.d_o_b = d_o_b
        if nick_name:
            self.nick_name=nick_name
        if image_url:
            self.image_url=image_url
        if firebase_json:
            self.firebase_json=firebase_json
        self.save()


# otp _type = set_password, reset_password
class otp_verify(models.Model):
    email = models.EmailField()
    otp = models.IntegerField()
    otp_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def delete_otp(cls, email, otp_type):
        if cls.objects.filter(email=email, otp_type=otp_type).count() > 0:
            otp_row = cls.objects.get(email=email, otp_type=otp_type)
            otp_row.delete()
            return True
        else:
            # Handle case where no such object exists
             return True
    def check_otp(cls, email, otp_type, otp):
        
        if cls.objects.filter(email=email, otp_type=otp_type, otp=otp).count() > 0:
            otp_row = cls.objects.get(email=email, otp_type=otp_type, otp=otp)
            otp_row.delete()
            return True
        else:
            # Handle case where no such object exists
            return False
        
        
# Models for Health Goals:
class health_goal(models.Model):
    user_token = models.CharField(max_length=150, unique=True)
    goal_id = models.IntegerField()
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def goal_exists(cls, user_token):
        return cls.objects.filter(user_token=user_token).exists()

# Models for All Diagonsis:
class diagonsis(models.Model):
    user_token = models.CharField(max_length=150, null=True)
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True)
    icon = models.TextField(null=True)
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def get_list(cls, user_token=None,query_string=None,limit=None):
        if query_string:
            return cls.objects.filter(title__icontains=query_string)
        return cls.objects.all()
    def get_list_by_user(cls, user_token):
        return cls.objects.filter(user_token=user_token,soft_delete=False)
    @classmethod
    def soft_delete_by_user(cls, diagnosis_id, user_token):
        diagonsis_to_delete = cls.objects.filter(id=diagnosis_id,user_token=user_token, soft_delete=False).first()
        if diagonsis_to_delete:
            if diagonsis_to_delete.soft_delete == True:
                return True
            diagonsis_to_delete.soft_delete = True
            diagonsis_to_delete.updated_at = timezone.now()
            diagonsis_to_delete.save()
        return diagonsis_to_delete
    @classmethod
    def get_diagonsis_suggestions(cls, title, diagonsis):
        doc = nlp(title) # type: ignore
        suggestions = []
        for diag in diagonsis:
            similarity = doc.similarity(nlp(diag.title)) # type: ignore
            if similarity > 0.75:  # Adjust similarity threshold as needed
                suggestions.append({'id': diag.id, 'title': diag.title})
        return suggestions
    
# Models for Particular User Symptoms:
class user_diagonsis(models.Model):  
    user_token = models.CharField(max_length=150)
    # diagnosis_id = models.IntegerField()
    diagnosis = models.ForeignKey('diagonsis', on_delete=models.CASCADE)
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    @classmethod
    def get_list(cls, user_token):
        return cls.objects.filter(user_token=user_token)
    @classmethod
    def soft_delete_by_user(cls, user_diagonsis_id, user_token):
        symptom_to_delete = cls.objects.filter(id=user_diagonsis_id,user_token=user_token, soft_delete=False).first()
        if symptom_to_delete:
            symptom_to_delete.soft_delete = True
            symptom_to_delete.updated_at = timezone.now()
            symptom_to_delete.save()
        return symptom_to_delete


# Models for All Symptoms:
class symptoms(models.Model):  
    user_token = models.CharField(max_length=150, null=True)
    title = models.CharField(max_length=150,unique=True)
    description = models.TextField(null=True)
    icon = models.TextField(null=True)
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    @classmethod
    def soft_delete_by_user(cls, symptom_id, user_token):
        symptom_to_delete = cls.objects.filter(id=symptom_id,user_token=user_token).first()
        if symptom_to_delete:
            if symptom_to_delete.soft_delete == True:
                return True
            else:
                symptom_to_delete.soft_delete = True
                symptom_to_delete.updated_at = timezone.now()
                symptom_to_delete.save()
        return symptom_to_delete
    def get_list(cls, user_token=None, query_string=None, limit=None):
        query = cls.objects.all()
        if query_string:
            query = query.filter(title__icontains=query_string)
        if limit:
            query = query[:limit]
        return query
    def get_list_by_user(cls, user_token):
        return cls.objects.filter(user_token=user_token)
    @classmethod
    def get_symptom_suggestions(cls, title, symptoms):
        doc = nlp(title)
        suggestions = []
        for symptom in symptoms:
            similarity = doc.similarity(nlp(symptom.title))
            print(f"Comparing '{title}' with '{symptom.title}' - Similarity: {similarity}")
            if similarity > 0.75:  # Adjust similarity threshold as needed
                suggestions.append({'id': symptom.id, 'title': symptom.title})
        return suggestions

# For Particular User Table Data:
class user_symptoms(models.Model):  
    user_token = models.CharField(max_length=150)
    # symptoms_id = models.IntegerField()
    symptoms = models.ForeignKey('symptoms', on_delete=models.CASCADE)
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    @classmethod
    def permanent_delete_by_user(cls, user_symptom_id, user_token):
        symptom_to_delete = cls.objects.filter(id=user_symptom_id, user_token=user_token, soft_delete=True).first()
        if symptom_to_delete:
            symptom_to_delete.delete()
        return symptom_to_delete
    @classmethod
    def soft_delete_by_user(cls, user_symptom_id, user_token):
        symptom_to_delete = cls.objects.filter(id=user_symptom_id,user_token=user_token, soft_delete=False).first()
        if symptom_to_delete:
            symptom_to_delete.soft_delete = True
            symptom_to_delete.updated_at = timezone.now()
            symptom_to_delete.save()
        return symptom_to_delete
    @classmethod
    def get_list(cls, user_token):
        return cls.objects.filter(user_token=user_token)
        
# Models for Symptoms:
class user_severity(models.Model):  
    user_token = models.CharField(max_length=150)
    severity_1 = models.JSONField()
    severity_2 = models.JSONField()
    severity_3 = models.JSONField()
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def get_list(cls, user_token):
        return cls.objects.all()

# Models for Symptoms:
class health_style(models.Model):  
    user_token = models.CharField(max_length=150)
    foods_diets = models.JSONField()
    supplements = models.JSONField()
    movement_exercise = models.JSONField()
    body_therapies = models.JSONField()
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def get_list(cls, user_token):
        return cls.objects.all()
    # Food and Diets:
    @classmethod
    def get_foods_diets(cls, user_token):
        instances = cls.objects.filter(user_token=user_token)
        if instances.exists():
            return [instance.foods_diets for instance in instances]
        else:
            return []
    @classmethod
    def get_supplements(cls, user_token):
        instances = cls.objects.filter(user_token=user_token)
        if instances.exists():
            return [instance.supplements for instance in instances]
        else:
            return []
    @classmethod
    def get_movement_exercise(cls, user_token):
        instances = cls.objects.filter(user_token=user_token)
        if instances.exists():
            return [instance.movement_exercise for instance in instances]
        else:
            return []
    @classmethod
    def get_body_therapies(cls, user_token):
        instances = cls.objects.filter(user_token=user_token)
        if instances.exists():
            return [instance.body_therapies for instance in instances]
        else:
            return []
        

# Create Model for Post:
class post(models.Model):
    user_token = models.CharField(max_length=150)
    media_type = models.CharField(max_length=150)
    private_post = models.BooleanField(default=False)
    post_description = models.TextField()
    post_image_urls = models.JSONField(null=True, blank=True)
    post_video = models.FileField(upload_to='videos/', null=True, blank=True)
    status = models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

# Model for Story Post:
class story_post(models.Model):
    user_token = models.CharField(max_length=150)
    story_post_url = models.JSONField(null=True, blank=True)
    status = models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class feed_media(models.Model):
    user_token = models.CharField(max_length=150)
    post = models.ForeignKey('post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class feed_post(models.Model):
    user_token = models.CharField(max_length=150)
    post_type = models.IntegerField()
    private_post = models.BooleanField()
    post_template = models.TextField()
    description = models.TextField()
    post_media = models.JSONField()
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


    
    

