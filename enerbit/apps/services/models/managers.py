from django.db.models.manager import Manager


class CustomerFilters(Manager):
    def filterByStatus(self):
        return self.filter(is_active=True)

    def filterById(self, id):
        return self.filter(pk=id)


class WorkerOrdersFilters(Manager):
    def filterByDate(self, since, until):
        return self.filter(
            planned_date_begin__gte=since, planned_date_end__lte=until
        ).select_related("customer")

    def filterByState(self, status):
        return self.filter(status=status).select_related("customer")
