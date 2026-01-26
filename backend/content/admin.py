from django.contrib import admin
from .models import HomePageConfig, FAQ, SystemConfig, SEOArticle

admin.site.register(HomePageConfig)
admin.site.register(FAQ)
admin.site.register(SystemConfig)
admin.site.register(SEOArticle)
