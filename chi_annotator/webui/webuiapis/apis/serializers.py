from rest_framework import serializers

from apis.apiresponse import APIResponse


class APIResponseSerializer(serializers.Serializer):
    data = serializers.CharField()
    code = serializers.IntegerField(read_only=True)
    message = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return APIResponse(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.data = validated_data.get('data', instance.data)
        instance.code = validated_data.get('code', instance.code)
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance
