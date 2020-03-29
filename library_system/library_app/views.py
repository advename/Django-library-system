from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .models import Book, BookLoan
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    # books_loaned = BookLoan.objects.filter(returned_timestamp__isnull=True)
    # books = Book.objects.all().exclude(bookloan__book=Book.id)
    # https://docs.djangoproject.com/en/3.0/topics/db/queries/#spanning-multi-valued-relationships
    # books = Book.objects.all()
    # books = Book.objects.filter(bookloan__returned_timestamp__isnull=True)
    books = Book.objects.filter(is_available=True)
    context = {"books": books}
    return render(request, "library_app/index.html", context)
