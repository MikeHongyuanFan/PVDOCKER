from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ReminderViewSet, basename='reminder')

urlpatterns = router.urls