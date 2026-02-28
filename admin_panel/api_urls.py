
from rest_framework.routers import DefaultRouter
from .api_views import BlogViewSet,LeadViewSet,PropertyViewSet

router = DefaultRouter()
router.register(r"blogs", BlogViewSet, basename="blogs")
router.register(r"leads", LeadViewSet, basename="leads")
 
router.register(r"properties", PropertyViewSet, basename="properties") 

urlpatterns = router.urls