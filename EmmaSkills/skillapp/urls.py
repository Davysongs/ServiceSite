from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from skillapp.controller import cart, coupon, authview, wishlist, checkout

urlpatterns = [
    path('', views.index, name = 'index'),

    path('login', authview.login, name = 'login'),
    path('register', authview.register, name = 'register'),
    path('logout', authview.logout, name = 'logout'),

    path('a/dashboard', views.admin_dash, name = 'admin_dash'),
    path('a/users', views.users, name = 'users'),
    path('a/ud', views.ud, name = 'user_detail'),
    path('a/inbox', views.inbox, name = 'inbox'),
    path('a/upload', views.upload, name = 'upload'),

    path('u/dashboard', views.user_dash, name = 'user_dash'),
    path('u/profile', views.user_profile, name = 'user_profile'),
    path('u/order', views.order, name = 'order'),
    path('u/bookings', views.bookings, name = 'bookings'),
    path('fetch-booked-dates/', views.fetch_booked_dates, name='fetch_booked_dates'),
    path('u/marketplace', views.marketplace, name = 'marketplace'),
    path('u/product/<str:slug>', views.market, name = 'market'),

    path('coupon', coupon.upload_coup, name = "upload_coup"),
    path('validate_coupon', coupon.validate_coupon, name = "validate_coupon"),

    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('u/cart', cart.cart, name = "cart"),
    path('update-cart', cart.updatecart, name = "updatecart"),
    path('delete-cart-item', cart.deletecartitem, name = "deletecartitem"),

    # path("wishlist", wishlist.index, name="wishlist"),
    # path("add-to-wishlist", wishlist.addtowish, name="addtowish"),
    # path("deletewish", wishlist.deletewish, name="deletewish"),

    path('placeorder', checkout.placeorder, name="placeorder"),
    path('paystack/callback/', checkout.paystack_callback, name='paystack_callback'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'recover-password.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'reset_done.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)