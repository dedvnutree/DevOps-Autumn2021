from django.contrib import admin

from .models import Type, Brand, Furniture, FurnitureInstance
from send_mail.models import DelayedMail, MailRecipient


@admin.register(DelayedMail)
class MailAdmin(admin.ModelAdmin):
    pass


@admin.register(MailRecipient)
class RecipientAdmin(admin.ModelAdmin):
    pass


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'description',)


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_type', 'brand', 'price', 'image', 'published')


@admin.register(FurnitureInstance)
class FurnitureInstanceAdmin(admin.ModelAdmin):
    list_display = ('furniture', 'status', 'delivery_day', 'buyer', id)
    # list_filter = ('furniture', 'status')
    fieldsets = (
        (None, {
            'fields': ('furniture', 'id')
        }),
        ('Availability', {
            'fields': ('status',  'buyer', 'delivery_day')
        }),
    )


admin.site.register(Type)
admin.site.register(Brand, BrandAdmin)