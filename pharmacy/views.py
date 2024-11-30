from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import *

#Placeholder for your comment
def signup(request):
    if request.method == 'POST':
        names = request.POST.get('names')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        password = request.POST.get('password')
        
        email_error = None
        phone_error = None

        if PharmacyInstance.objects.filter(email=email).exists():
            email_error = 'This email is already registered.'

        if PharmacyInstance.objects.filter(phonenumber=phonenumber).exists():
            phone_error = 'This phone number is already registered.'

        if email_error or phone_error:
            return render(request, 'pharmacy/signup.html', {
                'email_error': email_error,
                'phone_error': phone_error,
            })
            
        PharmacyInstance.objects.create(
            names=names,
            email=email,
            phonenumber=phonenumber,
            password=password
        )
        return redirect('login')
    return render(request, 'pharmacy/signup.html')

def login_view(request):
    if request.method == 'POST':
        pharmacy_name = request.POST['name']  
        password = request.POST["password"]
        try:
            pharmacy = PharmacyInstance.objects.get(names=pharmacy_name)
            if pharmacy.password == password :
                # Login successful, redirect to a protected page
                request.session['pharmacy_id'] = pharmacy.phonenumber  # Store pharmacy in the session
                return redirect('read_product')
            else:
                return render(request, 'pharmacy/login.html', {
                    'error': 'Invalid Name or password. Please try again.'})
        except PharmacyInstance.DoesNotExist:
            return render(request, 'pharmacy/login.html', {
                'error': 'Invalid Name or password. Please try again.'})
    else:
        return render(request, 'pharmacy/login.html', {'error': None})

def logout_view(request):
    logout(request)
    return redirect('login')

#@login_required
def read_product(request):
    products = Product.objects.all()
    return render(request, 'pharmacy/read_product.html', {'products': products})

#@login_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        stock_quantity = request.POST['stock_quantity']
        expiration_date = request.POST['expiration_date']
        picture = request.POST['url']
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=stock_quantity,
            expiration_date=expiration_date,
            picture=picture,
        )
        return redirect('read_product')
    return render(request, 'pharmacy/create_product.html')

#@login_required
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.quantity = request.POST['stock_quantity']
        product.expiration_date = request.POST['expiration_date']
        product.picture = request.POST['url']
        product.save()
        return redirect('read_product')
    return render(request, 'pharmacy/update_product.html', {'product': product})

#@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('read_product')
    return render(request, 'pharmacy/delete_product.html', {'product': product})

#@login_required
def view_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'pharmacy/view_product.html', {'product': product})

#@login_required
def search_medicines(request):
    """
    View to handle medicine search functionality.
    Returns only the names of the medicines matching the query (case-insensitive).
    """
    query = request.GET.get('query', '').strip()  # Get and clean the search query
    results = []

    if query:
        # Perform a case-insensitive search and retrieve required fields
        results = Product.objects.filter(
            name__icontains=query
        ).values('id', 'name','picture')
        print(results)
    context = {
        'query': query,
        'results': results,  
    }
    return render(request, 'pharmacy/search_medicine.html', context)