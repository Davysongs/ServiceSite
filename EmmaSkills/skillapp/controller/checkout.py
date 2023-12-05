from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from skillapp.models import Profile, Order, Cart, Market, OrderItem
from django.contrib.auth.models import User
from django.conf import settings
from random import randint
import requests

def placeorder(request):
    if request.method == "POST":
        
        currentuser = User.objects.filter(id = request.user.id).first()
        
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('first_name')
            currentuser.last_name = request.POST.get('last_name')
            currentuser.save()

        if not Profile.objects.filter(user = request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.postcode = request.POST.get('postcode')
            userprofile.save()
            
        user = Profile.objects.get(user = request.user)
        neworder = Order()
        neworder.user = request.user
        neworder.fullname = request.user.last_name + ' ' + request.user.first_name
        neworder.email = request.POST.get('email')
        neworder.phone = user.phone
        neworder.amount_paid = request.POST.get('amount')
        neworder.payment_mode = request.POST.get('payment_mode')
        
        # Generate transaction reference
        reference = "paystack" + str(randint(1111111, 9999999))

        # Create payload for Paystack payment initialization
        payload = {
            "email": neworder.email,
            "amount": int(float(neworder.amount_paid) * 100),  # Paystack API accepts amount in kobo
            "reference": reference,
            "callback_url": request.build_absolute_uri('/paystack/callback/'),
            }

        # Make a POST request to Paystack API for payment initialization
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        paystack_init_url = "https://api.paystack.co/transaction/initialize"
        response = requests.post(paystack_init_url, headers=headers, json=payload)

        # Check if the payment initialization was successful
        if response.status_code == 200:
            # Extract the authorization URL from the response
            authorization_url = response.json().get("data").get("authorization_url")

            # Save the transaction reference in the order model
            neworder.transaction_ref = reference
            neworder.save()
            
            order_items = Cart.objects.filter(user = request.user)
            for item in order_items:
                OrderItem.objects.create(
                    order = neworder,
                    product = item.product,
                    price = item.product.selling_price,
                    quantity = item.product_qty
                )
                
                orderproduct = Market.objects.filter(id = item.product.id)
                orderproduct.quantity -= item.product_qty  # Update available quantity
                orderproduct.save()

                # Generate a unique tracking number (alternative approach)
                trackno = 'skillsorder' + str(randint(1111111, 9999999))
                while Order.objects.filter(tracking_no = trackno).exists():
                    trackno = 'skillsorder' + str(randint(1111111, 9999999))

                neworder.tracking_no = trackno
                neworder.save()
                messages.success(request, 'Your order has been placed successfully')

                # Delete items from the cart after successful order placement
                Cart.objects.filter(user = request.user).delete()

                # Redirect the user to the Paystack authorization URL
                return redirect(authorization_url)
        else:
            # Handle the case where payment initialization failed
            messages.error(request, 'Payment initialization failed. Please try again.')
            return HttpResponse('Payment initialization failed. Please try again.')

    # trackno = 'emmaskill' + str(randint(1111111, 9999999))
    # while Order.objects.filter(tracking_no=trackno).exists():
    #     trackno = 'emmaskill' + str(randint(1111111, 9999999))
        
    #     neworder = Order()
    #     neworder.tracking_no = trackno
    #     neworder.save()

    #     neworderitems = Cart.objects.filter(user = request.user)
    #     for item in neworderitems:
    #         OrderItem.objects.create(
    #             order=neworder,
    #             product=item.product,
    #             price=item.product.selling_price,
    #             quantity=item.quantity
    #         )

    #         orderproduct = Market.objects.filter(id=item.product_id).first()
    #         orderproduct.quantity -= item.product_qty  # Update available quantity
    #         orderproduct.save()
            
    #     Cart.objects.filter(user=request.user).delete()
    #     messages.success(request, 'Your order has been placed successfully')
        
    #     return redirect('checkout')

    
def paystack_callback(request):
    # Retrieve the transaction reference from the query parameters
    transaction_ref = request.GET.get('transaction_ref')
    order = Order.objects.filter(tracking_no = transaction_ref).first()

    # Make a GET request to Paystack API for transaction verification
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    paystack_verify_url = f"https://api.paystack.co/transaction/verify/{transaction_ref}"
    response = requests.get(paystack_verify_url, headers=headers)

    # Check if the transaction verification was successful
    if response.status_code == 200:
        # Extract the transaction status from the response
        transaction_status = response.json().get("data").get("status")

        # Perform necessary actions based on the transaction status
        if transaction_status == "success":
            # Update the order status to indicate successful payment
            order = Order.objects.filter(tracking_no=transaction_ref).first()
            order.status = "paid"
            order.save()

            # Perform other actions like sending confirmation emails, etc.
            messages.success(request, 'Payment successful. Your order has been placed.')
        else:
            messages.error(request, 'Payment failed. Please try again.')
    return redirect('user_dash')