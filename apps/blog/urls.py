from rest_framework.routers import DefaultRouter
from apps.blog.views import PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
urlpatterns = router.urls
