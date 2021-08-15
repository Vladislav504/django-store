from django.urls import path


from .views import WalletsRegisterView, WalletsLoginView, WalletsLoggingOutView, WalletsHomeView

urls = [
    path('', WalletsHomeView.as_view(), name='home'),
    path('register', WalletsRegisterView.as_view(), name='register'),
    path('login', WalletsLoginView.as_view(), name='login'),
    path('logout', WalletsLoggingOutView.as_view(), name='logout'),
]