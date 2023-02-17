from rest_framework import serializers
from django.core.exceptions import SuspiciousOperation
from advertising.constants import PAID
from advertising.models import Advertising


class CreateAdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = ['title', 'description', 'category']

    def create(self, validated_data):
        user = self.context['request'].user
        advertising = Advertising(**validated_data)
        advertising.author = user
        advertising.save()
        return advertising


class AdvertisingSerializer(CreateAdvertisingSerializer):
    class Meta:
        model = Advertising
        fields = CreateAdvertisingSerializer.Meta.fields + ['id', 'author',
                                                            'status']


class UpdateStatusAdvertising(serializers.Serializer):
    ids = serializers.ListField(child=serializers.PrimaryKeyRelatedField(
        queryset=Advertising.objects.all()), write_only=True)
    status = serializers.CharField(max_length=1)
    price = serializers.DecimalField(
        max_digits=12, decimal_places=2, default=50
    )

    def create(self, validated_data):
        return validated_data.get('ids')

    def apply_changes_to_instance(self, instance):
        status = self.validated_data.get('status')
        instance.status = status

        if status == PAID:
            user = self.context['request'].user
            price = self.validated_data.get('price')
            if user.wallet - price < 0:
                raise SuspiciousOperation(f"Недостаточно средств на балансе "
                                          f"для оплаты - {instance.title}")
            user.wallet -= price
            instance.author.wallet += price
            user.save()
            instance.author.save()

        instance.save()
        return instance
