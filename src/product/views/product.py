import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from product.models import (
    Variant,
    Product,
    ProductVariant,
    ProductVariantPrice,
    ProductImage,
)


class CreateProductView(generic.TemplateView):
    template_name = "products/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values("id", "title")
        context["product"] = True
        context["variants"] = list(variants.all())
        return context

    def post(self, request, *args, **kwargs):
        try:
            # Access JSON data from FormData
            product_data = json.loads(request.POST.get("product", "{}"))
            product_variant_prices_data = json.loads(
                request.POST.get("productVariantPrice", "[]")
            )
            files = request.FILES
            product = Product.objects.create(
                title=product_data.get("title"),
                sku=product_data.get("sku"),
                description=product_data.get("description"),
            )

            for product_variant_price in product_variant_prices_data:
                product_variants = []
                for index, variant in enumerate(
                    product_variant_price["title"].split("/")[:3]
                ):
                    if variant:
                        product_variants.append(
                            ProductVariant.objects.create(
                                variant_title=variant,
                                variant=Variant.objects.get(id=index + 1),
                                product=product,
                            )
                        )

                ProductVariantPrice.objects.create(
                    product_variant_one=(
                        product_variants[0] if len(product_variants) > 0 else None
                    ),
                    product_variant_two=(
                        product_variants[1] if len(product_variants) > 1 else None
                    ),
                    product_variant_three=(
                        product_variants[2] if len(product_variants) > 2 else None
                    ),
                    price=product_variant_price["price"],
                    stock=product_variant_price["stock"],
                    product=product,
                )

            for index in range(len(files)):
                file_key = "file_" + str(index)
                f = files.get(file_key)

                product_image = ProductImage(product=product)
                product_image.file_path.save(f.name, f)
                product_image.save()

            # Return a JsonResponse if needed
            return JsonResponse({"message": "Product Saved successfully"})
        except Exception as e:
            return JsonResponse({"error": "Invalid Product data"}, status=400)


class ProductListView(generic.ListView):
    model = Product
    template_name = "products/list.html"
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        queryset = Product.objects.prefetch_related(
            "product_variants__product_variant_one",
            "product_variants__product_variant_two",
            "product_variants__product_variant_three",
        ).order_by("-created_at")

        title_query = self.request.GET.get("title")
        variant_query = self.request.GET.get("variant")
        price_from_query = self.request.GET.get("price_from")
        price_to_query = self.request.GET.get("price_to")
        date_query = self.request.GET.get("date")

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)

        if variant_query:
            queryset = queryset.filter(
                product_variants__product_variant_two__variant_title__icontains=variant_query
            )

        if price_from_query:
            queryset = queryset.filter(product_variants__price__gte=price_from_query)

        if price_to_query:
            queryset = queryset.filter(product_variants__price__lte=price_to_query)

        if date_query:
            queryset = queryset.filter(created_at__date=date_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all distinct variant names
        variant_names = ProductVariant.objects.values_list(
            "variant_title", flat=True
        ).distinct()
        context["variant_names"] = variant_names
        return context


class EditProductView(View):
    template_name = "products/edit.html"

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product_id = kwargs.get("pk")
        product = get_object_or_404(Product, pk=product_id)

        # Prefetch related data to minimize database queries
        product_variants = ProductVariant.objects.filter(
            product=product
        ).prefetch_related(
            "variant",
            "product_variant_one",
            "product_variant_two",
            "product_variant_three",
        )

        variants = Variant.objects.filter(active=True).values("id", "title")

        context = {
            "product": model_to_dict(product),
            "product_variants": product_variants,
            "variants": list(variants.all()),
            "edit_mode": True,
        }

        return render(request, self.template_name, context)
