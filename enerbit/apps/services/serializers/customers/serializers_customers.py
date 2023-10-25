from rest_framework import serializers
from ...models import Customer


class WorkOrderSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)
    planned_date_begin = serializers.DateTimeField(read_only=True)
    planned_date_end = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        ref_name = "workerOrderList"


class CustomerSerializerList(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    workorder_set = WorkOrderSerializer(read_only=True, many=True)

    def __init__(self, instance=None, data=..., **kwargs):
        context = kwargs.get("context", {})
        super().__init__(instance, data, **kwargs)

        order = context.get("orders", False)

        if order:
            self.fields.pop("workorder_set")

    def to_representation(self, instance):
        results = super().to_representation(instance)

        if "workorder_set" in results:
            results["workorder"] = [x for x in results["workorder_set"]]
            del results["workorder_set"]
        return results

    class Meta:
        fields = ("id", "first_name", "last_name", "address", "start_date")


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

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance


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
