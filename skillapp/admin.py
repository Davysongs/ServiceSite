from django.contrib import admin
from .models import Profile, Booking, Market, Category, MartImage, Review, Cart, Coupon, Order, OrderItem

# Register your models here.
admin.site.register(Profile)
admin.site.register(Booking)
admin.site.register(Market)
admin.site.register(Category)
admin.site.register(MartImage)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(OrderItem)