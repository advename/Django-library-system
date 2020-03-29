from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .models import Item, ItemLoan
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):

    items = Item.objects.filter(is_available=True)
    context = {"items": items}
    return render(request, "library_app/index.html", context)
