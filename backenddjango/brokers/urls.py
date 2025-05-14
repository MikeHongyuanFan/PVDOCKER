from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Register the more specific routes first
router.register(r'bdms', views.BDMViewSet)
router.register(r'branches', views.BranchViewSet)
# Register the base route last
router.register(r'', views.BrokerViewSet)

urlpatterns = router.urls
