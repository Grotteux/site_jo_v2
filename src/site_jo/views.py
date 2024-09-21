from django.shortcuts import render

def vue_principal(request):
    return render(request, 'index.html')

def vue_contact(request):
    return render(request, 'contact.html')

def vue_billet_connect(request):
    return render(request, 'billet_connect.html')