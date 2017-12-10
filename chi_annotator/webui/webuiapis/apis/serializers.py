from rest_framework import serializers

from apis.apiresponse import APIResponse
from apis.mongomodel import AnnotationData


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
        return instance


class AnnotationDataSerializer(serializers.Serializer):
    text = serializers.CharField()
    label = serializers.CharField()
    uuid = serializers.CharField()
    dataset_id = serializers.IntegerField()
    time_stamp = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return AnnotationData(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.text = validated_data.get('text', instance.text)
        instance.label = validated_data.get('label', instance.label)
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.dataset_id = validated_data.get('dataset_id', instance.dataset_id)
        instance.time_stamp = validated_data.get('time_stamp', instance.time_stamp)
        return instance
