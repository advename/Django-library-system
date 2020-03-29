from django.contrib import admin

from .models import Book, BookLoan

# Customize which fields to display in the admin area


class BookLoanAdmin(admin.ModelAdmin):
    readonly_fields = ("loaned_timestamp",)
    fields = ("user", "book", "loaned_timestamp", "returned_timestamp")


# Register your the models with the custom fields display
admin.site.register(Book)
admin.site.register(BookLoan, BookLoanAdmin)
