from django.contrib.auth import get_user_model
from rest_framework import serializers
from main_app.models import Task, Category

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'url']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_fields(self):
        fields = super(TaskSerializer, self).get_fields()
        fields['category'].queryset = fields['category'].queryset.filter(user=self.context['request'].user)
        return fields

    class Meta:
        model = Task
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = '__all__'
