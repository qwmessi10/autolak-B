from rest_framework import serializers
from .models import HomePageConfig, FAQ, SystemConfig, SEOArticle

class HomePageConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageConfig
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = '__all__'

class SEOArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOArticle
        fields = '__all__'
