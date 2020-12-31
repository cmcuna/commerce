from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    cat = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.cat}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=64)
    #category = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="CategoryList")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserList")
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"Title: {self.title}    Desc: {self.description}    Price: {self.price}"

    @property #this lets us access as property and not as attribute.
    def imageURL(self): #function to error handle page error when an image url is not defined. 'imageURL' is now our attribute name (aka Listing.imageURL)
        try:
            url = self.image.url #first, query the url
        except:
            url = '' #if no url for image, give it an empty string that way we can still render image field
        return url

class Comment(models.Model):
    comment = models.CharField(max_length=164)
    parent = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingParent")

    def __str__(self):
        return f"{self.comment}"

class Watchlist(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistUserParent")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlistlistingParent")

    def __str__(self):
        return f"{self.user} {self.listing}"