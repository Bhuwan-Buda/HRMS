from django.shortcuts import render, redirect, get_object_or_404
from vacancy.models import Vacancy, Apply
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="login")
def vacancy(request):
    vac = Vacancy.objects.filter(user=request.user)[::-1]
    context = {
        'vacancy': vac
    }
    return render(request, 'employee/vacancy.html', context)


@login_required(login_url="login")
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
        messages.add_message(request, messages.SUCCESS, "Vacancy successfully created!")
        return redirect('vacancy')

    return render(request, 'employee/create_vacancy.html')


@login_required(login_url="login")
def deletevacancy(request, id):
    vac = Vacancy.objects.get(id=id)
    vac.delete()
    messages.add_message(request, messages.ERROR, f"{vac.title} is deleted successfully!")
    return redirect('vacancy')


@login_required(login_url="login")
def viewvacancy(request, id):
    vac = get_object_or_404(Vacancy, id=id)
    app = Apply.objects.filter(vacancy_id=id)
    context = {
        'vacancy': vac,
        'apply': app
    }
    return render(request, 'employee/view_vacancy.html', context)


@login_required(login_url="login")
def editvacancy(request, id):
    vac = get_object_or_404(Vacancy, id=id)
    context = {
        'vacancy': vac
    }

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
            messages.add_message(request, messages.SUCCESS, "Vacancy is successfully edited!")
        else:
            v = Vacancy(title=title, description=des, qualification=qualify, experience=exp, salary=salary, final_date=date, user_id=uid)
            v.save()
            messages.add_message(request, messages.SUCCESS, "Vacancy is successfully created!")
        return redirect('vacancy')

    return render(request, 'employee/edit_vacancy.html', context)


@login_required(login_url="login")
def userVacancy(request):
    vac = Vacancy.objects.all()[::-1]
    context = {
        'vacancy': vac
    }
    return render(request, 'user/vacancy.html', context)


@login_required(login_url="login")
def viewuservacancy(request, id):
    context = {}
    vac = get_object_or_404(Vacancy, id=id)
    isApply = Apply.objects.filter(vacancy_id=id).exists()
    if isApply:
        aply = get_object_or_404(Apply, vacancy_id=id)
        context.update({
            'vacancy': vac,
            'apply': aply
        })
    else:
        context.update({
            'vacancy': vac
        })
    return render(request, 'user/view-vacancy.html', context)


@login_required(login_url="login")
def apply(request, id):
    vac = get_object_or_404(Vacancy, id=id)
    context = {
        'vacancy': vac
    }

    aply = Apply(vacancy_id=id, user_id=request.user.id)
    try:
        aply.save()
        messages.add_message(request, messages.SUCCESS, "You have successfully applied for this vacancy!")
    except:
        messages.add_message(request, messages.ERROR, "You have already applied for this vacancy!")

    return render(request, 'user/view-vacancy.html', context)


@login_required(login_url="login")
def hire(request, id):
    aply = get_object_or_404(Apply, id=id)
    try:
        aply.status = True
        aply.save()
        messages.add_message(request, messages.SUCCESS, "Successfully hired!")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "Already hired")

    return redirect('vacancy')
