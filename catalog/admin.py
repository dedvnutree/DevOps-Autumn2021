from django.contrib import admin

from .models import Type, Brand, Furniture, FurnitureInstance


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'description',)


# class FurnitureInstanceInline(admin.TabularInline): #не работает хз почему
#     model = FurnitureInstance


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_type')
    #inlines = [FurnitureInstanceInline]


@admin.register(FurnitureInstance)
class FurnitureInstanceAdmin(admin.ModelAdmin):
    list_display = ('furniture', 'status', 'buyer', id)
    list_filter = ('furniture', 'status')
    fieldsets = (
        (None, {
            'fields': ('furniture', 'id')
        }),
        ('Availability', {
            'fields': ('status',  'buyer')
        }),
    )


admin.site.register(Type)
admin.site.register(Brand, BrandAdmin)