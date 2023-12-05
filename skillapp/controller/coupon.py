from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from skillapp.models import Coupon

@login_required(login_url = 'login')
def upload_coup(request):
    if request.method == "POST":
        coupon = request.POST['coupon'].lower()
        discount = request.POST['discount']

        if Coupon.objects.filter(coupon_code = coupon).exists():
            messages.error(request, 'Coupon Exists')
            return redirect('admin_dash')
        else:
            coup = Coupon.objects.create(coupon_code = coupon, discount = discount)
            messages.success(request, 'Coupon Created Successfully')
            return redirect('admin_dash')

@login_required(login_url = 'login')
def validate_coupon(request):
    if request.method == "POST":
        coupon = request.POST.get('coupon').lower()
        
        try:
            coupon = get_object_or_404(Coupon, coupon_code = coupon)
        except Coupon.DoesNotExist:
            return JsonResponse({'error' : 'Invalid Coupon Code'})
        
        discount = coupon.discount

        return JsonResponse({'discount' : float(discount)})
    else:
        return JsonResponse({'error' : 'Invalid Coupon Code'})
