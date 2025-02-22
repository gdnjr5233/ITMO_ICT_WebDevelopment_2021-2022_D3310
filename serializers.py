from .models import *
from rest_framework import serializers

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'passport', 'salary', 'cell']


class ChickenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chicken
        fields = "__all__"


class ChickenRelatedSerializer(serializers.ModelSerializer):
    breed = serializers.StringRelatedField(read_only=True)
    cell = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Chicken
        fields = "__all__"


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ServiceRelatedSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)
    cell = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Service
        fields = "__all__"


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = "__all__"


class CellRelatedSerializer(serializers.ModelSerializer):
    row = serializers.StringRelatedField(read_only=True)
    tsekh = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cell
        fields = "__all__"


class ServiceNestedSerializer(serializers.ModelSerializer):
    username = NewUserSerializer()
    cell = CellSerializer()

    class Meta:
        model = Service
        fields = "__all__"


class ChickenNestedSerializer(serializers.ModelSerializer):
    breed = BreedSerializer()
    cell = CellSerializer()

    class Meta:
        model = Chicken
        fields = "__all__"