from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),#if listing is put before this path, then category html won't be rendered, maybe it wanted int:listing_id?
    path("category/<int:category_id>", views.singleCategory, name="singleCategory"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("<int:listing_id>", views.listing, name="listing")
]
