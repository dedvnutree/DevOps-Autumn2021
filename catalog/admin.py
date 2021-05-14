from django.contrib import admin

from .models import Type, Brand, Furniture, FurnitureInstance


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'description',)


# class FurnitureInstanceInline(admin.TabularInline): #не работает хз почему
#     model = FurnitureInstance


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_type', 'image', 'published')
    #inlines = [FurnitureInstanceInline]


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