from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from accounts.utils import phone_number_required

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

@login_required(login_url = 'login')
@phone_number_required
def add_wishlist(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_wishlist_item_exists = WishlistItem.objects.filter(product=product, user=current_user).exists()
        if is_wishlist_item_exists:
            wishlist_item = WishlistItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in wishlist_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the wishlist item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = WishlistItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = WishlistItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            wishlist_item = WishlistItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                wishlist_item.variations.clear()
                wishlist_item.variations.add(*product_variation)
            wishlist_item.save()
        return redirect('wishlist')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request)) # get the wishlist using the wishlist_id present in the session
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(
                wishlist_id = _wishlist_id(request)
            )
        wishlist.save()

        is_wishlist_item_exists = WishlistItem.objects.filter(product=product, wishlist=wishlist).exists()
        if is_wishlist_item_exists:
            wishlist_item = WishlistItem.objects.filter(product=product, wishlist=wishlist)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in wishlist_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the wishlist item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = WishlistItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = WishlistItem.objects.create(product=product, quantity=1, wishlist=wishlist)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            wishlist_item = WishlistItem.objects.create(
                product = product,
                quantity = 1,
                wishlist = wishlist,
            )
            if len(product_variation) > 0:
                wishlist_item.variations.clear()
                wishlist_item.variations.add(*product_variation)
            wishlist_item.save()
        return redirect('wishlist')

@login_required(login_url = 'login')
@phone_number_required
def remove_wishlist(request, product_id, wishlist_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            wishlist_item = WishlistItem.objects.get(product=product, user=request.user, id=wishlist_item_id)
        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist, id=wishlist_item_id)
        if wishlist_item.quantity > 1:
            wishlist_item.quantity -= 1
            wishlist_item.save()
        else:
            wishlist_item.delete()
    except:
        pass
    return redirect('wishlist')

@login_required(login_url = 'login')
@phone_number_required
def remove_wishlist_item(request, product_id, wishlist_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        wishlist_item = WishlistItem.objects.get(product=product, user=request.user, id=wishlist_item_id)
    else:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist, id=wishlist_item_id)
    wishlist_item.delete()
    return redirect('wishlist')

@login_required(login_url = 'login')
@phone_number_required
def wishlist_view(request, total=0, quantity=0, wishlist_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(user=request.user, is_active=True)
        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)
        for wishlist_item in wishlist_items:
            total += (wishlist_item.product.price * wishlist_item.quantity)
            quantity += wishlist_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'wishlist_items': wishlist_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/wishlist.html', context)