from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'status', 'failure_reason', 'created_at')

    def validate(self, data):
        user = self.context['request'].user
        cost = data['quantity'] * 2 # 2 Rupees per task
        if user.balance < cost:
            raise serializers.ValidationError("Insufficient balance.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        cost = validated_data['quantity'] * 2
        user.balance -= cost
        user.save()
        validated_data['user'] = user
        return super().create(validated_data)
