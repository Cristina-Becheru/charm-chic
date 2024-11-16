from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Category, SubCategory, Tag
from django.contrib import messages
from django.db.models import Q

from .forms import ProductForm

def all_products(request):
    """ A view to show all products, including sorting and search queries """
    
    products = Product.objects.all()
    
    query = None
    categories = None
    subcategories = None
    tags = None
    sort_option = request.GET.get('sort', 'None_None')  
    current_sorting = sort_option
    
      # Handles the category, subcategory, and tag filtering
    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            
        if 'subcategory' in request.GET:
            subcategory_filter = request.GET['subcategory']
            products = products.filter(subcategory__name=subcategory_filter)
            subcategories = SubCategory.objects.filter(name=subcategory_filter)
            
        if 'tag' in request.GET:
            tags = request.GET['tag'].split(',')
            products = products.filter(tags__name__in=tags)
            tags = Tag.objects.filter(name__in=tags) 
                
    
     # Handles search query
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    
     # Sorting logic
    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')
    elif sort_option == 'name_asc':
        products = products.order_by('name')
    elif sort_option == 'name_desc':
        products = products.order_by('-name')
        
                
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_subcategories': subcategories,
        'current_tags': tags,
        'current_sorting': current_sorting,
     }
    
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    
     # Define size options based on subcategory name
    if product.subcategory and product.subcategory.name == 'Rings':
        size_options = ['Size 5', 'Size 6', 'Size 7', 'Size 8']
        size_label = "Ring Size"
    elif product.subcategory and product.subcategory.name == 'Necklaces':
        size_options = ['16 inches', '18 inches', '20 inches']
        size_label = "Necklace Length"
    elif product.subcategory and product.subcategory.name == 'Bracelets':
        size_options = ['6 inches', '7 inches', '8 inches']
        size_label = "Bracelet Length"
    elif product.subcategory and product.subcategory.name == 'Earrings':
        size_options = ['One-size']
        size_label = "Earring Size"
    else:
        size_options = ['N/A']
        size_label = "Size"

    context = {
        'product': product,
        'size_options': size_options,
        'size_label': size_label,
        }

    return render(request, 'products/product_detail.html', context)

def add_product(request):
    
    """ Add a product to the store """
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Successfully added {product.name}!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
    