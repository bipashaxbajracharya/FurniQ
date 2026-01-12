import json
import re
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required #This gives access to staffs only
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from .models import Product, Profile, Order, Notification
from django.views.decorators.csrf import csrf_exempt
# This part gets your data from your database and sends to the screen.

#Customer homepage
def home(request):
    
    products = Product.objects.filter(is_featured=True)[:6]
    return render(request, 'inventory/index.html', {'products': products})

def bedroom(request):
    products = Product.objects.filter(category='Bedroom')
    return render(request, 'inventory/bedroom.html', {'products': products})

def livingroom(request):
    products = Product.objects.filter(category='Living Room')
    return render(request, 'inventory/livingroom.html', {'products': products})

def dining(request):
    products = Product.objects.filter(category='Dining')
    return render(request, 'inventory/dining.html',{'products':products})




def user(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        role = request.POST.get('role')
        #print(f"Attempting login for: {u}")
        
        user_obj = authenticate(request, username=u, password=p)
        
        #print(f"User found: {user_obj}")
        
        if user_obj is not None:
            login(request, user_obj)
            if user_obj.is_staff:
                return redirect('product_list')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, 'inventory/user.html')
    
def signout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('user')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone') # This captures the country code + number
        role = request.POST.get('role')

        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('register')

        # 1. Create the User (visible in Admin)
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password,
            first_name=full_name
        )
        
        # 2. Assign Staff Role
        if role == 'staff':
            user.is_staff = True
            user.save()

        # 3. Create the Profile (Saves the Phone Number!)
        Profile.objects.create(user=user, phone_number=phone)

        messages.success(request, f"Welcome {full_name}! Your FurniQ account is ready.")
        return redirect('user') 

    return render(request, 'register.html') # Ensure this path matches your folder
    
def search_results(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = Product.objects.none()
    return render(request, 'inventory/search_results.html', {
        'results': results,
        'query': query
    })

#for staffs
@login_required (login_url='user') #This "locks" the page


def mark_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
def staff_orders(request):
    if not request.user.is_staff:
        return redirect('home')
    
    # Show orders assigned to this specific staff member
    assigned_orders = Order.objects.filter(assigned_staff=request.user).order_by('-order_date')
    return render(request, 'inventory/staff_orders.html', {'orders': assigned_orders})

@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Order.objects.create(
            customer=request.user,
            items_summary=data['items'],
            total_price=data['total']
        )
        return JsonResponse({'status' : 'success'})

def update_stock(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, assigned_staff=request.user)
        action = request.POST.get('action')
        if action == 'increase':
            product.stock += 1
        elif action == 'decrease' and product.stock > 0:
            product.stock -= 1
        product.save()
    return redirect('product_list')

def cart(request):
    return render(request, 'inventory/cart.html')

def product_list(request):
    query = request.GET.get('q')
    if request.user.is_staff:
        products = Product.objects.filter(assigned_staff=request.user)
        if query:
            products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.none()
        messages.error(request, "You do not have permission to view this inventory.")
    return render(request, 'inventory/product_list.html',{'products': products})
