from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth import authenticate, login as dj_login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from library_app.models import Item, ItemLoan
from django.utils import timezone

item_limit = 2


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
    # Show all the items a user has loaned

    # From item, get
    user = request.user  # currently logged in user
    itemloans = ItemLoan.objects.filter(user=user)
    context = {"itemloans": itemloans, "user": user}
    return render(request, "user_app/profile.html", context)


@login_required
def loan_item(request, type, id):
    # The type parameter is currently not used, but you never know... :-)
    item = get_object_or_404(Item, id=id)

    # 1. Get all records with the requested item id
    # 2. Of all those items, get the ones who have a returned_timestamp with value NULL (this means that the item is loaned)
    # 3. Get the count number of it, which we can use to do an if else statement on
    #           itemLoaned1 -> loaned_timestamp = 3273193712; returned_timestamp = 324324324234324
    #           itemLoaned2 -> loaned_timestamp = 3273193712; returned_timestamp = 234234324324324
    #           itemLoaned3 -> loaned_timestamp = 3273193712; returned_timestamp = NULL
    loaned_items_list = ItemLoan.objects.filter(
        item=item).filter(returned_timestamp__isnull=True).count()

    # If the query returns 0, then the item is not loaned at the moment -> available
    if loaned_items_list == 0:

        # Check if we have reached the max amount of items the user can rent
        items_loaned_amount = (ItemLoan.objects.filter(
            user=request.user) & ItemLoan.objects.filter(returned_timestamp__isnull=True)).count()

        if items_loaned_amount < item_limit:
            item.is_available = False
            item.save()
            ItemLoan.objects.create(item=item, user=request.user)

    return HttpResponseRedirect(reverse("library_app:index"))


@login_required
def return_item(request, type, id):
    # The type parameter is currently not used, but you never know... :-)
    item = get_object_or_404(
        Item, id=id, itemloan__returned_timestamp__isnull=True, itemloan__user=request.user)

    item.is_available = True
    item.save()
    loaned_item = ItemLoan.objects.filter(
        item=item).get(returned_timestamp__isnull=True)
    loaned_item.returned_timestamp = timezone.now()
    loaned_item.save()

    return HttpResponseRedirect(reverse("user_app:profile"))
