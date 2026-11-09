from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
class HealthView(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[]
    def get(self,request):
        checks={}
        try:
            with connection.cursor() as cursor: cursor.execute("SELECT 1"); cursor.fetchone()
            checks["database"]="ok"
        except Exception: checks["database"]="error"
        return Response({"status":"ok" if checks.get("database")=="ok" else "degraded","checks":checks})
