from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from .models import Verify_Email,Cart,CartItem



RAZOR_KEY_ID="rzp_test_tQ8k6xZ3bQWVmF"
RAZOR_CLIENT_SECRET="ZlcRk3FbbcGu1rUl4AVOcSsM"

razorpay_client = razorpay.Client(
	auth=(RAZOR_KEY_ID, RAZOR_CLIENT_SECRET))

def getAmount(request):
    user=request.session.get("user")
    cart_items = CartItem.objects.filter(cart__user=user) 
    total_amount = sum(item.price for item in cart_items)
    currency = 'INR'
    amount = total_amount*100
    request.session["amount"]=amount
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))

    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
    data={}
    data['razorpay_order_id'] = razorpay_order_id
    data['razorpay_merchant_key'] = RAZOR_KEY_ID
    data['razorpay_amount'] = amount
    data['currency'] = currency
    data['callback_url'] = callback_url
    return JsonResponse(data)

def dash(request):
    if request.session.get("user"):

        context = {}

        context["user"]=request.session["user"]
        template = loader.get_template('dash.html')
        rendered_template = template.render(context, request)
        
        return HttpResponse(rendered_template)
    else:
        return redirect("login")

def delete_all_items(user):
    try:
        cart_items = CartItem.objects.filter(cart__user=user)
        cart_items.delete()
        return JsonResponse({"status": "ok", "message": "All items deleted from cart."}, status=200)
    except Exception as e:
        return JsonResponse({"status": "bad", "error": str(e)}, status=500)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                delete_all_items(request.session.get("user"))
                return render(request, 'paysuccess.html')
            else:
                return render(request, 'paymentfail.html', {'error': 'Payment signature verification failed'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)