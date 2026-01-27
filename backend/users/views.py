from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, AdminUserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # Check if username or email already exists
        username = request.data.get('username')
        email = request.data.get('email')
        
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Risk Control: Check Cookie
        cookie = request.data.get('registration_cookie')
        if cookie:
            if User.objects.filter(registration_cookie=cookie).exists():
                return Response(
                    {"detail": "You have already registered an account on this device."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().create(request, *args, **kwargs)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_admin': user.is_staff,
            'balance': user.balance,
            'avatar_url': user.avatar_url
        })

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reward_contact(request):
    method = request.data.get('method')
    contact = request.data.get('contact')
    if method not in ['whatsapp', 'telegram'] or not contact:
        return Response({'detail': 'Invalid contact submission.'}, status=status.HTTP_400_BAD_REQUEST)
    user = request.user
    try:
        from decimal import Decimal
        import requests
        from content.models import SystemConfig
        user.balance = (user.balance or Decimal('0')) + Decimal('10')
        user.save()
        print(f"Rewarded 10 to {user.username} for contact: {method}={contact}")
        config = SystemConfig.objects.first()
        if config and config.telegram_bot_token and config.telegram_chat_id:
            message = (
                f"📇 Contact Submitted\n"
                f"👤 User: `{user.username}`\n"
                f"🔌 Method: {method}\n"
                f"📞 Contact: {contact}\n"
                f"💰 Bonus: ₹10 credited"
            )
            url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
            data = {"chat_id": config.telegram_chat_id, "text": message, "parse_mode": "Markdown"}
            try:
                resp = requests.post(url, json=data, timeout=5)
                if resp.status_code == 200:
                    print(f"Sent contact to Telegram for {user.username}")
                else:
                    print(f"Failed to send contact to Telegram: {resp.status_code} {resp.text}")
            except Exception as e:
                print(f"Error sending contact to Telegram: {str(e)}")
        return Response({'balance': str(user.balance)}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': 'Failed to reward contact.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
