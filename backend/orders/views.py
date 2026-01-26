from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        order = serializer.save()
        self.send_to_telegram(order)

    def send_to_telegram(self, order):
        import json
        import requests
        from content.models import SystemConfig
        
        config = SystemConfig.objects.first()
        if not config or not config.telegram_bot_token or not config.telegram_chat_id:
            print("Telegram config missing, skipping notification.")
            return

        payload = {
            'username': order.user.username,
            'task_id': order.task_id,
            'video_type': order.video_type,
            'video_link': order.video_link,
            'title': order.title,
            'quantity': order.quantity
        }
        
        message = (
            f"📦 *New Order Received*\n"
            f"👤 User: `{payload['username']}`\n"
            f"🆔 Task ID: `{payload['task_id']}`\n"
            f"📺 Type: {payload['video_type']}\n"
            f"🔗 Link: {payload['video_link']}\n"
            f"📝 Title: {payload['title']}\n"
            f"🔢 Quantity: {payload['quantity']}"
        )
        
        url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
        data = {
            "chat_id": config.telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 200:
                print("Successfully sent to Telegram.")
            else:
                print(f"Failed to send to Telegram: {response.text}")
        except Exception as e:
            print(f"Error sending to Telegram: {str(e)}")


class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
