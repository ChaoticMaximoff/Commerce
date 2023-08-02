from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class AuctionList(models.Model):
    lister = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    image = models.CharField(max_length=2048, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auction_on = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True,blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title} item, listed by {self.lister.username}"


class Bid(models.Model):
    value = models.IntegerField()
    item = models.ForeignKey(AuctionList, related_name="bids", on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, related_name="biddings", on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=1500, null=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(AuctionList, related_name="comments", on_delete=models.CASCADE, null=True)


class Watchlist(models.Model):
    user_id = models.ForeignKey(User, related_name = "watchlist", on_delete=models.CASCADE)
    auction_id = models.ForeignKey(AuctionList, related_name = "watchlist_auction", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.username} watchlisted item {self.auction_id}"

