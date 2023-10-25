from rest_framework import serializers
from rest_framework.fields import empty
from django.core.exceptions import ValidationError


class BaseSerializers(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        

        update = kwargs.pop("update", None)

        if update:
            self.fields.pop("customer")
            self.fields.update("title", {"required": False})
            self.fields.update("planned_date_begin", {"required": False})
            self.fields.update("planned_date_end", {"required": False})
        
        super().__init__(instance, data, **kwargs)

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
