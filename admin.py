from django.contrib import admin

from .models import User
from .models import Order
from .models import OrderItem
from .models import Valute
from .models import Promo


class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'email', 'date_joined']
	search_fields = ['username']

admin.site.register(User, UserAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
	list_display = ['user', 'status', 'name', 'email', 'phone', 'comment', 'retail_price', 'wholesale_price', 'retail_price_with_discount']
	list_filter = ['status', 'user']
	inlines = [OrderItemInline]



admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['user', 'order', 'content_object', 'retail_price', 'wholesale_price', 'retail_price_with_discount', 'count']
	list_filter = ['user', 'order', 'count']

admin.site.register(OrderItem, OrderItemAdmin)


class ValuteAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'rate']

admin.site.register(Valute, ValuteAdmin)


admin.site.register(Promo)