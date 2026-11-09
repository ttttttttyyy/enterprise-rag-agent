from rest_framework import serializers
from .models import Document
class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by=serializers.CharField(source="uploaded_by.username",read_only=True)
    class Meta:
        model=Document
        fields=("id","tenant","title","file","file_type","status","error_message","approved","uploaded_by","created_at","indexed_at")
        read_only_fields=("status","error_message","approved","uploaded_by","created_at","indexed_at")
