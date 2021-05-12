from django.shortcuts import render
from catalog.models import Furniture, FurnitureInstance, Brand, Type
from django.views import generic


def index(request):
    num_furniture = Furniture.objects.all().count()
    num_instances = FurnitureInstance.objects.all().count()
    num_instances_available = FurnitureInstance.objects.filter(status='a').count()
    num_brands = Brand.objects.count()
    num_brands_from_Russia = Brand.objects.filter(country__startswith='Russia').count()

    context = {
        'num_furniture': num_furniture,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_brands': num_brands,
        'num_brands_from_Russia': num_brands_from_Russia,
    }

    return render(request, 'index.html', context=context)


class FurnitureListView(generic.ListView):
    model = Furniture
    paginate_by = 5


class FurnitureDetailView(generic.DetailView):
    model = Furniture


class BrandListView(generic.ListView):
    model = Brand
    paginate_by = 5


class BrandDetailView(generic.DetailView):
    model = Brand
