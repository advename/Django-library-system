from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth import authenticate, login as dj_login,  logout as dj_logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from library_app.models import Item, ItemLoan
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


item_limit = {
    "book": 10,
    "magazine": 3
}


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

# Sign Up


def sign_up(request):
    context = {}
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_name = request.POST['username']
        email = request.POST['email']
        if password == confirm_password:
            if User.objects.create_user(user_name, email, password, is_staff=False):
                return HttpResponseRedirect(reverse('user_app:login'))
            else:
                context = {
                    'error': 'Could not create user account - please try again.'
                }
        else:
            context = {
                'error': 'Passwords did not match. Please try again.'
            }
    return render(request, 'user_app/sign_up.html', context)


@login_required
def profile(request, extraContext={}):
    context = {}
    context.update(extraContext)
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
        items_loaned_amount = ItemLoan.objects.filter(
            user=request.user, returned_timestamp__isnull=True, item__item_type=item.item_type).count()

        if items_loaned_amount < item_limit[item.item_type]:
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


@login_required
def change_password(request):
    context = {}

    # Only handle password updates on a Post request
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        # Check if the old password is correct
        if request.user.check_password(old_password):

            # Check if both passwords match
            if new_password1 == new_password2:
                user = get_object_or_404(User, username=request.user.username)
                user.set_password(new_password1)
                user.save()

                context = {"message": "Password successfully changed!"}

                # Stay logged in after a password change
                update_session_auth_hash(request, user)

            # Passwords do not match
            else:
                context = {"message": "Passwords do not match"}

        # Wrong old password
        else:
            context = {"message": "Wrong old password"}

    # redirect back to profile page with messages
    return profile(request, context)


@login_required
def administrator(request):
    context = {}
    # Show all the items a user has loaned

    # From item, get
    user = request.user  # currently logged in user
    itemloans = ItemLoan.objects.filter(
        returned_timestamp__isnull=True).order_by("loaned_timestamp")
    context = {"itemloans": itemloans}
    return render(request, "user_app/administrator.html", context)


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('user_app:login'))
