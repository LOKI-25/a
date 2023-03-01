from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns=[
     path('payments/',views.payments,name='payments'),
    path('place_order/',views.place_order,name='place_order'),
    path('order_complete/', views.order_complete, name='order_complete'),

   
    
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)