def cart_context(request):
    """
    Context processor to make cart item count and subtotal globally available
    across all templates.
    """
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values())
    
    cart_subtotal = 0
    for item in cart.values():
        price = float(item.get('price', 0))
        qty = int(item.get('quantity', 0))
        cart_subtotal += price * qty

    return {
        'global_cart_count': cart_count,
        'global_cart_subtotal': round(cart_subtotal, 2),
    }

