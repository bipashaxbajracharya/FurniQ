from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required #This gives access to staffs only
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from .models import Product
# This part gets your data from your database and sends to the screen.

#Customer homepage
def home(request):
    return render(request, 'inventory/index.html')

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
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        role = request.POST.get('role')
        #check if user already exist!!
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'inventory/register.html')
        #create new user
        new_user = User.objects.create_user(username=u, email=e, password=p)
        
        #role assignment
        if role == 'staff':
            new_user.is_staff = True   # Allows access to @login_required pages for staff
            new_user.save()
            messages.success(request, "Staff account created! Please login.")
        else:
            messages.success(request, "Account created successfully!")
        return redirect('user')    # Take them to the login page
    return render(request, 'inventory/register.html')

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
