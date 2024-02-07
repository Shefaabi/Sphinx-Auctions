from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:id>", views.listing, name="listing"),
    path("listings/create", views.create_listing, name="create_listing"),
    path("category", views.category, name="category"),
    path("category/<int:id>", views.category_listing, name="category_listing"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist, name="handle_watchlist"),
    path("listings/<int:listing_id>/comment", views.comment, name="comment"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close"),
]
