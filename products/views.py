from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Category, SubCategory, Tag, Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import ProductForm, ReviewForm

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
    
    reviews = Review.objects.filter(product=product)
    star_range = range(1, 6)
    
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
        'reviews': reviews, 
        'star_range': star_range,
        }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
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

@login_required
def edit_product(request, product_id):
    """ Edit an existing product in the store """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated {product.name}!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')
    
    
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store immediately """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
    
    
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']

            # Check if the user has already reviewed this product
            if Review.objects.filter(product=product, user=request.user).exists():
                messages.error(request, "You've already reviewed this product.")
                return redirect('product_detail', product_id=product.id)

            try:
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Thank you for your review!')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('product_detail', product_id=product.id)
        else:
            print(form.errors)  
            messages.error(request, 'Both rating and comment are required.')

    return redirect('product_detail', product_id=product.id)

def submit_review(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Assign the logged-in user
            review.product = product
            review.save()
            messages.success(request, "Review submitted successfully!")
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {'form': form, 'product': product})

               
def delete_review(request, review_id):
    # Ensure the review exists
    review = get_object_or_404(Review, id=review_id)
    
    # Only allow admins to delete reviews
    if request.user.is_staff:
        review.delete()
    
    return redirect('product_detail', product_id=review.product.id)