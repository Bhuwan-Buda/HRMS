from django.shortcuts import render, redirect, get_object_or_404
from vacancy.models import Vacancy
from django.contrib import messages

# Create your views here.


def deletevacancy(request, id):
    vac = Vacancy.objects.get(id=id)
    vac.delete()
    return redirect('vacancy')


def viewvacancy(request, id):
    vac = get_object_or_404(Vacancy, id=id)
    context = {
        'vacancy': vac
    }
    return render(request, 'employee/view_vacancy.html', context)


def editvacancy(request, id):
    if request.method == 'POST':
        title = request.POST['t']
        des = request.POST['d']
        qualify = request.POST['q']
        exp = request.POST['e']
        salary = request.POST['s']
        date = request.POST['dat']
        uid = request.POST['v']
        isVacancy = Vacancy.objects.filter(id=id).exists()
        if isVacancy:
            v = Vacancy.objects.get(id=id)
            v.title = title
            v.description = des
            v.qualification = qualify
            v.experience = exp
            v.salary = salary
            v.final_date = date
            v.save()
        else:
            v = Vacancy(title=title, description=des, qualification=qualify, experience=exp, salary=salary, final_date=date, user_id=uid)
            v.save()
        return redirect('vacancy')

    return render(request, 'employee/edit_vacancy.html')


def vacancy(request):
    vac = Vacancy.objects.all()[::-1]
    context = {
        'vacancy': vac
    }
    return render(request, 'employee/vacancy.html', context)


def createvacancy(request):
    if request.method == 'POST':
        title = request.POST['title']
        des = request.POST['description']
        qualify = request.POST['qualification']
        exp = request.POST['experience']
        salary = request.POST['salary']
        date = request.POST['date']
        uid = request.POST['vac']
        v = Vacancy(title=title, description=des, qualification=qualify, experience=exp, salary=salary, final_date=date, user_id=uid)
        v.save()
        return redirect('vacancy')

    return render(request, 'employee/create_vacancy.html')