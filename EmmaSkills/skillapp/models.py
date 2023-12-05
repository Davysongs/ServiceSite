from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'Profile Pictures')
    first_name = models.CharField(max_length = 100, blank = False)
    last_name = models.CharField(max_length = 100, blank = False)
    email = models.EmailField()
    phone = models.CharField(blank = False, max_length = 11)
    address = models.CharField(blank = False, max_length = 200)
    city = models.CharField(blank = False, max_length = 200)
    country = models.CharField(blank = False, max_length = 200)
    postcode = models.CharField(blank = False, max_length = 200)
    state = models.CharField(blank = False, max_length=200)

    def __str__(self):
        return str(self.user)

    class Meta():
        db_table = 'User Profile'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, blank = False)
    reason = models.CharField(max_length = 100, blank = False)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.user)
    
    class Meta():
        db_table = 'Bookings'

class Category(models.Model):
    category = models.CharField(max_length = 100, blank = False)

    def __str__(self):
        return str(self.category)
    
    class Meta():
        db_table = 'Category'

class Market(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    slug = models.SlugField(max_length = 150, null = False, blank = False)
    name = models.CharField(max_length = 500, blank = False)
    tag = models.CharField(max_length = 100, blank = True)
    quantity = models.IntegerField(null = False, blank = False)
    image = models.ImageField(upload_to = 'Product', blank = False, null = False)
    sdesc = models.CharField(max_length = 500, blank = False)
    desc = models.TextField(max_length = 1000, blank = False)
    original_price = models.FloatField(null = False, blank = False)
    selling_price = models.FloatField(null = False, blank = False)
    trending = models.BooleanField(default = False, help_text = "0 = default, 1 = Trending")
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.name)
    
    class Meta():
        db_table = 'Market'

class MartImage(models.Model):
    mart_name = models.ForeignKey(Market, on_delete = models.CASCADE)
    image = models.FileField(upload_to = 'Sub Product', blank = False, null = False)

    def __str__(self):
        return self.mart_name.name
    
    class Meta():
        db_table = 'Market Images'
       
class Review(models.Model):
	name = models.ForeignKey(User, on_delete = models.CASCADE)
	email = models.EmailField()
	subject = models.CharField(max_length = 50, blank = False)
	message = models.CharField(max_length = 1000, blank = False)

	def __str__(self):
		return self.subject

	class Meta():
		db_table = 'Reviews'
          
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Market, on_delete = models.CASCADE)
    product_qty = models.IntegerField(null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.product)
    
    class Meta():
        db_table = 'Cart'

class Coupon(models.Model):
    coupon_code = models.CharField(max_length = 100, blank = True, unique = True)
    discount = models.IntegerField(blank = True)
    
    def __str__(self):
        return str(self.coupon_code)
    
    class Meta():
        db_table = 'Coupon Codes'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    fullname = models.CharField(max_length = 150, null = False, blank = False)
    email = models.EmailField()
    phone = models.CharField(max_length = 150, null = False, blank = False)
    amount_paid = models.FloatField(null = False)
    payment_mode = models.CharField(max_length = 150, null = False, blank = False)
    # payment_id = models.CharField(max_length = 250, null = False, blank = False)
    orderstatuses = (
        ('pending', 'pending'),
        ('Out For Shipping', 'Out For Shipping'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length = 150, choices = orderstatuses, default = 'pending')
    transaction_ref = models.CharField(max_length = 250, null = False, blank = False)
    tracking_no = models.CharField(max_length = 150, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    
    class Meta():
        db_table = 'Order'
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Market, on_delete = models.CASCADE)
    price = models.FloatField(null = False)
    quantity = models.IntegerField(null = False)

    def __str__(self):
        return str(self.order)
    
    class Meta():
        db_table = 'OrderItem'