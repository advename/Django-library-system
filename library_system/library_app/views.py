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
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "library_app/index.html", context)


@login_required
def loan_item(request, type, id):
    if type == "book":
        book = get_object_or_404(Book, id=id)

        # 1. Get all records with the requested book id
        # 2. Of all those books, get the ones who have a returned_timestamp with value NULL (this means that the book is loaned)
        # 3. Get the count number of it, which we can use to do an if else statement on
        #           BookLoaned1 -> loaned_timestamp = 3273193712; returned_timestamp = 324324324234324
        #           BookLoaned2 -> loaned_timestamp = 3273193712; returned_timestamp = 234234324324324
        #           BookLoaned3 -> loaned_timestamp = 3273193712; returned_timestamp = NULL
        loaned_books_list = BookLoan.objects.filter(
            book=book).filter(returned_timestamp__isnull=True).count()

        # If the query returns 0, then the book is not loaned at the moment
        if loaned_books_list == 0:
            BookLoan.objects.create(book=book, user=request.user)

    return HttpResponseRedirect(reverse("library_app:index"))
