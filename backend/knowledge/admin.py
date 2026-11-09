from django.contrib import admin
from .models import Document, Chunk
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display=("id","title","tenant","status","approved","created_at")
    list_filter=("status","approved")
@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display=("id","document","ordinal","tenant")
