from django.urls import path
from . import views

app_name = "user_app"

urlpatterns = [
    path("", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("administrator/", views.administrator, name="administrator"),
    path("loan/<str:type>/<int:id>", views.loan_item, name="loan_item"),
    path("return/<str:type>/<int:id>/", views.return_item, name="return_item"),
]
