from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('read_product')
    else:
        form = UserCreationForm()
    return render(request, 'pharmacy/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'read_product')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'pharmacy/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def read_product(request):
    products = Product.objects.all()
    return render(request, 'pharmacy/read_product.html', {'products': products})

@login_required
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

@login_required
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

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('read_product')
    return render(request, 'pharmacy/delete_product.html', {'product': product})

@login_required
def view_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'pharmacy/view_product.html', {'product': product})

@login_required
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