from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Booking, Market, Category, MartImage, Review

# Create your views here.

# Homepage
def index(request):
    mart = Market.objects.all()
    context = {'mart' : mart }
    return render(request, 'index.html', context)

########################## Admin pages function ##############################
@login_required(login_url = 'login')
def admin_dash(request):
    user = User.objects.filter(is_superuser=False).order_by('-date_joined')
    if request.method == "POST":
        category = request.POST['category'].lower()

        if Category.objects.filter(category = category).exists():
            messages.error(request, 'Category Exists')
            return redirect('admin_dash')
        else:
            cat = Category.objects.create(category = category)
            messages.success(request, 'Category Created Successfully')
            return redirect('admin_dash')
            
    context = {"user" : user}
    return render(request, 'adm/admin.html', context)

@login_required(login_url = 'login')
def users(request):
    user = User.objects.all()
    context = {"user" : user}
    return render(request, 'adm/users.html', context)

@login_required(login_url = 'login')
def ud(request):
    return render(request, 'adm/ud.html')

@login_required(login_url = 'login')
def inbox(request):
    return render(request, 'adm/message.html')

@login_required(login_url = 'login')
def upload(request):
    category = Category.objects.all()
    if request.method == "POST":
        cat = request.POST['category'].lower()
        name = request.POST['name'].lower()
        oprice = request.POST['oprice']
        sprice = request.POST['sprice']
        qty = request.POST['qty']
        tag = request.POST['tag'].lower()
        trend = request.POST['trend']
        image = request.FILES.getlist('image')
        sdesc = request.POST['sdesc'].lower()
        desc = request.POST['desc'].lower()

        slug = name.replace(' ', '-')
        
        cate = Category.objects.get(category = cat)
        if Market.objects.filter(name = name).exists():
            messages.error(request, 'Product already added')
            return redirect('upload')
        else:
            Market.objects.create(category_id = cate.id, name = name, original_price = oprice, selling_price = sprice, tag = tag, sdesc = sdesc, desc = desc, trending = trend, quantity = qty, slug = slug)
            messages.error(request, 'Product Added Successfully')
        
        fetch_name = Market.objects.get(name = name)
        for i in image:
            img, created = Market.objects.get_or_create(name = fetch_name)
            img.image = i
            img.save()

            multi = MartImage(mart_name_id = fetch_name.id, image = i)
            multi.save()

    context = {'category' : category}
    return render(request, 'adm/upload.html', context)

############################### User pages function #############################
@login_required(login_url = 'login')
def user_dash(request):
    mart = Market.objects.all()
    book = Booking.objects.filter(user = request.user)
    show = Profile.objects.get(user = request.user)
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']

        store = Review.objects.create(name = request.user, email = request.user.email, subject = subject, message = message)
        body = {
			'Name': request.user, 
			'E-mail': request.user.email, 
			'Subject': subject, 
			'Message': message
			}
        content = "\n".join(f'{k}: {v}' for k,v in body.items())
        print(content)
        
        try:
            send_mail(subject, message, 'koladegeorge5@gmail.com', ['emaskills2@gmail.com', 'obikolade@gmail.com']) 
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect ("user_dash")
    context = {'mart' : mart, 'show' : show, 'book' : book}
    return render(request, 'users/index.html', context)

@login_required(login_url = 'login')
def user_profile(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        postcode = request.POST['postcode']
        state = request.POST['state']
        country = request.POST['country']
        image = request.FILES.get('image')

        user_model = User.objects.get(username = request.user)
        user_model.first_name = fname
        user_model.last_name = lname
        user_model.save()

        profile, created = Profile.objects.get_or_create(user = user_model)
        profile.first_name = fname
        profile.last_name = lname
        profile.email = email
        profile.phone = phone
        profile.address = address
        profile.city = city
        profile.postcode = postcode
        profile.state = state
        profile.country = country
        if image:
            profile.image = image
        profile.save()

    show = Profile.objects.get(user = request.user)    
    context = {"show" : show}
    return render(request, 'users/profile.html', context)

@login_required(login_url = 'login')
def order(request):
    show = Profile.objects.get(user = request.user)
    context = {'show' : show}
    return render(request, 'users/order.html', context)

@login_required(login_url = 'login')
def marketplace(request):
    show = Profile.objects.get(user = request.user)

    # Set up Paginator
    p = Paginator(Market.objects.all(), 20)
    page = request.GET.get('page')
    products = p.get_page(page)

    context = {'products' : products, "show" : show}
    return render(request, 'users/marketplace.html', context)

@login_required(login_url = 'login')
def market(request, slug):
    show = Profile.objects.get(user = request.user)
    mart = Market.objects.get(slug = slug)
    img = MartImage.objects.filter(mart_name = mart.id)
    context = {'mart' : mart, "img" : img, "show" : show}
    return render(request, 'users/mart-details.html', context)

@login_required(login_url = 'login')
def bookings(request):
    show = Profile.objects.get(user = request.user)
    if request.method == "POST":
        name = request.POST['name']
        purpose = request.POST['purpose']
        date = request.POST['date']
        time = request.POST['time']

        if Booking.objects.filter(date=date, time=time).exists():
            messages.error(request, 'The date and time already booked')
            return redirect('bookings')
        else:
            Booking.objects.create(user = request.user, name = name, reason = purpose, date = date, time = time)
            messages.success(request, 'Date and Time booked successfully')
            return redirect('bookings')
    
    booked = Booking.objects.filter(user = request.user)
    context = {"show": show, "booked" : booked}
    return render(request, 'users/bookings.html', context)

@login_required(login_url = 'login')
def fetch_booked_dates(request):
    # Query the database to retrieve booked dates
    booked_dates = Booking.objects.values_list('date', flat=True)

    # Convert the QuerySet to a list
    booked_dates_list = list(booked_dates)

    # Create a dictionary to hold the data
    data = {'booked_dates': booked_dates_list}

    # Return the data as JSON response
    return JsonResponse(data)

from django.shortcuts import redirect

@login_required(login_url = 'login')
def placeorder(request):
    pay_value = request.GET.get('pay', '')  # Retrieve the pay value from the URL
    # Additional logic for handling the order, if needed
    return redirect('checkout', pay=pay_value)
