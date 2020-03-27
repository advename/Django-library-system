from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as dj_login
from django.http import HttpResponseRedirect


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
