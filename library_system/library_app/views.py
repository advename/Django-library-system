from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .models import Book, BookLoan
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "library_app/index.html", context)


@login_required
def loan_item(request, type, id):
    if type == "book":
        book = get_object_or_404(Book, id=id)
        BookLoan.objects.create(book=book, user=request.user)

    return HttpResponseRedirect(reverse("library_app:index"))
