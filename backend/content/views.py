from rest_framework import viewsets, permissions
from .models import HomePageConfig, FAQ, SystemConfig, SEOArticle
from .serializers import HomePageConfigSerializer, FAQSerializer, SystemConfigSerializer, SEOArticleSerializer

class HomePageConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomePageConfig.objects.all()
    serializer_class = HomePageConfigSerializer
    permission_classes = [permissions.AllowAny]

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]

class SEOArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SEOArticle.objects.all().order_by('-created_at')
    serializer_class = SEOArticleSerializer
    permission_classes = [permissions.AllowAny]

class AdminHomePageConfigViewSet(viewsets.ModelViewSet):
    queryset = HomePageConfig.objects.all()
    serializer_class = HomePageConfigSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminFAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminSystemConfigViewSet(viewsets.ModelViewSet):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminSEOArticleViewSet(viewsets.ModelViewSet):
    queryset = SEOArticle.objects.all().order_by('-created_at')
    serializer_class = SEOArticleSerializer
    permission_classes = [permissions.IsAdminUser]
