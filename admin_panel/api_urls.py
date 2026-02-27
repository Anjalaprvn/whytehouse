
from rest_framework.routers import DefaultRouter
from .api_views import BlogViewSet, LeadViewSet

router = DefaultRouter()
router.register(r"blogs", BlogViewSet, basename="blogs")
router.register(r"leads", LeadViewSet, basename="leads")

urlpatterns = router.urls