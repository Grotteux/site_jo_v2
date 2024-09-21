import qrcode
from django.db.models import Count
from django.shortcuts import render
import io
import base64

from .decorators import two_factor_required
from .models import Ticket, Purchase
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
import json

@two_factor_required
@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket/ticket_list.html', {'tickets': tickets})


@login_required
def process_purchase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_tickets = data.get('tickets', [])
        purchases = []

        for ticket_data in selected_tickets:
            ticket_id = ticket_data.get('id')
            quantity = ticket_data.get('quantity', 1)

            ticket = Ticket.objects.get(id=ticket_id)

            for _ in range(quantity):
                purchase = Purchase.objects.create(ticket=ticket, user=request.user)
                purchases.append({
                    'ticket': ticket.type,
                    'price': str(ticket.price),
                    'unique_key': str(purchase.unique_key)
                })
        return JsonResponse({'status': 'success', 'purchases': purchases})
@two_factor_required
@login_required
def my_tickets(request):
    user_purchases = Purchase.objects.filter(user=request.user).select_related('ticket')
    return render(request, 'ticket/my_ticket.html', {'purchases': user_purchases})

@two_factor_required
@login_required
def my_tickets(request):
    user_purchases = Purchase.objects.filter(user=request.user).select_related('ticket')
    purchases_with_qr = []
    for purchase in user_purchases:
        qr_data = purchase.get_qr_data()
        qr_image = qrcode.make(qr_data)
        buf = io.BytesIO()
        qr_image.save(buf, format='PNG')
        buf.seek(0)
        qr_code_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        purchases_with_qr.append({
            'purchase': purchase,
            'qr_code_base64': qr_code_base64
        })
    return render(request, 'ticket/my_ticket.html', {'purchases_with_qr': purchases_with_qr})

def is_employee(user):
        return user.is_staff

@user_passes_test(is_employee, login_url='home')
def validate_qr(request):
    return render(request, 'ticket/validate_qr.html')

@user_passes_test(is_employee, login_url='home')
def admin_dashboard(request):
    # Calcul du nombre total de tickets vendus
    total_tickets_vendus = Purchase.objects.count()

    # Calcul du nombre de tickets vendus par type
    tickets_par_type = Purchase.objects.values('ticket__type').annotate(nombre_vendus=Count('ticket__type'))

    context = {
        'total_tickets_vendus': total_tickets_vendus,
        'tickets_par_type': tickets_par_type,
    }
    return render(request, 'ticket/admin_dashboard.html', context)


