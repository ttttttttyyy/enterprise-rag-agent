import hashlib, os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document
from .serializers import DocumentSerializer
from .tasks import index_document
from tenants.permissions import membership_for
class DocumentListCreate(APIView):
    parser_classes=[MultiPartParser,FormParser]
    def get(self,request):
        tid=request.query_params.get("tenant_id")
        if not tid: raise ValidationError({"tenant_id":"Required."})
        membership_for(request.user,tid)
        qs=Document.objects.filter(tenant_id=tid)
        return Response(DocumentSerializer(qs,many=True).data)
    def post(self,request):
        tid=request.data.get("tenant_id")
        member=membership_for(request.user,tid,["tenant_admin","knowledge_manager"])
        upload=request.FILES.get("file")
        if not upload: raise ValidationError({"file":"Upload a file."})
        if upload.size>settings.MAX_UPLOAD_MB*1024*1024: raise ValidationError({"file":"File exceeds upload limit."})
        ext=os.path.splitext(upload.name)[1].lower().lstrip(".")
        if ext not in ("pdf","docx","txt"): raise ValidationError({"file":"Only PDF, DOCX and TXT are allowed."})
        digest=hashlib.sha256(upload.read()).hexdigest(); upload.seek(0)
        if Document.objects.filter(tenant_id=tid,sha256=digest).exists(): raise ValidationError({"file":"This file already exists in this workspace."})
        doc=Document.objects.create(tenant_id=tid,uploaded_by=request.user,title=request.data.get("title") or upload.name,file=upload,file_type=ext,sha256=digest)
        try: index_document.delay(doc.id)
        except Exception:
            # Queue unavailable: retain queued state; staff can retry after worker recovery.
            pass
        return Response(DocumentSerializer(doc).data,status=201)
class DocumentDetail(APIView):
    def get(self,request,pk):
        doc=Document.objects.filter(pk=pk).first()
        if not doc: raise NotFound()
        membership_for(request.user,doc.tenant_id)
        return Response(DocumentSerializer(doc).data)
    def delete(self,request,pk):
        doc=Document.objects.filter(pk=pk).first()
        if not doc: raise NotFound()
        membership_for(request.user,doc.tenant_id,["tenant_admin","knowledge_manager"])
        doc.delete()
        return Response(status=204)
