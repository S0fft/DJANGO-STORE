from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display: list[str] = ('__str__', 'status', 'created')
    fields: list[str] = (
        'id', 'created',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'basket_history', 'status', 'initiator',
    )
    readonly_fields: list[str] = ('id', 'created')
