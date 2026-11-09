from django.conf import settings
from django.db import models
from tenants.models import Tenant
class AuditEvent(models.Model):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE,null=True,blank=True)
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    event=models.CharField(max_length=100)
    resource=models.CharField(max_length=200,blank=True)
    metadata=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
