from rest_framework.routers import DefaultRouter
from apps.blog.views import PostViewSet, TagViewSet, CategoryViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('tags', TagViewSet)
router.register('category', CategoryViewSet)
urlpatterns = router.urls
