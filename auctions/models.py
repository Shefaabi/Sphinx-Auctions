from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=65)
    description = models.TextField()
    starting_price = models.FloatField()
    image_url = models.URLField(null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="listings", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
   

    def __str__(self):
        return f"{self.title} - {('Active' if self.is_active else 'Inactive' )}"
    
    def get_current_price(self):
        bid = self.bids.order_by("amount").last()
        current_price = self.starting_price if not bid else bid.amount
        return current_price
       



class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()
    

    def __str__(self):
        return f"Bid on {self.listing.title} by {self.bidder.username} for {self.amount}"
    


class Comment(models.Model):
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.writer.username} on {self.listing.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return f"{self.user.username} interested in {self.listing.title}"

