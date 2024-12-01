from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
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
        
        PharmacyInstance.objects.create(names=names, email=email, phonenumber=phonenumber, password=password)
        return redirect('login')
    return render(request, 'pharmacy/signup.html')

def login_view(request):
    if request.method == 'POST':
        pharmacy_name = request.POST['name']  
        password = request.POST["password"]
        try:
            pharmacy = PharmacyInstance.objects.get(names=pharmacy_name)
            if pharmacy.password == password :
                request.session['pharmacy_id'] = pharmacy.phonenumber
                return redirect('read_product')
            else:
                return render(request, 'pharmacy/login.html', {'error': 'Invalid Name or password. Please try again.'})
        except PharmacyInstance.DoesNotExist:
            return render(request, 'pharmacy/login.html', {'error': 'Invalid Name or password. Please try again.'})
    return render(request, 'pharmacy/login.html', {'error': None})

def logout_view(request):
    logout(request)
    return redirect('login')

def read_product(request):
    pharmacy_id = request.session.get('pharmacy_id')
    if not pharmacy_id:
        return redirect('login')

    pharmacy = get_object_or_404(PharmacyInstance, phonenumber=pharmacy_id)

    products = Product.objects.filter(pharmacy=pharmacy)
    return render(request, 'pharmacy/read_product.html', {'products': products})


def create_product(request):
    pharmacy_id = request.session.get('pharmacy_id')
    if not pharmacy_id:
        return redirect('login')
    if request.method == 'POST':

        Product.objects.create(
            name = request.POST['name'],
            description = request.POST['description'],
            price = request.POST['price'],
            quantity = request.POST['stock_quantity'],
            expiration_date = request.POST['expiration_date'],
            picture = request.POST['url'],
            pharmacy = get_object_or_404(PharmacyInstance, phonenumber=pharmacy_id)
        )
        return redirect('read_product')
    return render(request, 'pharmacy/create_product.html')

def update_product(request, id):
    pharmacy_id = request.session.get('pharmacy_id')
    if not pharmacy_id:
        return redirect('login')
    pharmacy = get_object_or_404(PharmacyInstance, phonenumber=pharmacy_id)
    product = get_object_or_404(Product, id=id, pharmacy=pharmacy)
    
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

def delete_product(request, id):
    pharmacy_id = request.session.get('pharmacy_id')
    if not pharmacy_id:
        return redirect('login')
    pharmacy = get_object_or_404(PharmacyInstance, phonenumber=pharmacy_id)
    product = get_object_or_404(Product, id=id, pharmacy=pharmacy)
    
    if request.method == 'POST':
        product.delete()
        return redirect('read_product')
    return render(request, 'pharmacy/delete_product.html', {'product': product})

def view_product(request, id):
    pharmacy_id = request.session.get('pharmacy_id')
    if not pharmacy_id:
        return redirect('login')
    pharmacy = get_object_or_404(PharmacyInstance, phonenumber=pharmacy_id)
    product = get_object_or_404(Product, id=id, pharmacy=pharmacy)
    return render(request, 'pharmacy/view_product.html', {'product': product})

def search_medicines(request):
    query = request.GET.get('query', '').strip()
    results = []

    if query:
        results = Product.objects.filter(
            name__icontains=query
        ).values('id', 'name','picture')
        print(results)
    context = {
        'query': query,
        'results': results,  
    }
    return render(request, 'pharmacy/search_medicine.html', context)