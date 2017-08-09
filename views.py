from datetime import datetime
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import Price, Market, Provider, Product, ProductUnit, Sort


def price_list(request):

    prices = Price.objects.\
        filter(is_actual=True).\
        order_by('-pub_date')

    markets = Market.objects.all()
    providers = Provider.objects.all()
    products = Product.objects.all()
    product_units = ProductUnit.objects.all()

    template = loader.get_template('price_list.html')

    context = {
        'prices': prices,
        'markets': markets,
        'providers': providers,
        'products': products,
        'product_units': product_units,
    }

    return HttpResponse(template.render(context))


def market_list(request):

    markets = Market.objects.all()

    template = loader.get_template('market_list.html')

    context = {'markets': markets}

    return HttpResponse(template.render(context))


def provider_list(request):

    providers = Provider.objects.all()

    template = loader.get_template('provider_list.html')

    context = {'providers': providers}

    return HttpResponse(template.render(context))


def product_list(request):

    products = Product.objects.all()

    template = loader.get_template('product_list.html')

    context = {'products': products}

    return HttpResponse(template.render(context))


def unit_list(request):

    products_units = ProductUnit.objects.all()

    template = loader.get_template('units_list.html')

    context = {'units': products_units}

    return HttpResponse(template.render(context))


def sort_list(request):

    sorts = Sort.objects.all()

    template = loader.get_template('sort_list.html')

    context = {'sorts': sorts}

    return HttpResponse(template.render(context))


@csrf_exempt
def add_price(request):

    # fix it
    from django.contrib.auth.models import User
    user = User.objects.get(id=1)

    actual_price = Price.objects.filter(
        provider=Provider.objects.get(id=request.POST.get(
            'provider')),
        market=Market.objects.get(id=request.POST.get('market')),
        product=Product.objects.get(id=request.POST.get(
            'product')),
        sort=Sort.objects.get(id=request.POST.get('sort')),
        is_actual=True
    )

    for ap in actual_price:
        ap.is_actual = False
        ap.save()

    p = Price(
        user=user,
        provider=Provider.objects.get(id=request.POST.get(
            'provider')),
        market=Market.objects.get(id=request.POST.get('market')),
        product=Product.objects.get(id=request.POST.get(
            'product')),
        sort=Sort.objects.get(id=request.POST.get('sort')),
        product_unit=ProductUnit.objects.get(id=request.POST.get(
            'product_unit')),
        price=request.POST.get('price'),
        waggon_sign=request.POST.get('waggon_sign'),
        pub_date=datetime.now(),
        is_actual=True
    )

    p.save()

    return HttpResponse(price_list(request))


@csrf_exempt
def delete_price(request):

    p = Price.objects.filter(id=request.POST.get('price_id')).get()
    p.is_actual = False

    p.save()

    return HttpResponse(price_list(request))


def actions_market(request):
    name = request.GET.get('name_market')
    id_market = request.GET.get('id_market')
    if name and id_market is None:
        m = Market(name=name)
        m.save()
    if id_market and name is None:
        id_list_market = [int(el) for el in id_market.split(',')]
        m = Market.objects.filter(id__in=id_list_market)
        m.delete()
    if name and id_market:
        m = Market.objects.get(id=id_market)
        m.name = name
        m.save(update_fields=['name'])
    return HttpResponse(market_list(request))


def actions_provider(request):
    name = request.GET.get('name_provider')
    description = request.GET.get('description')
    id_provider = request.GET.get('id_provider')
    if name and description and id_provider is None:
        p = Provider(name=name, description=description)
        p.save()
    if id_provider and name is None and description is None:
        id_list_provider = [int(el) for el in id_provider.split(',')]
        p = Provider.objects.filter(id__in=id_list_provider)
        p.delete()
    if name and description and id_provider:
        p = Provider.objects.get(id=id_provider)
        p.name = name
        p.description = description
        p.save(update_fields=['name', 'description'])
    return HttpResponse(provider_list(request))


def sorts_ajax(request):
    sort_product_id = request.GET.get('sorts')
    sorts = serializers.serialize("json", Sort.objects.filter(product_id=sort_product_id))
    return HttpResponse(sorts, content_type='application/json')