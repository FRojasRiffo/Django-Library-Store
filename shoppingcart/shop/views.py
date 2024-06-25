from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import BookForm, RegistrationForm
from .models import Book
import requests
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'shop/index.html')

def catalogue(request):
    currency = request.GET.get('currency', 'CLP')

    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/CLP')
        data = response.json()
        conversion_rate = data['rates']['USD']
    except Exception as e:
        conversion_rate = None
        print(f"Error fetching conversion rate: {e}")

    books = Book.objects.all()
    book_data = []
    for book in books:
        if currency == 'USD' and conversion_rate:
            price_in_usd = book.price * conversion_rate
        else:
            price_in_usd = None
        book_data.append({
            'book': book,
            'price_in_usd': price_in_usd,
        })

    context = {
        'book_data': book_data,
        'conversion_rate': conversion_rate,
        'currency': currency,
    }
    return render(request, 'shop/catalogue.html', context)


# def login(request):
#     return render(request, 'shop/login.html')

def register(request):
    return render(request, 'shop/register.html')

def detalle_libro(request, id_book):
    resultado = Book.objects.get(id=id_book)
    contexto = {"book": resultado}
    return render(request, 'shop/detalle_libro.html', contexto)

def eliminar_libro(request, id_book):
    if request.user.is_authenticated and request.user.is_superuser:
        libro = Book.objects.get(id=id_book)
        libro.delete()
        return redirect('/shop/catalogo')
    else:
        redirect('/shop')

def agregar_libro(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('catalogue')
        else:
            form = BookForm()
        return render(request, 'shop/agregar_libro.html', {'formulario': form})
    else:
        return redirect('/shop')

def actualizar_libro(request, id_book):
    libro = Book.objects.get(id=id_book)
    if request.method == "GET":
        contexto = {"book": libro}
        return render(request, 'shop/actualizar_libro.html', contexto)
    if request.method == "POST":
        title = request.POST["txt_title"]
        price = request.POST["int_price"]
        description = request.POST["txt_description"]
        libro.title = title
        libro.price = price
        libro.description = description
        if 'cover_image' in request.FILES:
            libro.cover_image = request.FILES['cover_image']
        libro.save()
        return redirect('/shop/catalogo')
    else:
        return redirect('/shop/catalogo')

def carrito(request):
    carrito = request.session.get('carrito', [])
    total = sum(item['price'] * item['quantity'] for item in carrito)
    contexto = {
        'carrito': carrito,
        'total': total
    }
    return render(request, 'shop/carrito.html', contexto)

def agregar_al_carrito(request, id_book):
    libro = Book.objects.get(id=id_book)
    carrito = request.session.get('carrito', [])
    
    for item in carrito:
        if item['id'] == libro.id:
            item['quantity'] += 1
            break
    else:
        carrito.append({
            'id': libro.id,
            'title': libro.title,
            'price': libro.price,
            'quantity': 1,
            'cover_image': libro.cover_image.url if libro.cover_image else None
        })
    
    request.session['carrito'] = carrito
    
    if 'from_cart' in request.POST:
        return redirect('/shop/carrito')
    return redirect('/shop/catalogo')

def eliminar_del_carrito(request, id_book):
    carrito = request.session.get('carrito', [])
    for item in carrito:
        if item['id'] == id_book:
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                carrito.remove(item)
            break
    request.session['carrito'] = carrito
    return redirect('/shop/carrito')
    
def limpiar_carrito(request):
    request.session['carrito'] = []
    return redirect('/shop/carrito')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/shop')
    else:
        form = RegistrationForm()
    
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error': 'Usuario o contraseña incorrecta'})
    return render(request, 'registration/login.html')

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({'success': True, 'redirect_url': '/index/'})
#         else:
#             return JsonResponse({'success': False, 'error': 'Usuario o contraseña incorrecta'})
#     return render(request, 'login.html')

