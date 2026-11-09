from django.conf import settings
from django.db import models
from tenants.models import Tenant
class Conversation(models.Model):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name="conversations")
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="conversations")
    title=models.CharField(max_length=200,default="New conversation")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
class Message(models.Model):
    ROLES=[("user","User"),("assistant","Assistant")]
    conversation=models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name="messages")
    role=models.CharField(max_length=12,choices=ROLES)
    content=models.TextField()
    citations=models.JSONField(default=list,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
class Feedback(models.Model):
    message=models.ForeignKey(Message,on_delete=models.CASCADE,related_name="feedback")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating=models.CharField(max_length=20,choices=[("helpful","Helpful"),("incorrect","Incorrect"),("citation_issue","Citation issue"),("missing_knowledge","Missing knowledge")])
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
