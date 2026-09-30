from django.db import models
import uuid


class Part(models.Model):
    CATEGORY_CHOICES = [
        ('Engine', 'Engine'),
        ('Brakes', 'Brakes'),
        ('Electrical', 'Electrical'),
        ('Filters', 'Filters'),
        ('Lighting', 'Lighting'),
        ('Suspension', 'Suspension'),
        ('Accessories', 'Accessories'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Engine')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    icon = models.CharField(max_length=20, default='⚙️')
    part_number = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=25)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} ({self.part_number}) - ₹{self.price}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Order Placed'),
        ('Processing', 'Processing & Packing'),
        ('Dispatched', 'Dispatched / In Transit'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]

    DELIVERY_CHOICES = [
        ('Standard', 'Standard Delivery (3-5 Days) - ₹49 (Free over ₹1,500)'),
        ('Express', 'Express Delivery (1-2 Days) - ₹149'),
        ('Doorstep Priority', 'Doorstep Priority (Same/Next Day) - ₹249'),
    ]

    order_id = models.CharField(max_length=30, unique=True, editable=False)
    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    pincode = models.CharField(max_length=15)

    delivery_method = models.CharField(max_length=40, choices=DELIVERY_CHOICES, default='Standard')
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Placed')
    estimated_delivery = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_id} - {self.full_name} (₹{self.total_price})"

    @staticmethod
    def generate_order_id():
        short_code = uuid.uuid4().hex[:6].upper()
        return f"ORD-AP-{short_code}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, blank=True)
    part_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.part_name} (₹{self.item_total})"
