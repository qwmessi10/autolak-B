from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomePageConfigViewSet, FAQViewSet, SEOArticleViewSet, AdminHomePageConfigViewSet, AdminFAQViewSet, AdminSystemConfigViewSet, AdminSEOArticleViewSet

router = DefaultRouter()
router.register(r'home-config', HomePageConfigViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'seo-articles', SEOArticleViewSet)
router.register(r'admin/home-config', AdminHomePageConfigViewSet, basename='admin-home-config')
router.register(r'admin/faqs', AdminFAQViewSet, basename='admin-faq')
router.register(r'admin/system-config', AdminSystemConfigViewSet, basename='admin-system-config')
router.register(r'admin/seo-articles', AdminSEOArticleViewSet, basename='admin-seo-article')

urlpatterns = [
    path('', include(router.urls)),
]
