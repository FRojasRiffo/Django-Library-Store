from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogue, name='catalogue'),
    path('detalle/<int:id_book>/', views.detalle_libro, name='detalle_libro'),
    path('eliminar/<int:id_book>/', views.eliminar_libro, name='eliminar_libro'),
    path('agregar/', views.agregar_libro, name='agregar_libro'),
    path('actualizar/<int:id_book>/', views.actualizar_libro, name='actualizar_libro'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar_al_carrito/<int:id_book>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:id_book>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('limpiar_carrito/', views.limpiar_carrito, name='limpiar_carrito'),
    path('login/', views.login_view, name='login'),  # Ensure this is pointing to the correct view
    path('register/', views.registrar_usuario, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
