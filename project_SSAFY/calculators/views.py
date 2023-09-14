from django.shortcuts import render

# Create your views here.
def calculation(request):
    return render(request, 'calculators/calculation.html')

def result(request):
    first = int(request.GET.get('first'))
    second = int(request.GET.get('second'))
    minus = first - second
    times = first * second
    divide = first / second if second != 0 else 0
    context = {
        'first': first,
        'second': second,
        'minus': minus,
        'times': times,
        'divide': divide,
    }
    return render(request, 'calculators/result.html', context)