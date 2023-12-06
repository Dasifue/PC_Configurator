from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("register/", view=views.RegisterView.as_view(), name="register"),
    path("login/", view=views.LoginView.as_view(), name="login"),
    path("logout/", view=views.LogoutView.as_view(), name="logout"),
    path("user/profile/<int:pk>", view=views.UserDetailsView.as_view(), name="profile"),
    path("user/profile/update/", view=views.UpdateProfileView.as_view(), name="update"),
    path("user/password/change/", view=views.ChangePasswordView.as_view(), name="change_password"),
]