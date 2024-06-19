from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .forms import BookForm, RegistrationForm
from .models import Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def index(request):
    resultado = Book.objects.all()
    contexto = {"books": resultado}
    return render(request, 'shop/index.html', contexto)

def catalogue(request):
    resultado = Book.objects.all()
    contexto = {"books": resultado}
    return render(request, 'shop/catalogue.html', contexto)

def login(request):
    return render(request, 'shop/login.html')

def register(request):
    return render(request, 'shop/register.html')

def detalle_libro(request, id_book):
    resultado = Book.objects.get(id=id_book)
    contexto = {"book": resultado}
    return render(request, 'shop/detalle_libro.html', contexto)

def eliminar_libro(request, id_book):
    libro = get_object_or_404(Book, id=id_book)
    libro.delete()
    return redirect('/shop/catalogo')

def agregar_libro(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "GET":
            formulario = BookForm()
            contexto = {'formulario': formulario}
            return render(request, 'shop/agregar_libro.html', contexto)
        elif request.method == "POST":
            formulario = BookForm(request.POST, request.FILES)
            if formulario.is_valid():
                formulario.save()
                return redirect('/shop/catalogo')
        else:
            return redirect('/shop')
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
