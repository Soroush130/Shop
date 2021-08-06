from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from shop_todo.models import ToDoForm, ToDo


# Create your views here.

@login_required(login_url='/login')
def add_todo(request):
    todo = ToDo.objects.filter(user_id=request.user.id)
    paginator = Paginator(todo, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ToDo.objects.create(user_id=request.user.id, text=data['text'], time=data['time'], date=data['date'])
            return redirect(url)
    else:
        form = ToDoForm()
    context = {
        'form': form,
        'todo': todo,
        'page_obj': page_obj,
    }
    return render(request, 'account/todo-list.html', context)


@login_required(login_url='/login')
def remove_todo(request, id):
    url = request.META.get('HTTP_REFERER')
    todo = ToDo.objects.get(user_id=request.user.id, id=id)
    todo.delete()
    return redirect(url)
