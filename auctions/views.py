from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import *


def index(request):
    listings = AuctionList.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


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
    

def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories,
        })
    else:
        lister = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        price = float(request.POST["price"])
        url = request.POST["url"]
        category_id = int(request.POST.get('category.id', 1))
        category = Category.objects.get(pk=category_id)
        listing = AuctionList.objects.create(lister=lister, title=title, description=description, price=price, category=category, image=url)
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    

def listing_view(request, listing_id):
    is_watchlist = False
    listing = AuctionList.objects.get(id=listing_id)
    comments = listing.comments.all()
    if request.user.is_authenticated:
        user = request.user

        try:
            Watchlist.objects.get(user_id=user, auction_id=listing)
        except:
            pass
        else:
            is_watchlist = True

    
    listing_bids = Bid.objects.filter(item=listing).order_by('-value')
    if len(listing_bids) > 0:
        min_bid = listing_bids[0].value +1
    else:
        min_bid =listing.price

    listing = AuctionList.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watchlist": is_watchlist,
        "min_bid" : min_bid,
        "comments":comments
    })


@login_required
def add_watchlist(request, listing_id):
    user = request.user
    listing = AuctionList.objects.get(id=listing_id)
    watchlist = Watchlist.objects.create(user_id = user, auction_id=listing)
    watchlist.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def remove_watchlist(request, listing_id):
    user = request.user
    listing = AuctionList.objects.get(id=listing_id)
    watchlist = Watchlist.objects.get(user_id=user, auction_id=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def bid(request, listing_id):
    user = request.user
    listing = AuctionList.objects.get(id=listing_id)
    bid_value = int(request.POST['bid'])
    bid = Bid.objects.create(value=bid_value, item=listing, bidder=user)
    bid.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def close_auction(request, listing_id):
    listing = AuctionList.objects.get(id=listing_id)
    listing.auction_on = False
    listing_bids = Bid.objects.filter(item=listing).order_by('-value')
    if(len(listing_bids) > 0):
        winner_id = listing_bids[0].bidder.id
        listing.winner = User.objects.get(pk=winner_id)
    listing.save()
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
        })


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = AuctionList.objects.filter(category = category)
    return render(request, 'auctions/index.html', {
        'category': category,
        'listings': listings
    })


@login_required
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist,
    })


@login_required
def comment(request, listing_id):
    listing = AuctionList.objects.get(id=listing_id)
    user = request.user
    text = request.POST["text"]
    comment = Comment.objects.create(user=user, text=text, item=listing)
    comment.save()
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))