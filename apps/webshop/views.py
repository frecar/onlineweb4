from django.contrib import messages
from django.views.generic import TemplateView, DetailView
from apps.webshop.models import Category, Product, Order, OrderLine
from apps.webshop.forms import OrderForm


class CartMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CartMixin, self).get_context_data(**kwargs)
        context['order_line'] = self.current_order_line()
        return context

    def current_order_line(self):
        order_line = OrderLine.objects.filter(user=self.request.user).first()
        if not order_line:
            order_line = OrderLine.objects.create(user=self.request.user)
        return order_line


class Home(CartMixin, TemplateView):
    template_name = 'webshop/base.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryDetail(CartMixin, DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'webshop/category.html'


class ProductDetail(CartMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'webshop/product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['orderform'] = OrderForm
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = OrderForm(request.POST)
        if form.is_valid():
            order_line = self.current_order_line()
            # Checking if product has already been added to cart
            order = order_line.orders.filter(product=product).first()
            if order:
                # Adding to existing order
                order.number += form.cleaned_data['number']
                messages.info(
                    request,
                    'Produktet \'{product}\' var allerede i handlekurven din. Antall har blitt oppdatert til {number}.'
                    .format(product=product, number=order.number)
                )
            else:
                # Creating new order
                order = Order(
                    product=product, price=product.price,
                    number=form.cleaned_data['number'],
                    order_line=order_line)
            order.save()
        else:
            messages.error(request, 'Vennligst oppgi et gyldig antall')
        return super(ProductDetail, self).get(request, *args, **kwargs)


class Checkout(CartMixin, TemplateView):
    template_name = 'webshop/checkout.html'