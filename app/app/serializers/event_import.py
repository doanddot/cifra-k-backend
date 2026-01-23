from rest_framework import serializers


class EventImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        if not file.name.endswith(".xlsx"):
            raise serializers.ValidationError("Only .xlsx files are supported")
        return file