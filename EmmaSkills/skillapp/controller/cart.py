from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from skillapp.models import Profile, Market, Cart, Coupon

@login_required(login_url = 'login')
def addtocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Market.objects.get(id = prod_id)
            if(product_check):
                if(Cart.objects.filter(user = request.user.id, product_id = prod_id)):
                    return JsonResponse({'status' : 'Product Already in Cart'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user = request.user, product_id = prod_id, product_qty = prod_qty)
                        return JsonResponse({'status' : 'Product added successfully'})
                    else:
                        return JsonResponse({'status' : "Only " + str(product_check.quantity) + " quantity available"})
            else:
                return JsonResponse({'status' : 'No such product found '})
        else:
            return JsonResponse({'status' : 'Login to Continue'})
        
    return redirect('user_dash')

@login_required(login_url = 'login')
def cart(request):
    cart = Cart.objects.filter(user = request.user)
    coupon = Coupon.objects.all()
    context = {'cart' : cart, coupon : 'coupon'}
    return render(request, 'users/cart.html', context)

@login_required(login_url = 'login')
def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        prod_qty = int(request.POST.get('product_qty'))
        if(Cart.objects.filter(user = request.user, product_id = prod_id)):
            try:
                cart = Cart.objects.get(product_id=prod_id, user=request.user)
                cart.product_qty = prod_qty
                cart.save()
                return JsonResponse({'status': "Updated Successfully"})
            except Cart.DoesNotExist:
                return JsonResponse({'message': 'Cart item not found'}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required(login_url = 'login')
def deletecartitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user = request.user, product_id = prod_id)):
            cartitem = Cart.objects.get(product_id = prod_id, user = request.user)
            cartitem.delete()
            return JsonResponse({'status' : "Deleted Successfully"})
    return redirect('cart')