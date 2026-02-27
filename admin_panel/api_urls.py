
from rest_framework.routers import DefaultRouter
from .api_views import BlogViewSet

router = DefaultRouter()
router.register(r"blogs", BlogViewSet, basename="blogs")

urlpatterns = router.urls