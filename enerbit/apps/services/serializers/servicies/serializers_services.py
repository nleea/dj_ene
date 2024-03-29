from rest_framework import serializers
from rest_framework.fields import empty
from ...models import WorkOrder
from django.core.exceptions import ValidationError
from ..customers.serializers_customers import CustomerSerializerList


TYPE_ORDER = (
    ("MANTENIMIENTO", "Mantenimiento"),
    ("PLANEACION", "Planeacion"),
    ("LIMPIEZA", "Limpieza"),
)

class WorkOrderSerializer(serializers.Serializer):
    """
    Serializador para el modelo `WorkOrder`.

    **Validaciones:**

    * `customer_id` debe ser un identificador de cliente válido.
    * `title` debe ser una cadena de caracteres no vacía.
    * `planned_date_begin` y `planned_date_end` deben ser fechas válidas.
    """

    customer = serializers.IntegerField(write_only=True)
    title = serializers.CharField(write_only=True)
    planned_date_begin = serializers.DateTimeField(write_only=True)
    planned_date_end = serializers.DateTimeField(write_only=True)
    type_order = serializers.ChoiceField(choices=TYPE_ORDER,required=False)


    class Meta:
        fields = (
            "customer",
            "title",
            "planned_date_begin",
            "planned_date_end",
            "type_order",
        )

    def validate(self, data):
        planned_date_begin = data["planned_date_begin"]
        planned_date_end = data["planned_date_end"]

        difference = planned_date_end - planned_date_begin

        if difference.total_seconds() / 3600 > 2:
            raise ValidationError(
                {
                    "planned_date_end": "The difference between the planned start and end dates should not be greater than 2 hours."
                }
            )

        return data

    def get_status_display(self, obj) -> str:
        return obj.get_status().label

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("the title can't be empty")
        return value

    def create(self, validated_data):
        return WorkOrder.objects.create(
            customer_id=validated_data["customer"],
            title=validated_data["title"],
            planned_date_begin=validated_data["planned_date_begin"],
            planned_date_end=validated_data["planned_date_end"],
            type_order=validated_data["type_order"]
        )


class WorkOrderSerializerList(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)
    planned_date_begin = serializers.DateTimeField(read_only=True)
    planned_date_end = serializers.DateTimeField(read_only=True)
    status_display = serializers.SerializerMethodField()
    customer = CustomerSerializerList(read_only=True, context={"orders": True})
    type_order = serializers.CharField(read_only=True)

    def __init__(self, instance=None, data=..., **kwargs):
        context = kwargs.get("context", {})
        super().__init__(instance, data, **kwargs)

        order = context.get("customer", False)

        if order:
            self.fields.pop("customer")

    class Meta:
        fields = (
            "id",
            "title",
            "planned_date_begin",
            "planned_date_end",
            "status_display",
            "customer",
            "type_order",
        )

    def get_status_display(self, obj) -> str:
        return obj.get_status().label


STATUS_CHOISES = (("NEW", "New"), ("DONE", "Done"), ("CANCELLED", "Cancelled"))



class WorkOrderSerializerUpdate(serializers.Serializer):
    """
    Serializador para el modelo `WorkOrder`.

    **Validaciones:**

    * `customer_id` debe ser un identificador de cliente válido.
    * `title` debe ser una cadena de caracteres no vacía.
    * `planned_date_begin` y `planned_date_end` deben ser fechas válidas.
    """

    title = serializers.CharField(required=False)
    planned_date_begin = serializers.DateTimeField(required=False)
    planned_date_end = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(choices=STATUS_CHOISES, required=False)
    type_order = serializers.ChoiceField(choices=TYPE_ORDER,required=False)


    class Meta:
        fields = ("title", "planned_date_begin", "planned_date_end", "type_order")

    def validate_status(self, value):
        choises = [x[0] for x in STATUS_CHOISES]

        if value not in choises:
            raise serializers.ValidationError(
                f"Status no coincide, los posibles son: {choises}"
            )
        return value

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.planned_date_begin = validated_data.get(
            "planned_date_begin", instance.planned_date_begin
        )
        instance.planned_date_end = validated_data.get(
            "planned_date_end", instance.planned_date_end
        )
        instance.status = validated_data.get("status", instance.status)
        instance.type_order = validated_data.get("type_order", instance.type_order)

        difference = instance.planned_date_end - instance.planned_date_begin

        if difference.total_seconds() / 3600 > 2:
            raise ValidationError(
                {
                    "planned_date_end": "The difference between the planned start and end dates should not be greater than 2 hours."
                }
            )

        instance.save()
        return instance
