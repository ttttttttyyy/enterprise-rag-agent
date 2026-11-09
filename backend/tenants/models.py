from django.conf import settings
from django.db import models
class Tenant(models.Model):
    STATUS = [("active","Active"),("suspended","Suspended"),("archived","Archived")]
    name = models.CharField(max_length=160)
    status = models.CharField(max_length=16, choices=STATUS, default="active")
    plan = models.CharField(max_length=40, default="academic")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_tenants")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Membership(models.Model):
    ROLES = [("tenant_admin","Tenant Admin"),("knowledge_manager","Knowledge Manager"),("reviewer","Reviewer"),("user","User"),("read_only","Read Only")]
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="tenant_memberships")
    role = models.CharField(max_length=24,choices=ROLES,default="user")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = [("tenant","user")]
