from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'dash/dash.html')


def deposits(request):
    return render(request,'dash/deposits.html')


def withdraws(request):
    return render(request,'dash/withdraws.html')