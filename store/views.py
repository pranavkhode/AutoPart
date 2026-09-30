from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Part, Order, OrderItem
import datetime


def home(request):
    category = request.GET.get('category', 'All')
    categories = [
        'All',
        'Engine',
        'Brakes',
        'Electrical',
        'Filters',
        'Lighting',
        'Suspension',
        'Accessories'
    ]

    if category and category != 'All':
        parts = Part.objects.filter(category=category, is_available=True)
    else:
        parts = Part.objects.filter(is_available=True)

    context = {
        'parts': parts,
        'categories': categories,
        'active_category': category,
    }
    return render(request, 'store/index.html', context)


def add_to_cart(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    cart = request.session.get('cart', {})
    key = str(part_id)

    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {
            'id': part.id,
            'name': part.name,
            'price': float(part.price),
            'category': part.category,
            'icon': part.icon,
            'part_number': part.part_number,
            'quantity': 1,
        }

    request.session['cart'] = cart
    request.session.modified = True

    total_count = sum(item['quantity'] for item in cart.values())
    subtotal = sum(float(item['price']) * item['quantity'] for item in cart.values())

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        return JsonResponse({
            'status': 'success',
            'message': f"{part.name} added to cart!",
            'part_name': part.name,
            'cart_count': total_count,
            'cart_subtotal': round(subtotal, 2),
            'item_quantity': cart[key]['quantity'],
        })

    messages.success(request, f"{part.name} added to your cart!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = 0.0

    for key, item in cart.items():
        price = float(item.get('price', 0))
        qty = int(item.get('quantity', 0))
        item_total = price * qty
        subtotal += item_total
        cart_items.append({
            'id': item.get('id', key),
            'name': item.get('name'),
            'price': price,
            'category': item.get('category'),
            'icon': item.get('icon', '🚗'),
            'part_number': item.get('part_number', ''),
            'quantity': qty,
            'item_total': round(item_total, 2),
        })

    gst_tax = round(subtotal * 0.18, 2)  # 18% standard GST for automotive components
    standard_shipping = 0.0 if subtotal >= 1500 or subtotal == 0 else 49.0
    estimated_total = round(subtotal + standard_shipping, 2)

    context = {
        'cart_items': cart_items,
        'subtotal': round(subtotal, 2),
        'gst_tax': gst_tax,
        'standard_shipping': standard_shipping,
        'estimated_total': estimated_total,
        'free_shipping_qualify': subtotal >= 1500,
        'free_shipping_needed': max(0, round(1500 - subtotal, 2)),
    }
    return render(request, 'store/cart.html', context)


def update_cart_quantity(request, part_id, action):
    cart = request.session.get('cart', {})
    key = str(part_id)

    if key in cart:
        if action == 'inc':
            cart[key]['quantity'] += 1
        elif action == 'dec':
            cart[key]['quantity'] -= 1
            if cart[key]['quantity'] <= 0:
                del cart[key]

        request.session['cart'] = cart
        request.session.modified = True

    total_count = sum(item['quantity'] for item in cart.values())
    subtotal = sum(float(item['price']) * item['quantity'] for item in cart.values())

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        item_qty = cart.get(key, {}).get('quantity', 0)
        item_price = cart.get(key, {}).get('price', 0)
        return JsonResponse({
            'status': 'success',
            'cart_count': total_count,
            'subtotal': round(subtotal, 2),
            'item_quantity': item_qty,
            'item_total': round(item_qty * item_price, 2),
            'cart_empty': len(cart) == 0,
        })

    return redirect('cart')


def remove_from_cart(request, part_id):
    cart = request.session.get('cart', {})
    key = str(part_id)

    if key in cart:
        removed_name = cart[key]['name']
        del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, f"Removed {removed_name} from cart.")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        total_count = sum(item['quantity'] for item in cart.values())
        subtotal = sum(float(item['price']) * item['quantity'] for item in cart.values())
        return JsonResponse({
            'status': 'success',
            'cart_count': total_count,
            'subtotal': round(subtotal, 2),
            'cart_empty': len(cart) == 0,
        })

    return redirect('cart')


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.info(request, "Your cart has been cleared.")
    return redirect('cart')


def delivery_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty! Please add some spare parts first.")
        return redirect('cart')

    subtotal = sum(float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in cart.values())

    shipping_rates = {
        'Standard': 0.0 if subtotal >= 1500 else 49.0,
        'Express': 149.0,
        'Doorstep Priority': 249.0,
    }

    eta_info = {
        'Standard': (datetime.date.today() + datetime.timedelta(days=4)).strftime("%d %b, %Y"),
        'Express': (datetime.date.today() + datetime.timedelta(days=2)).strftime("%d %b, %Y"),
        'Doorstep Priority': (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d %b, %Y"),
    }

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        delivery_method = request.POST.get('delivery_method', 'Standard')

        if not (full_name and phone and address and city and pincode):
            messages.error(request, "Please fill in all required delivery address fields.")
            return redirect('delivery')

        shipping_cost = shipping_rates.get(delivery_method, 49.0)
        total_price = subtotal + shipping_cost
        estimated_date = eta_info.get(delivery_method, "Within 3-5 days")

        order = Order.objects.create(
            order_id=Order.generate_order_id(),
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state if state else "Maharashtra",
            pincode=pincode,
            delivery_method=delivery_method,
            delivery_cost=shipping_cost,
            subtotal=subtotal,
            total_price=total_price,
            status='Placed',
            estimated_delivery=estimated_date
        )

        # Create Order Items
        for key, item in cart.items():
            part_id = item.get('id')
            part_obj = Part.objects.filter(id=part_id).first() if part_id else None
            price = float(item.get('price', 0))
            qty = int(item.get('quantity', 1))

            OrderItem.objects.create(
                order=order,
                part=part_obj,
                part_name=item.get('name', 'Automotive Spare Part'),
                price=price,
                quantity=qty,
                item_total=price * qty
            )

            # Update stock if part exists
            if part_obj and part_obj.stock >= qty:
                part_obj.stock -= qty
                part_obj.save()

        # Clear session cart
        request.session['cart'] = {}
        request.session.modified = True
        request.session['recent_order_id'] = order.order_id

        messages.success(request, f"Congratulations! Your order #{order.order_id} has been placed successfully!")
        return redirect('order_confirmation', order_id=order.order_id)

    # GET request: render checkout form
    cart_summary_items = []
    for key, item in cart.items():
        price = float(item.get('price', 0))
        qty = int(item.get('quantity', 1))
        cart_summary_items.append({
            'name': item.get('name'),
            'quantity': qty,
            'price': price,
            'item_total': round(price * qty, 2),
            'icon': item.get('icon', '⚙️'),
        })

    context = {
        'cart_items': cart_summary_items,
        'subtotal': round(subtotal, 2),
        'shipping_rates': shipping_rates,
        'eta_info': eta_info,
        'today': datetime.date.today().strftime("%d %b, %Y"),
    }
    return render(request, 'store/delivery.html', context)


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    items = order.items.all()

    # Define delivery milestones
    milestones = [
        {'id': 1, 'name': 'Order Placed', 'icon': '📝', 'desc': 'Order verified & received'},
        {'id': 2, 'name': 'Processing & Packing', 'icon': '⚙️', 'desc': 'Quality inspected & boxed'},
        {'id': 3, 'name': 'Dispatched / In Transit', 'icon': '🚚', 'desc': 'Handed over to courier'},
        {'id': 4, 'name': 'Out for Delivery', 'icon': '📍', 'desc': 'Agent assigned for doorstep delivery'},
        {'id': 5, 'name': 'Delivered', 'icon': '🏁', 'desc': 'Package safely delivered'},
    ]

    # Map status to milestone step index
    status_step_map = {
        'Placed': 1,
        'Processing': 2,
        'Dispatched': 3,
        'Out for Delivery': 4,
        'Delivered': 5,
    }
    current_step = status_step_map.get(order.status, 1)

    context = {
        'order': order,
        'items': items,
        'milestones': milestones,
        'current_step': current_step,
    }
    return render(request, 'store/confirmation.html', context)


def track_order(request):
    order_id = request.GET.get('order_id', '').strip()
    order = None
    searched = False

    if order_id:
        searched = True
        order = Order.objects.filter(order_id__iexact=order_id).first()

    recent_order_id = request.session.get('recent_order_id')
    recent_order = None
    if recent_order_id:
        recent_order = Order.objects.filter(order_id=recent_order_id).first()

    context = {
        'order_id': order_id,
        'order': order,
        'searched': searched,
        'recent_order': recent_order,
    }
    return render(request, 'store/track.html', context)