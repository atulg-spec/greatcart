from django.db.models import Count, Q
from .models import Product
from django.db.models import Case, When, Value, IntegerField

def get_related_products(product, limit=4):
    """
    Get related products based on multiple factors:
    - Same category
    - Same brand
    - Similar price range
    - Popular products
    """
    base_queryset = Product.objects.filter(
        is_available=True
    ).exclude(id=product.id)
    
    # Get products from same category and brand first
    related = base_queryset.filter(
        Q(category=product.category) |
        Q(product_brand=product.product_brand)
    ).annotate(
        relevance=Count('id')  # Placeholder for more complex logic
    ).order_by('-relevance', '?')
    
    # If not enough results, expand to similar price range
    if related.count() < limit:
        price_range = product.price * 0.7, product.price * 1.3
        price_related = base_queryset.filter(
            price__range=price_range
        ).exclude(
            id__in=related.values_list('id', flat=True)
        ).order_by('?')
        related = list(related) + list(price_related)
    
    return related[:limit]


def get_behavior_related_products(product, request=None, limit=4):
    """
    Get related products based on:
    - What other customers viewed/purchased with this product
    - User's browsing history (if available)
    """
    base_queryset = Product.objects.filter(
        is_available=True
    ).exclude(id=product.id)
    
    # Get products frequently bought together (from order data)
    try:
        from orders.models import OrderProduct
        orders_with_product = OrderProduct.objects.filter(
            product=product,
            order__status='Completed'
        ).values_list('order_id', flat=True).distinct()
        
        frequently_bought_together = base_queryset.filter(
            orderproduct__order_id__in=orders_with_product
        ).annotate(
            joint_orders=Count('orderproduct__order')
        ).order_by('-joint_orders')[:limit]
        
        if frequently_bought_together.count() >= limit:
            return frequently_bought_together
    except Exception as e:
        # Log error or fallback if order data isn't available
        frequently_bought_together = []
    
    # Fallback to category-based if no order data
    category_related = base_queryset.filter(
        category=product.category
    ).order_by('?')
    
    # Combine results
    related = list(frequently_bought_together)
    related_ids = [p.id for p in related]
    
    # Add category-based products if needed
    for p in category_related:
        if p.id not in related_ids and len(related) < limit:
            related.append(p)
            related_ids.append(p.id)
    
    # If user is authenticated, prioritize their browsing history
    if request and request.user.is_authenticated:
        try:
            # Check the correct field name in your RecentlyStalked model
            user_history = Product.objects.filter(
                recentlystalked__user=request.user
            ).exclude(
                id__in=[product.id] + related_ids
            ).order_by('-recentlystalked__id')[:2]  # Using ID as fallback
            
            related = list(user_history) + related
            related = related[:limit]
        except Exception as e:
            # Log error but continue without user history
            pass
    
    return related