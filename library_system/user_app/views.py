from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth import authenticate, login as dj_login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from library_app.models import Book, BookLoan
from django.utils import timezone

book_limit = 2


# Create your views here.
def login(request):
    context = {}

    # Login request
    if request.method == "POST":
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])

        if user:
            # User login success
            dj_login(request, user)
            return HttpResponseRedirect(reverse("library_app:index"))

        else:
            # User login failed
            context = {"error_message": "Invalid username/password combination"}

    return render(request, "user_app/login.html", context)


@login_required
def profile(request):
    # Show all the books a user has loaned

    # From Book, get
    user = request.user  # currently logged in user
    bookloans = BookLoan.objects.filter(user=user)
    context = {"bookloans": bookloans, "user": user}
    return render(request, "user_app/profile.html", context)


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

        # If the query returns 0, then the book is not loaned at the moment -> available
        if loaned_books_list == 0:

            # Check if we have reached the max amount of books we can rent
            books_loaned_amount = (BookLoan.objects.filter(
                user=request.user) & BookLoan.objects.filter(returned_timestamp__isnull=True)).count()

            if books_loaned_amount < book_limit:
                book.is_available = False
                book.save()
                BookLoan.objects.create(book=book, user=request.user)

    return HttpResponseRedirect(reverse("library_app:index"))


@login_required
def return_item(request, type, id):
    # Check the type, book or magazine
    if type == "book":
        book = get_object_or_404(Book, id=id)

        # Check if we currently have loaned the book? (This means we have it inside BookLoan and the returned_timestamp has no value)
        booksloaned = BookLoan.objects.filter(
            book=book, returned_timestamp__isnull=True, user=request.user).count()
        if booksloaned > 0:
            # We are the ones who have loaned the requested book
            book.is_available = True
            book.save()
            loaned_book = BookLoan.objects.filter(
                book=book).get(returned_timestamp__isnull=True)
            loaned_book.returned_timestamp = timezone.now()
            loaned_book.save()

    return HttpResponseRedirect(reverse("user_app:profile"))
