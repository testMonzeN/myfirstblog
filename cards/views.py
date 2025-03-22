from django.shortcuts import render,  redirect

# Create your views here.
def cards_list(request):
    return render(request, 'cards/cards.html', {
        'user': request.user.is_superuser
    })

def teleport_blog(request):
    return redirect('post_list')

def teleport_stepik(request):
    return redirect('main')
