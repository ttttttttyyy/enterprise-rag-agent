from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("accounts.urls")),
    path("api/v1/", include("tenants.urls")),
    path("api/v1/", include("knowledge.urls")),
    path("api/v1/", include("assistant.urls")),
    path("api/v1/", include("audit_usage.urls")),
]
