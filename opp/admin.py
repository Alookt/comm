from django.contrib import admin
from .models import Category, Product, Order, OrderItem, CartItem,UserProfile
from django.utils.html import format_html
import numpy as np
import matplotlib.pyplot as plt
import io
from django.db.models import Sum
import base64
from django.utils.timezone import now
from datetime import timedelta
from django.http import Http404

class AdminLogin404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the requested path is the admin login page
        if request.path == '/admin/login/':
            # If the user is already authenticated and staff, allow normal access
            if request.user.is_authenticated and request.user.is_staff:
                return self.get_response(request)
            # Otherwise, raise 404 to hide the admin login page
            raise Http404("Page not found")

        # For all other requests, continue as usual
        response = self.get_response(request)
        return response


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'sales_chart')
    

#     def sales_chart(self, obj):
#         import numpy as np
#         import matplotlib.pyplot as plt
#         import io
#         import base64

#         x = np.arange(1, 31)  # 30 days

#     # Convert Decimal to float before arithmetic
#         price_float = float(obj.price)

#     # Simulate sales data (replace with real data if available)
#         np.random.seed(obj.id)
#         y = 10 + price_float + (np.sin(x / 3) * 5) + np.random.normal(scale=2, size=x.size)

#         plt.figure(figsize=(3, 1.5))
#         plt.plot(x, y, marker='o', linestyle='-', color='teal', linewidth=2)
#         plt.title("Sales (simulated)")
#         plt.xticks([])
#         plt.yticks([])
#         plt.tight_layout()

#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         plt.close()
#         buf.seek(0)

#         image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
#         buf.close()

#         from django.utils.html import format_html
#         return format_html('<img src="data:image/png;base64,{}" width="300" height="150" />', image_base64)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sales_chart')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


    def sales_chart(self, obj):
        # Define date range (last 30 days)
        end_date = now().date()
        start_date = end_date - timedelta(days=29)

        # Query sales aggregated by date (sum of quantity)
        sales_qs = (
            obj.sales.filter(date__range=(start_date, end_date))
            .values('date')
            .annotate(total_qty=Sum('quantity'))
            .order_by('date')
        )

        # Prepare x (days) and y (sales qty) arrays
        date_to_qty = {item['date']: item['total_qty'] for item in sales_qs}

        x_dates = [start_date + timedelta(days=i) for i in range(30)]
        y_qty = [date_to_qty.get(day, 0) for day in x_dates]

        # Convert dates to labels or just numeric x-axis for the plot
        x = np.arange(1, 31)

        # Plotting
        plt.figure(figsize=(3, 1.5))
        plt.plot(x, y_qty, marker='o', linestyle='-', color='teal', linewidth=2)
        plt.title('Sales last 30 days')
        plt.xticks([])  # optional: hide x ticks to keep chart clean
        plt.yticks([])
        plt.tight_layout()

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        # Encode to base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        # Render image in Django Admin
        return format_html(
            '<img src="data:image/png;base64,{}" width="300" height="150"/>',
            image_base64
        )

    sales_chart.short_description = "Sales Chart"

admin.site.register(UserProfile)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price')
#     list_filter = ('category',)
#     search_fields = ('name', 'description')
#     prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'complete', 'transaction_id')
    list_filter = ('complete', 'created_at')
    search_fields = ('user__username', 'transaction_id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
