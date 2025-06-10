from django.shortcuts import render
from django.views import View
from .forms import CalculatorForm
from decimal import Decimal, ROUND_HALF_UP
from .models import TableIpAddressSort, Table


def round_half_up(value, ndigits):
    return float(Decimal(str(value)).quantize(Decimal('1.' + '0'*ndigits), rounding=ROUND_HALF_UP))


class Calculator():
    def __init__(self, target=200, dist=1000):
        self.target = target
        self.dist = dist

    def resurt_one_try(self):
        try:
            value = ((-1 * float(self.target)) / (float(self.dist) / 100)) + 8
            if 1 <= round_half_up(value, 2) <= 6:
                return round_half_up(value, 2)
            else:
                return 0
        except:
            return 0

    def resurt_two_try(self):
        return round_half_up(self.resurt_one_try() * 0.75, 2)
    

    def resurt_three_try(self):
        return round_half_up(self.resurt_one_try() * 0.5, 2)


    def result_MRAD(self):
        try:
            return round_half_up(float(self.target) / (float(self.dist) * 0.1), 2)
        except:
            return 0

class CalculatorView(View):
    def get(self, request):
        form = CalculatorForm()
        current_ip = request.META.get('REMOTE_ADDR')
        recent_tables = TableIpAddressSort.objects.filter(ip=current_ip).order_by('-id')

        return render(request, 'calc/calc.html', {'form': form,
                                                  'recent_tables': recent_tables})

    def post(self, request):
        if 'clear' in request.POST:
            form = CalculatorForm()
            current_ip = request.META.get('REMOTE_ADDR')
            TableIpAddressSort.objects.filter(ip=current_ip).delete()
            recent_tables = []
            return render(request, 'calc/calc.html', {'form': form,
                                                  'recent_tables': recent_tables})
        
        
        form = CalculatorForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            dist = form.cleaned_data['dist']
            calculator = Calculator(target, dist)


            current_ip = request.META.get('REMOTE_ADDR')

            table = Table()
            table.target = target
            table.dist = dist
            table.first_try = calculator.resurt_one_try()
            table.second_try = calculator.resurt_two_try()
            table.third_try = calculator.resurt_three_try()
            table.mrad = calculator.result_MRAD()
            table.save()

            sort_table_for_ip = TableIpAddressSort()
            sort_table_for_ip.ip = current_ip
            sort_table_for_ip.table = table
            sort_table_for_ip.save()
            
            recent_tables = TableIpAddressSort.objects.filter(ip=current_ip).order_by('-id')

        return render(
            request, 'calc/calc.html', 
            {
                'form': form,
                'recent_tables': recent_tables
            })   

        
    