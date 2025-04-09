from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from notifications.utils.email_utils import send_emails
from django.contrib import messages
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct, PaymentGateway
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import hashlib
from django.views.decorators.csrf import csrf_exempt
import razorpay
from home.models import SiteSettings

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

@login_required
def place_order(request, total=0, quantity=0,):
    assigned_tax = SiteSettings.objects.all().first().gst_percentage
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (assigned_tax * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            data.user.first_name = form.cleaned_data['first_name']
            data.user.last_name = form.cleaned_data['last_name']
            data.user.address_line_1 = form.cleaned_data['address_line_1']
            data.user.address_line_2 = form.cleaned_data['address_line_2']
            data.user.city = form.cleaned_data['city']
            data.user.state = form.cleaned_data['state']
            data.user.country = form.cleaned_data['country']
            data.user.zip_code = form.cleaned_data['zip_code']
            data.user.save()
            
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')



@login_required
def proceed_payment(request,orderid):
    gateway = PaymentGateway.objects.all().first()
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=orderid)
    if request.user.wallet >= order.order_total:
        request.user.wallet = request.user.wallet - order.order_total
        request.user.save()
        payment = Payment(
            user = request.user,
            payment_id = order.order_number,
            payment_method = 'Wallet',
            amount_paid = order.order_total,
            status = 'pending',
        )
        
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()
    
            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
    
    
            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        CartItem.objects.filter(user=request.user).delete()
    
        payment.status = 'Completed'
        payment.save()
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        try:
            from home.models import SiteSettings
            settings = SiteSettings.objects.all().first()
            variables = {
                'payment': payment,
                'request': request,
                'settings': settings,
            }
            message = render_to_string('emails/order-confirmation.html', variables)
            send_emails('Order Confirmation & Payment Completed', message, [payment.user.email], message)
        except Exception as e:
            print(f'Error sending e-mail {e}')

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }

        return render(request, 'orders/order_complete.html', context)
            
    elif gateway.use == 'PAYU':
        payu_url = "https://secure.payu.in/_payment"  # Default to LIVE mode
        if gateway.mode == "TEST":
            payu_url = "https://test.payu.in/_payment"
        userid = request.user.first_name
        amount = order.order_total
        MERCHANT_KEY = gateway.payu_marchent_key
        SALT = gateway.payu_marchent_salt
        txnid = order.order_number
        productInfo = f'{order.user.first_name} order'
        firstname = request.user.first_name
        email = request.user.email
        phone = request.user.phone_number
        # Create the hash_string exactly as in PHP
        hash_string = f"{MERCHANT_KEY}|{txnid}|{amount}|{productInfo}|{firstname}|{email}|{userid}||||||||||{SALT}"
        # Generate the hash using SHA-512 and convert to lowercase
        hash_value = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        # Print the redirection message
        html_form = f"""
        <body>
        <form action="{payu_url}" method="post" name="payuForm">
              <input type="hidden" name="key" value="{MERCHANT_KEY}" />
             <input type="hidden" name="hash" value="{hash_value}"/>
             <input type="hidden" name="txnid" value="{txnid}" />
            <input type="hidden" name="amount" value="{amount}">
            <input type="hidden" name="productinfo" value="{productInfo}">
            <input type="hidden" name="firstname" value="{firstname}">
            <input type="hidden" name="email" value="{email}">
            <input type="hidden" name="phone" value="{phone}">
            <input type="hidden" name="mobile" value="{phone}">
            <input type="hidden" name="surl" value="{request.scheme}://{request.get_host()}/orders/payu_success/">
            <input type="hidden" name="furl" value="{request.scheme}://{request.get_host()}/orders/payu_failure/">
            <input type="hidden" name="udf1" value="{userid}">
            <input type="hidden" name="service_provider" value="payu_paisa" size="64" />
            <script>
            document.body.onload = function(ev){{
                 document.payuForm.submit();
            }}
            </script>
        </form>
        </body>
        """
        payment = Payment(
            user = request.user,
            payment_id = order.order_number,
            payment_method = gateway.use,
            amount_paid = order.order_total,
            status = 'pending',
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()
    
            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
    
    
            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # CartItem.objects.filter(user=request.user).delete()
        return HttpResponse(html_form)
    elif gateway.use == 'RAZORPAY':
        # RazorPay implementation
        amount = int(order.order_total * 100)  # RazorPay expects amount in paise
        currency = 'INR'
        razorpay_order_id = order.order_number
        
        # Create RazorPay client
        client = razorpay.Client(auth=(gateway.razorpay_id, gateway.razorpay_secret))
        
        # Create a RazorPay order
        razorpay_order = client.order.create({
            'amount': amount,
            'currency': currency,
            'receipt': razorpay_order_id,
            'payment_capture': '1'  # auto-capture payment
        })
        
        # Create payment record
        payment = Payment(
            user=request.user,
            payment_id=razorpay_order['id'],  # Using RazorPay order ID as payment_id
            payment_method=gateway.use,
            amount_paid=order.order_total,
            status='pending',
        )
        payment.save()
        
        # Update order with payment
        order.payment = payment
        order.save()
        
        # Prepare context for the template
        context = {
            'user': request.user,
            'order': order,
            'order_id': razorpay_order['id'],
            'razorpay_key_id': gateway.razorpay_id,
            'amount': amount,
            'currency': currency,
            'name': request.user.first_name,
            'email': request.user.email,
            'contact': request.user.phone_number,
            'callback_url': f"{request.scheme}://{request.get_host()}/orders/razorpay_callback/",
        }
        
        return render(request, 'orders/razorpay_payment.html', context)


@login_required
def razorpay_callback(request):
    payment_id = request.GET.get('razorpay_payment_id')
    order_id = request.GET.get('razorpay_order_id')
    signature = request.GET.get('razorpay_signature')
    error = request.GET.get('error')
    
    if not order_id:
        return redirect('razorpay_failure')
    
    try:
        gateway = PaymentGateway.objects.first()
        if not gateway:
            raise Exception("Payment gateway not configured")
        
        if error == 'payment_failed':
            try:
                # Get the most recent unprocessed order for this user with matching payment ID
                order = Order.objects.filter(
                    payment__payment_id=order_id,
                    user=request.user,
                    is_ordered=False
                ).latest('created_at')
                
                payment = order.payment
                payment.status = 'Failed'
                payment.save()
                return redirect('razorpay_failure')
            except Order.DoesNotExist:
                return redirect('razorpay_failure')
        
        # Verify the payment signature
        client = razorpay.Client(auth=(gateway.razorpay_key_id, gateway.razorpay_key_secret))
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            
            # Payment successful, update order and payment
            try:
                order = Order.objects.filter(
                    payment__payment_id=order_id,
                    user=request.user,
                    is_ordered=False
                ).latest('created_at')
                
                payment = order.payment
                
                # Mark payment as successful
                payment.status = 'Completed'
                payment.save()
                
                # Mark order as ordered
                order.is_ordered = True
                order.save()
                
                # Move cart items to order products
                cart_items = CartItem.objects.filter(user=request.user)
                
                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment = payment
                    orderproduct.user_id = request.user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.product_price = item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()
                    
                    product_variation = item.variations.all()
                    orderproduct.variations.set(product_variation)
                    
                    # Reduce product stock
                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()
                
                # Clear cart
                print('clearing cart')
                CartItem.objects.filter(user=request.user).delete()
                
                return redirect('razorpay_success')
                
            except Order.DoesNotExist:
                return redirect('razorpay_failure')
            
        except razorpay.errors.SignatureVerificationError:
            # Handle invalid signature
            return redirect('razorpay_failure')
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in razorpay_callback: {str(e)}")
        return redirect('razorpay_failure')

@csrf_exempt
def razorpay_success(request):
    try:
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_order_id = request.GET.get('razorpay_order_id')
        razorpay_signature = request.GET.get('razorpay_signature')
        
        # Find the payment record (using order_id as that's what we stored)
        payment = Payment.objects.filter(payment_id=razorpay_order_id).first()
        
        if payment:
            payment.status = 'Completed'
            payment.razorpay_payment_id = razorpay_payment_id  # Store payment ID for reference
            payment.razorpay_signature = razorpay_signature    # Store signature for verification
            payment.save()
            
            try:
                from home.models import SiteSettings
                settings = SiteSettings.objects.all().first()
                variables = {
                    'payment': payment,
                    'request': request,
                    'settings': settings,
                }
                message = render_to_string('emails/order-confirmation.html', variables)
                send_emails('Order Confirmation & Payment Completed', message, [payment.user.email], message)
            except Exception as e:
                print(f'Error sending e-mail {e}')

            # Mark order as completed if not already done in callback
            order = Order.objects.filter(payment=payment, is_ordered=False).first()
            if order:
                order.is_ordered = True
                order.save()

                cart_items = CartItem.objects.filter(user=request.user)
                
                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment = payment
                    orderproduct.user_id = request.user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.product_price = item.product.price
                    orderproduct.ordered = True
                    orderproduct.save()
                    
                    product_variation = item.variations.all()
                    orderproduct.variations.set(product_variation)
                    
                    # Reduce product stock
                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()
                
                CartItem.objects.filter(user=request.user).delete()

        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
    except Exception as e:
        print(f'RazorPay success error: {e}')
        return redirect('razorpay_failure')

    
    return render(request, 'orders/order_complete.html', context)

@csrf_exempt
def razorpay_failure(request):
    try:
        razorpay_order_id = request.GET.get('razorpay_order_id')
        # Find the payment record
        payment = Payment.objects.filter(payment_id=razorpay_order_id).first()
        
        if payment:
            payment.status = 'Failed'
            payment.save()
            messages.error(request, f'Payment failed for order {razorpay_order_id}.');
    except Exception as e:
        print(f'RazorPay failure error: {e}')

    return redirect("/cart/checkout/")


@login_required
def order_completed(request):
    return render(request, 'orders/order_complete.html')


@csrf_exempt
def payu_success(request):
    try:
        order_id = request.POST.get('txnid')
        pay = Payment.objects.filter(payment_id=order_id).first()
        pay.status = 'completed'
        pay.save()
        try:
            from home.models import SiteSettings
            settings = SiteSettings.objects.all().first()
            variables = {
                'payment': pay,
                'request': request,
                'settings': settings,
            }
            message = render_to_string('emails/order-confirmation.html', variables)
            send_emails('Order Confirmation & Payment Completed', message, [pay.user.email], message)
        except Exception as e:
            print(f'Error sending e-mail {e}')

    except Exception as e:
        print(f'success {e}')
    return redirect("/orders/order_complete/")


@csrf_exempt
def payu_failure(request):
    try:
        order_id = request.POST.get('txnid')
        pay = Payment.objects.filter(payment_id=order_id).first()
        pay.status = 'failed'
        pay.save()
    except Exception as e:
        print(f'fail {e}')
    return redirect("/orders/order_complete/")



def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    print('order_number')
    print(order_number)
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        print('order')
        print(order)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    # except (Payment.DoesNotExist, Order.DoesNotExist):
    except Exception as e:
        print(f'exception {e}')
        return redirect('home')
