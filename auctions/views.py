from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category, Watchlist
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html", {"listings": Listing.objects.filter(is_active=True)})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def category(request):
    return render(request, "auctions/category.html", {"categories": Category.objects.all()})


def category_listing(request, id):
    return render(request, "auctions/category_listing.html", {"listings": Listing.objects.filter(category=id), "category": Category.objects.get(id=id)})


def listing(request, id):
    requested_listing = Listing.objects.get(id=id)
    current_bid = requested_listing.bids.order_by("amount").last()

    try:
        watchlist = Watchlist.objects.get(listing=requested_listing, user=request.user)
        is_in_watchlist = True
    except:
        is_in_watchlist = False

    return render(request, 'auctions/listing.html', {"listing": requested_listing, "watchlist": is_in_watchlist, "current_bid":current_bid})


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        img_url = request.POST["image_url"]
        category_name = request.POST["category"]

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            category = None

       
        seller = request.user
        listing = Listing(title=title, description=description, starting_price=starting_price,
                          image_url=img_url, category=category, seller=seller)
        listing.save()

        starting_bid = Bid(bidder=seller, listing=listing, amount=starting_price)
        starting_bid.save()

        return redirect("listing", listing.id)

    else:
        return render(request, "auctions/listing_form.html", {"categories": Category.objects.all()})


@login_required
def watchlist_view(request):
    user = request.user
    watchlist_items = Watchlist.objects.filter(user=user)
    listings = [item.listing for item in watchlist_items]
    return render(request, "auctions/watchlist.html", {"listings": listings})


@login_required
def watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)

    try:
        watchlist_item = Watchlist.objects.get(user=user, listing=listing)
        watchlist_item.delete()
        messages.success(request, "removed from watchlist")
    except Watchlist.DoesNotExist:
        Watchlist.objects.create(user=user, listing=listing)
        messages.success(request, "added to watchlist")

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def bid(request,  listing_id):
    user_id = request.user.id
    if request.method == 'POST':

        listing = Listing.objects.get(id=listing_id)

        if not listing.is_active:
            messages.error(request, "This listing is not active.")
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        try:
            bidder = User.objects.get(id=user_id)
            price = request.POST["price"]
            highest_bid = Bid.objects.filter(
                listing=listing).order_by("amount").last()

            if not price:
                price = "0"

            if price.replace(".", "", 1).isdigit():
                price = float(price)
            else:
                raise ValueError("Your input is invalid, try again :)")

            if price > highest_bid.amount:
                listing.bids.create(bidder=bidder, listing=listing, amount=price)
            else:
                raise ValueError(
                    f'Your bid price should be greater than ${highest_bid}')
        except ValueError as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def close(request, listing_id):
    user= request.user

    listing = Listing.objects.get(id=listing_id)
    if listing.seller.id == user.id:
        if not listing.is_active:
            messages.error(request, "The listing is already closed.")
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        listing.is_active = False

        # winning_bid = listing.get_current_price()
        
        # winning_bid.is_win = True
        listing.save()
        messages.success(request, "The listing is closed.")
        return HttpResponseRedirect(reverse("index"))

    messages.error(request, "You are not allowed to close this listing.")
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def comment(request, listing_id):
    if request.method == "POST":
        writer = User.objects.get(id=request.user.id)
        listing = Listing.objects.get(id=listing_id)
        Comment.objects.create(
            writer=writer, content=request.POST["content"], listing=listing)

        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    else:
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
