from django.contrib import admin

from django.utils.html import format_html

from .models import Product, Profile, Order, Notification

admin.site.site_header = "FURNIQ Administration"
admin.site.site_title = "FURNIQ Admin Portal"
admin.site.index_title = "Welcome to the FurniQ Management Dashboard"

# In inventory/admin.py

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'assigned_staff', 'total_price', 'status')
    list_filter = ('status', 'assigned_staff')
    list_editable = ('status', 'assigned_staff')

    def save_model(self, request, obj, form, change):
        # Check if the 'assigned_staff' field was changed
        if change and 'assigned_staff' in form.changed_data:
            if obj.assigned_staff:
                # Create notification for the customer
                Notification.objects.create(
                    user=obj.customer,
                    message=f"Order #{obj.id} update: {obj.assigned_staff.username} has been assigned to your order!"
                )
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

class ProductAdmin(admin.ModelAdmin):
    list_display = ('display_image','name', 'category', 'price', 'stock', 'is_featured', 'assigned_staff', 'old_price')
    list_filter = ('category','assigned_staff')
    search_fields = ('name',)
    list_editable = ('price', 'old_price', 'is_featured',)
    
    def save_model(self, request, obj, form, change):
        if change and 'assigned_staff' in form.changed_data and obj.assigned_staff:
            Notification.objects.create(
                user=obj.customer,
                message=f"Order #{obj.id} has been assigned to {obj.assigned_staff.username}."
            )
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
    
    def display_image(self, obj):
        if obj.image: # Assumes your Product model has an 'image' field
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Preview'
    
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Notification)