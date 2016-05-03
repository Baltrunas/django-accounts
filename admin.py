from django.contrib import admin

from .models import User
from .models import Order
from .models import OrderItem
from .models import Valute
from .models import PromoCode


class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'email', 'date_joined']
	search_fields = ['username']

admin.site.register(User, UserAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
	list_display = ['user', 'created_at', 'status', 'name', 'email', 'phone', 'comment', 'retail_price', 'discount_price', 'accounting']
	list_editable = ['accounting']
	list_filter = ['status', 'user']
	inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['user', 'order', 'content_object', 'retail_price', 'discount_price', 'count']
	list_filter = ['user', 'order', 'count']

admin.site.register(OrderItem, OrderItemAdmin)


class ValuteAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'rate']

admin.site.register(Valute, ValuteAdmin)


class PromoCodeAdmin(admin.ModelAdmin):
	list_display = ['name', 'code', 'discount_type', 'discount_value', 'limit', 'active', 'active_from', 'active_before', 'sum_up', 'only_registered', 'one_per_user']
	list_filter = ['discount_type', 'active', 'active_from', 'active_before', 'sum_up', 'only_registered', 'one_per_user']
	search_fields = ['name', 'code', 'description']

admin.site.register(PromoCode, PromoCodeAdmin)