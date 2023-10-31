from django.contrib.auth import get_user_model

from rest_framework import serializers

from main_app.models import Task, Category

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_fields(self):
        """Get the serializer fields and filter the 'category' field queryset based on the request user.

        This method retrieves the serializer fields and filters the 'category' field queryset
        to include only categories associated with the requesting user.

        If the user is not authenticated, the 'category' field queryset is set to empty,
        ensuring compatibility with Swagger documentation.
        """
        fields = super(TaskSerializer, self).get_fields()
        fields['category'].queryset = fields['category'].queryset.none()
        if self.context['request'].user.is_authenticated:
            fields['category'].queryset = fields['category'].queryset.filter(user=self.context['request'].user)
        return fields

    class Meta:
        model = Task
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = '__all__'
