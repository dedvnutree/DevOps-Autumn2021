from django.shortcuts import render, redirect
from catalog.models import Furniture, FurnitureInstance, Brand
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User


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


def Add_To_Basket(request, pk):
    userName= str(request.user.get_username)
    userCache = cache.get(userName)
    if(userCache is None):
        userCache= {'basketList': [pk]}
        cache.set(userName, userCache, None)

    userCache = cache.get(userName)

    basketList = userCache['basketList']
    if(basketList is None): #если не существует
        userCache['basketList':[pk]]
        cache.set(userName, userCache, None)
    else:
        if(pk not in basketList):
            basketList.append(pk)
            userCache['basketList'] = basketList
        cache.set(userName, userCache, None)
    return redirect(request.GET.get('next'))


def Remove_From_Basket(request, pk):
    userName= str(request.user.get_username)
    userCache = cache.get(userName)
    if(userCache is None):
        return HttpResponse('<h1>Такого товара нет в корзине!</h1>')

    userCache = cache.get(userName)
    basketList = userCache['basketList']
    if(basketList is None):
        return HttpResponse('<h1>Такого товара нет в корзине!</h1>')
    else:
        if(pk in basketList):
            basketList.remove(pk)
            userCache['basketList'] = basketList
        cache.set(userName, userCache, None)

    return redirect(request.GET.get('next'))

@login_required
def basketView(request):
    userName = str(request.user.get_username)
    userCache = cache.get(userName)
    context = {}

    if(userCache is not None):
        context = {"basketList": userCache['basketList']}
        context["furnitureInstances"] = FurnitureInstance.objects.filter(id__in = context['basketList'])
        sum = 0
        for furnitureInstance in context["furnitureInstances"]:
            sum += furnitureInstance.furniture.price
        context['sum'] = sum

    return render(request, 'catalog/basket.html', context=context)


class PersonalAccountListView(LoginRequiredMixin, generic.ListView):
    model = FurnitureInstance
    template_name = 'catalog/personal_account.html'

    def get_queryset(self):
        return FurnitureInstance.objects.filter(buyer=self.request.user).order_by('delivery_day')


class FurnitureListView(generic.ListView):
    model = Furniture
    def get_queryset(self):
        return Furniture.objects.filter(published=True)


class FurnitureDetailView(generic.DetailView):
    model = Furniture


class BrandListView(generic.ListView):
    model = Brand
    paginate_by = 8


class BrandDetailView(generic.DetailView):
    model = Brand




class WorkersPageListView(PermissionRequiredMixin, generic.ListView):
    model = Furniture
    template_name = 'catalog/workers_page.html'
    permission_required = ('catalog.worker',)

    def get_queryset(self):
        return Furniture.objects.filter(published=False)


import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse

from catalog.forms import RenewFurnitureForm, RenewFurnitureModelForm

@login_required
@permission_required('worker', raise_exception=True)
def renew_furniture_worker(request, pk):

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

class FurnitureCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.worker'
    model = Furniture
    fields = ['name', 'brand', 'type', 'image', 'description', 'isbn',]

class FurnitureUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.worker'
    model = Furniture
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class FurnitureDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.worker'
    model = Furniture
    success_url = reverse_lazy('furniture')

class FurnitureInstanceCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.worker'
    model = FurnitureInstance
    fields = '__all__'

class FurnitureInstanceUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.worker'
    model = FurnitureInstance
    fields = ['status', 'buyer', 'delivery_day']
    success_url = reverse_lazy('furniture')



class BrandCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.worker'
    model = Brand
    fields = '__all__'

class BrandUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.worker'
    model = Brand
    fields = '__all__'

class BrandDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.worker'
    model = Brand
    success_url = reverse_lazy('brand')
