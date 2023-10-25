from rest_framework import serializers
from ...models import Customer


class CustomerSerializerList(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "address",
            "start_date"
        )


class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)

    """
    Serializador para el modelo `Customer`.

    **Validaciones:**

    * `first_name` y `last_name` deben ser cadenas de caracteres no vacías.
    * `address` debe ser una cadena de caracteres no vacía.
    """

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "address",
        )

    # Validaciones

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("El apellido no puede estar vacío.")
        return value

    def validate_address(self, value):
        if not value:
            raise serializers.ValidationError("La dirección no puede estar vacía.")
        return value

    def create(self, validated_data):
        return Customer.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            address=validated_data["address"],
        )


class CustomerSerializerUpdate(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance
