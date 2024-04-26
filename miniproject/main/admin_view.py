from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from .models import ProductDB  

def submit_data(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        price = request.POST.get('price')
        code = request.POST.get('code')
        
        try:
            existing_product = ProductDB.objects.get(code=code)
            existing_product.name = name
            existing_product.quantity = quantity
            existing_product.category = category
            existing_product.price = price
            existing_product.save()
            return JsonResponse({'success': True})
        except ProductDB.DoesNotExist:
            new_product = ProductDB(name=name, quantity=quantity, category=category, price=price, code=code)
            new_product.save()
            return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)




def adminPanel(request):
    template = loader.get_template('adminpanel.html')
    return HttpResponse(template.render())  