from django.db import models
from enum import Enum
from django.utils.translation import gettext_lazy as _
from .managers import CustomerFilters, WorkerOrdersFilters


class Customer(models.Model):
    """
    Modelo de base de datos para clientes.

    **Atributos:**

    * id: Identificador único del cliente.
    * first_name: Nombre del cliente.
    * last_name: Apellido del cliente.
    * address: Dirección del cliente.
    * start_date: Fecha de inicio del cliente.
    * end_date: Fecha de finalización del cliente.
    * is_active: Estado del cliente.
    * created_at: Fecha de creación del cliente.
    """

    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    objects_filters = CustomerFilters()

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"


class WorkOrder(models.Model):
    """
    Modelo de base de datos para órdenes de trabajo.

    **Atributos:**

    * id: Identificador único de la orden de trabajo.
    * customer_id: Identificador de la cuenta de cliente.
    * title: Título de la orden de trabajo.
    * planned_date_begin: Fecha de inicio planificada de la orden de trabajo.
    * planned_date_end: Fecha de finalización planificada de la orden de trabajo.
    * status: Estado de la orden de trabajo.
    * created_at: Fecha de creación de la orden de trabajo.
    """

    class StatusChoises(models.TextChoices):
        NEW = "NEW", _("New")
        DONE = "DONE", _("Done")
        CANCELLED = "CANCELLED", _("Cancelled")

    class TypeOrder(models.TextChoices):
        MANTENIMIENTO = "MANTENIMIENTO", _("Mantenimiento")
        PLANEACION = "PLANEACION", _("Planeacion")
        LIMPIEZA = "LIMPIEZA", _("Limpieza")

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, null=False)
    planned_date_begin = models.DateTimeField(null=False)
    planned_date_end = models.DateTimeField(null=False)
    status = models.CharField(
        choices=StatusChoises.choices,
        default=StatusChoises.NEW,
        max_length=15,
        null=False,
    )
    type_order = models.CharField(
        max_length=15, choices=TypeOrder.choices, default=TypeOrder.PLANEACION
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    objects_filters = WorkerOrdersFilters()

    class Meta:
        verbose_name = "work_order"
        verbose_name_plural = "work_orders"

    def get_status(self) -> StatusChoises:
        return self.StatusChoises[self.status]

    def get_type_order(self, value) -> TypeOrder:
        return self.TypeOrder[value]
