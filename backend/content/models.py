from django.db import models

class HomePageConfig(models.Model):
    slogan_text = models.CharField(max_length=255, default="Boost Your YouTube Channel", blank=True)
    slogan_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    
    intro_text = models.TextField(default="We help you grow...", blank=True)
    intro_flowchart = models.ImageField(upload_to='homepage/', blank=True, null=True)
    
    case_1_img = models.ImageField(upload_to='cases/', blank=True, null=True)
    case_2_img = models.ImageField(upload_to='cases/', blank=True, null=True)
    case_3_img = models.ImageField(upload_to='cases/', blank=True, null=True)
    case_4_img = models.ImageField(upload_to='cases/', blank=True, null=True)
    case_text = models.TextField(default="Our success stories", blank=True)

    class Meta:
        verbose_name = "Home Page Configuration"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

class SystemConfig(models.Model):
    telegram_bot_token = models.CharField(max_length=255, default="", blank=True)
    telegram_chat_id = models.CharField(max_length=255, default="", blank=True)

    class Meta:
        verbose_name = "System Configuration"

class SEOArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Markdown supported")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

