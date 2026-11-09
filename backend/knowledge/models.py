from django.conf import settings
from django.db import models
from pgvector.django import VectorField
from tenants.models import Tenant
class Document(models.Model):
    STATUS=[("queued","Queued"),("processing","Processing"),("indexed","Indexed"),("failed","Failed"),("quarantined","Quarantined")]
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name="documents")
    uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    title=models.CharField(max_length=255)
    file=models.FileField(upload_to="tenant_documents/%Y/%m/")
    file_type=models.CharField(max_length=20)
    sha256=models.CharField(max_length=64,db_index=True)
    status=models.CharField(max_length=20,choices=STATUS,default="queued")
    error_message=models.TextField(blank=True)
    approved=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    indexed_at=models.DateTimeField(null=True,blank=True)
    class Meta: ordering=["-created_at"]
class Chunk(models.Model):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE,db_index=True)
    document=models.ForeignKey(Document,on_delete=models.CASCADE,related_name="chunks")
    ordinal=models.PositiveIntegerField()
    content=models.TextField()
    embedding=VectorField(dimensions=1536,null=True,blank=True)
    page_number=models.PositiveIntegerField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=[("document","ordinal")]
