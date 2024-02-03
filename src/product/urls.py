from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from product.views.product import CreateProductView, ProductListView, EditProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', csrf_exempt(CreateProductView.as_view()), name='create.product'),
    path('<int:pk>/', csrf_exempt(EditProductView.as_view()), name='edit.product'),
    path('list/', ProductListView.as_view() , name='list.product'),
]
