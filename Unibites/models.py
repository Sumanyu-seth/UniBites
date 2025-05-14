from django.db import models

class User(models.Model):
    status_choice = {"1":"active", "0":"inactive"}
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.IntegerField()
    password = models.CharField(max_length=20)
    status = models.CharField(choices = status_choice, default="1")
    class Meta:
        db_table = 'user'
        verbose_name="Client"
        verbose_name_plural="Clients"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='categoryIMGS/', null=True, default=None)

    class Meta:
        db_table = 'category'
        verbose_name='Category'
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name


class Canteen(models.Model):
    status_choice = {"1": "active", "0": "inactive"}
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.IntegerField()
    password = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    status = models.CharField(choices=status_choice, default="0")
    image = models.FileField(upload_to='canteenIMGS/', null=True, default=None)
    class Meta:
        db_table = 'canteen'
        verbose_name="canteen"
        verbose_name_plural="canteens"


class FoodItem(models.Model):
    avail_choice = [
        ("1", "Available"),
        ("0", "Not Available")
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='foodIMGS/', null=True, default=None)
    price = models.FloatField()
    discount = models.IntegerField(null=True, default="NA")
    availability = models.CharField(choices=avail_choice, default="1", max_length=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

    class Meta:
        db_table = 'foodItem'
        verbose_name="foodItem"
        verbose_name_plural="foodItems"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    total_price = models.FloatField()

    class Meta:
        db_table = 'cartItem'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)


class Order(models.Model):
    status_choice = {"1": "accept", "0": "pending","2":'rejected'}
    date=models.DateTimeField(auto_now_add=True)
    total_price=models.FloatField()
    mode=models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    status = models.CharField(choices=status_choice, default="0")
    class Meta:
        db_table = 'order'
        verbose_name="order"
        verbose_name_plural="orders"


class OrderDetails(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    class Meta:
        db_table = 'orderDetails'
        verbose_name="orderDetails"
        verbose_name_plural="orderDetails"


class Reviews(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField(max_length=300)
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    class Meta:
        db_table = 'reviews'
        verbose_name="review"
        verbose_name_plural="reviews"