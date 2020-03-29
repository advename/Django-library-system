from django.contrib import admin

from .models import Item, ItemLoan

# Customize which fields to display in the admin area


class ItemLoanAdmin(admin.ModelAdmin):
    readonly_fields = ("loaned_timestamp",)
    fields = ("user", "item", "loaned_timestamp", "returned_timestamp")


# Register your the models with the custom fields display
admin.site.register(Item)
admin.site.register(ItemLoan, ItemLoanAdmin)
