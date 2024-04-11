from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from .models import Verify_Email,Cart,CartItem
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from reportlab.pdfgen import canvas
from io import BytesIO
import smtplib

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
        
        items_list = []
        total_price = 0
        for cart_item in cart_items:
            item_info = {
                'item': cart_item.item,
                'quantity': cart_item.quantity,
                'price': cart_item.price
            }
            total_price += cart_item.price
            items_list.append(item_info)
        
        cart_items.delete()
        
        pdf_data = generate_pdf(items_list, total_price)
        
        send_email_with_attachment(user.email, pdf_data)
        
        return JsonResponse({"status": "ok", "message": "All items deleted from cart and email sent."}, status=200)
    except Exception as e:
        return JsonResponse({"status": "bad", "error": str(e)}, status=500)

def generate_pdf(items_list, total_price):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    
    pdf.drawString(100, 800, "fazcheck")
    
    y_position = 750
    for item in items_list:
        pdf.drawString(100, y_position, f"Item: {item['item']}")
        pdf.drawString(300, y_position, f"Quantity: {item['quantity']}")
        pdf.drawString(500, y_position, f"Price: {item['price']}")
        y_position -= 20
    
    pdf.drawString(100, y_position - 40, f"Total Price: {total_price}")
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer

def send_email_with_attachment(email, pdf_data):
    subject = 'Your cart items'
    message = 'Please find attached your cart items in PDF format.'
    email_from = "notescratchonline@gmail.com"
    recipient_list = [email]
    
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = ', '.join(recipient_list)
    email_message['Subject'] = subject
    
    email_message.add_header('fazcheck', 'something')
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_data.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="cart_items.pdf"')
    email_message.attach(part)
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  
    smtp_username = "notescratchonline@gmail.com"
    smtp_password = "tkjs cmsk zzrk vugc"
    
    try:
        smtp_server = smtplib.SMTP(smtp_server, smtp_port)
        smtp_server.starttls()
        smtp_server.login(smtp_username, smtp_password)
        smtp_server.send_message(email_message)
        smtp_server.quit()
        
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
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