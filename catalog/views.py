from django.shortcuts import render
from catalog.models import Furniture, FurnitureInstance, Brand
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


def index(request):
    num_furniture = Furniture.objects.all().count()
    num_instances = FurnitureInstance.objects.all().count()
    num_instances_available = FurnitureInstance.objects.filter(status='a').count()
    num_brands = Brand.objects.count()
    num_brands_from_russia = Brand.objects.filter(country__startswith='Russia').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_furniture': num_furniture,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_brands': num_brands,
        'num_brands_from_Russia': num_brands_from_russia,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class FurnitureListView(generic.ListView):
    model = Furniture
    def get_queryset(self):
        return Furniture.objects.filter(published=True)


class FurnitureDetailView(generic.DetailView):
    model = Furniture


class BrandListView(generic.ListView):
    model = Brand


class BrandDetailView(generic.DetailView):
    model = Brand


class PersonalAccountListView(LoginRequiredMixin, generic.ListView):
    model = FurnitureInstance
    template_name = 'catalog/personal_account.html'

    def get_queryset(self):
        return FurnitureInstance.objects.filter(buyer=self.request.user).order_by('delivery_day')


class WorkersPageListView(PermissionRequiredMixin, generic.ListView):
    model = Furniture
    template_name = 'catalog/workers_page.html'
    permission_required = ('catalog.change_furniture',)

    def get_queryset(self):
        return Furniture.objects.filter(published=False)