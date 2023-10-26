from rest_framework.views import APIView
from rest_framework.response import Response
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
from ...models import Customer, WorkOrder


class Analytics(APIView):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.values("id", "end_date")
        work_orders = WorkOrder.objects.values(
            "customer",
            "type_order",
            "status",
            "planned_date_begin",
            "planned_date_end",
        )

        data = pd.DataFrame(customers)
        data = data.merge(
            pd.DataFrame(work_orders),
            left_on="id",
            right_on="customer",
        )

        data["planned_date_begin"] = pd.to_datetime(data["planned_date_begin"])
        data["planned_date_end"] = pd.to_datetime(data["planned_date_end"])

        data["duration"] = data["planned_date_end"] - data["planned_date_begin"]

        data["duration"] = data["duration"].dt.components["hours"]

        fig, ax = plt.subplots()

        ax = sns.barplot(
            data=data,
            x="type_order",
            y="duration",
            hue="status",
            palette="pastel",
        )

        ax.set_xlabel("Tipo de orden de trabajo")
        ax.set_ylabel("Duración")
        ax.legend(
            ["Completada", "Cancelada"],
            loc="upper right",
            title="Estado",
        )

        ax.plot(
            data.groupby("type_order")["duration"].mean(),
            label="Tendencia",
            linestyle="dashed",
        )

        ax.legend(
            ["Completada", "Cancelada", "Tendencia (regresión lineal)"],
            loc="upper right",
            title="Estado",
        )

        return Response("R")
