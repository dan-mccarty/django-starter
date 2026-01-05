from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    # Simple payload for ping endpoints.
    message = serializers.CharField()


class ItemSerializer(serializers.Serializer):
    # Sample serializer for request/response bodies.
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, required=False)
    completed = serializers.BooleanField(default=False)


class ApiKeyCreateSerializer(serializers.Serializer):
    # Allows optional domain restrictions for the new API key.
    name = serializers.CharField(max_length=100)
    allowed_domains = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
    )


class ApiKeyResponseSerializer(serializers.Serializer):
    # Returns the raw API key once after creation.
    id = serializers.IntegerField()
    name = serializers.CharField()
    key = serializers.CharField()
    allowed_domains = serializers.ListField(child=serializers.CharField())
