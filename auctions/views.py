from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Category, Comment, Watchlist

def watchlist(request, user_id):
    activeUser = User.objects.get(id=user_id)
    userWatchList = Listing.objects.filter(user_id=activeUser.id) #activeUser variable above has attribute of 'id': we also need to pull in 'user' attributes (maybe vai select_related)
    return render(request, "auctions/watchlist.html", {
        "watchlist": userWatchList #pull data from categories database table
    })

def category(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all() #pull data from categories database table
    })

def singleCategory(request, category_id):
    return render(request, "auctions/singleCategory.html", {
        "category": Listing.objects.filter(category_id=category_id) #category_id is the variable sent from url, and also the name of the column in the database, but are two different variables here
        ,"catagoryTitle": Category.objects.get(id=category_id)
    })


def newlisting(request):
    cats = Category.objects.all()

    #create a POST (for sumbission of listing) and a GET
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        condition = request.POST["condition"]
        category = request.POST["category"] #text/word string is no longer valid, we have to input an ID bc we added it as a foreign key
        category_retrieve = Category.objects.get(cat=category) #get the single row from Category table in database where the string is equal
        category_id = category_retrieve.id #his ID value is what we want to save in the database due to our foreign key
        # Attempt to save new listing data
        try:
            newlist = Listing.objects.create(title=title, description=description, price=price, condition=condition, category_id=category_id)
            newlist.save()
        except IntegrityError:
            return render(request, "auctions/newlisting.html", {
                #"cats": Category.objects.all(),
                #"cats": Category.objects.only('cat'),
                "cats":cats, #this list is not being used to popoulate html yet
                "message": "Error posting listing. Please try again or contact our help department."
            })
        return render(request, "auctions/successful.html", {
                "message": "Your item has successfuly posted. Thank you for selling with us today."
            })
    else:
        return render(request, "auctions/newlisting.html")

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None: #aka if user exists, then go to the index page
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html") #GET request for login, takes us to login page



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



def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(parent_id=listing_id) #get comments for a single listing (via the listings ID)
    count = comments.count() #get the number of comments currently exist for the single listing we are filtered to
    
    if request.method == "POST":
        newcomment = request.POST["comment"] #comment entered via user to post 

        # Attempt to save new listing data
        try:
            com = Comment.objects.create(comment=newcomment, parent_id=listing_id) #create object to be saved
            com.save() #save object into database
            """re-query comment count bc we added a new comment"""
            comments = Comment.objects.filter(parent_id=listing_id) #get comments for a single listing (via the listings ID)
            count = comments.count() #get the number of comments currently exist for the single listing we are filtered to
        except IntegrityError:
            return render(request, "auctions/listing.html", {
                "message": "Error posting commnet. Please try again or contact our help department."
            })
        return render(request, "auctions/listing.html", {
            "listing": listing
            ,"comments": comments
            ,"count": count
        })
    else:
        #listing = Listing.objects.get(id=listing_id)
        return render(request, "auctions/listing.html", {
            "listing": listing
            ,"comments": comments
            ,"count": count
        })



