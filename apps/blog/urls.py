from rest_framework.routers import SimpleRouter
from apps.blog.views import PostViewSet, TagViewSet, CategoryViewSet

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('tags', TagViewSet)
router.register('category', CategoryViewSet)
urlpatterns = router.urls
