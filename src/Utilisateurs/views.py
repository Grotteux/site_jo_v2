from django.shortcuts import render

# Create your views here.
def cgu(request):
    return render(request, 'cgu.html')

def account_profile(request):
    return render(request, 'account_profile.html')

