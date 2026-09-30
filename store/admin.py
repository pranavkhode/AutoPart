from django.contrib import admin
from .models import Part, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('part_name', 'price', 'quantity', 'item_total')


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'part_number', 'price', 'stock', 'rating', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'part_number', 'description')
    list_editable = ('price', 'stock', 'is_available')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'full_name', 'phone', 'delivery_method', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'delivery_method', 'created_at')
    search_fields = ('order_id', 'full_name', 'phone', 'email')
    inlines = [OrderItemInline]
    readonly_fields = ('order_id', 'created_at')
