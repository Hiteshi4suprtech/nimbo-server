from django.db import models

class UserShard(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False, null=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField(default=False, null=True)
    is_blocked = models.BooleanField(default=False, null=True)
    is_influencer = models.BooleanField(default=False, null=True)
    is_provider= models.BooleanField(default=False, null=True)
    bio_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    health_goal = models.TextField(blank=True, null=True)
    alias = models.CharField(max_length=50, blank=True, null=True)
    diagnosis_selected_ids = models.JSONField(blank=True, null=True)  
    symptoms_selected_ids = models.JSONField(blank=True, null=True)   
    meta = models.JSONField(blank=True, null=True)                   

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users_shard'  # Specify the actual table name
        managed = False
