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
    permission_required = ('catalog.worker',)

    def get_queryset(self):
        return Furniture.objects.filter(published=False)

import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from catalog.forms import RenewFurnitureForm, RenewFurnitureModelForm

@login_required
@permission_required('worker', raise_exception=True)
def renew_furniture_worker(request, pk):
    """View function for renewing a specific FurnitureInstance by worker."""

    furniture_instance = get_object_or_404(FurnitureInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewFurnitureModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            furniture_instance.delivery_day = form.cleaned_data['renewal_date']
            furniture_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-reserved'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewFurnitureModelForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'furniture_instance': furniture_instance,
    }

    return render(request, 'catalog/renew_furniture_worker.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Furniture, Brand

class FurnitureCreate(CreateView):
    model = Furniture
    fields = ['name', 'brand', 'type', 'image', 'description', 'isbn',]

class FurnitureUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.worker'
    model = Furniture
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class FurnitureDelete(DeleteView):
    model = Furniture
    success_url = reverse_lazy('furniture')

class FurnitureInstanceCreate(CreateView):
    model = FurnitureInstance
    fields = '__all__'

class FurnitureInstanceUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.worker'
    model = FurnitureInstance
    fields = ['status', 'buyer', 'delivery_day']
    success_url = reverse_lazy('furniture')



class BrandCreate(CreateView):
    model = Brand
    fields = '__all__'

class BrandUpdate(UpdateView):
    model = Brand
    fields = '__all__'

class BrandDelete(DeleteView):
    model = Brand
    success_url = reverse_lazy('brand')
