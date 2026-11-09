from django.urls import path
from .views import TenantListCreate, MemberListCreate
urlpatterns=[path("tenants/",TenantListCreate.as_view()),path("members/",MemberListCreate.as_view())]
