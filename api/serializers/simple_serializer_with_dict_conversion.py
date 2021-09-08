from rest_framework import serializers


class SimpleSerializerWithDictConversion(serializers.Serializer):
    def to_dict(self):
        self.is_valid()
        return self.validated_data

    def create(self, validated_data):
        return self.to_dict()

    def update(self, instance, validated_data):
        return self.to_dict()
