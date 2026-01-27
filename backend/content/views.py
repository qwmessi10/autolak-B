from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import HomePageConfig, FAQ, SystemConfig, SEOArticle
from .serializers import HomePageConfigSerializer, FAQSerializer, SystemConfigSerializer, SEOArticleSerializer

class ImageUploadView(views.APIView):
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        if 'image' not in request.data:
            return Response({'error': 'No image provided'}, status=400)
        
        image = request.data['image']
        # Simple saving mechanism. For better organization, could use a model, but saving directly to media is fine for wysiwyg
        # We can use Django's default storage
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        import os
        
        path = default_storage.save(f"uploads/{image.name}", ContentFile(image.read()))
        url = default_storage.url(path)
        
        # Ensure full URL if needed, but relative usually works if frontend handles it. 
        # But for markdown ![](), absolute is safer if frontend and backend are on different ports/domains (dev mode).
        # In dev mode, default_storage.url returns /media/..., so we need to prepend host.
        # But let's return the relative path and let frontend prepend or handle.
        # Actually, for markdown, full URL is best.
        
        full_url = request.build_absolute_uri(url)
        return Response({'url': full_url})

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
