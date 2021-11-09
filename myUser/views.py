from django.shortcuts import render, redirect, get_object_or_404
from myUser.models import User, Education, Skill, Experience
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from vacancy.models import Vacancy

# Create your views here.


def homepage(request):
    return redirect('login')


def signup(request):
    context = {}
    if request.method == 'POST':
        name = request.POST['fullname']
        address = request.POST['address']
        email = request.POST['email']
        number = request.POST['contact']
        password = request.POST['password']
        password2 = request.POST['password2']
        select = request.POST['selectOption']
        context.update({
            'name': name,
            'address': address,
            'email': email,
            'number': number,
            'select': select
        })
        # fullname validation
        if len(name) == 0:
            messages.add_message(request, messages.ERROR, "Fullname should not be empty!")
            return render(request, 'master/signup.html', context)

        # address validation
        if len(address) == 0:
            messages.add_message(request, messages.ERROR, "Address should not be empty!")
            return render(request, 'master/signup.html', context)

        # password validation
        if len(password) <= 5:
            messages.add_message(request, messages.ERROR, "Password length should be greater than 5 !!!")
            return render(request, 'master/signup.html', context)

        if password == password2:
            u = User(email=email, fullname=name, address=address, contactNo=number)
            u.set_password(password)
            if select == 'user':
                u.isUser = True
            else:
                u.isEmployee = True
            try:
                u.save()
                messages.add_message(request, messages.SUCCESS, "Signup Successfully !!!")
                return render(request, 'master/login.html', context)
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
        else:
            messages.add_message(request, messages.ERROR, "Password does not match ! Please enter same password !!!")
            return render(request, 'master/signup.html', context)

    return render(request, 'master/signup.html', context)


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if user.isUser:
                return redirect('userDashboard')
            return redirect('employeeDashboard')
        else:
            messages.add_message(request, messages.ERROR, "Email and password does not match !!!")
            return redirect('login')
    return render(request, 'master/login.html')


def signout(request):
    logout(request)
    return redirect('login')


def delete(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return redirect('login')


@login_required(login_url='login')
def userDashboard(request):
    context = {}
    try:
        context.update({
            'edu': Education.objects.get(user=request.user),
            'user_count': User.objects.filter(isUser=True).count(),
            'employee_count': User.objects.filter(isEmployee=True).count(),
            'vacancy_count': Vacancy.objects.count()
        })
    except Exception as e:
        return render(request, 'user/dashboard.html', context)
    return render(request, 'user/dashboard.html', context)


@login_required(login_url='login')
def employeeDashboard(request):
    context = {}
    try:
        context.update({
            'user_count': User.objects.filter(isUser=True).count(),
            'employee_count': User.objects.filter(isEmployee=True).count(),
            'vacancy_count': Vacancy.objects.count()
        })
    except Exception as e:
        return render(request, 'employee/dashboard.html', context)
    return render(request, 'employee/dashboard.html', context)


def profile(request):
    context = {}
    try:
        context.update({
            'edu': Education.objects.get(user=request.user),
            'skl': Skill.objects.get(user=request.user),
            'exp': Experience.objects.get(user=request.user)
        })
    except Exception as e:
        messages.add_message(request, messages.ERROR, "We do not have any details to show!! Please provide all the details.")
        return render(request, 'user/education.html')
    return render(request, 'user/profile.html', context)


def education(request):
    if request.method == 'POST':
        inst = request.POST['institution']
        course = request.POST['course']
        level = request.POST['selectLevel']
        image = request.FILES['image']
        gender = request.POST['radiobutton']
        country = request.POST['country']
        file = request.FILES['file']
        uid = request.POST['edu']
        isEducation = Education.objects.filter(user=request.user).exists()
        if isEducation:
            e = Education.objects.get(user=request.user)
            e.institutionName = inst
            e.majorCourse = course
            e.level = level
            e.img = image
            e.gender = gender
            e.country = country
            e.file = file
            e.save()
        else:
            e = Education(institutionName=inst, majorCourse=course, gender=gender, level=level, img=image, country=country,file=file, user_id=uid)
            e.save()
        return render(request, 'user/skill.html')
    return render(request, 'user/education.html')


def skill(request):
    context = {}
    if request.method == 'POST':
        skl = request.POST['textarea']
        uid = request.POST['skl']
        context.update({
            'skill': skl
        })
        isSkill = Skill.objects.filter(user=request.user).exists()
        if isSkill:
            s = Skill.objects.get(user=request.user)
            s.skill = skl
            s.save()
        else:
            s = Skill(skill=skl, user_id=uid)
            s.save()
        return render(request, 'user/experience.html')
    return render(request, 'user/skill.html', context)


def experience(request):
    if request.method == 'POST':
        exp = request.POST['exptextarea']
        uid = request.POST['exp']
        isExperience = Experience.objects.filter(user=request.user).exists()
        if isExperience:
            e = Experience.objects.get(user=request.user)
            e.experience = exp
            e.save()
        else:
            e = Experience(experience=exp, user_id=uid)
            e.save()
        return redirect('profile')
    return render(request, 'user/experience.html')


def userlist(request):
    context = {}
    try:
        context.update({
            'employee': User.objects.filter(isUser=True, is_admin=False)[::-1]
        })
    except Exception as e:
        messages.add_message(request, messages.ERROR, "We do not have any details to show!!")
        return render(request, 'employee/userlist.html')
    return render(request, 'employee/userlist.html', context)


def viewuser(request, id):
    user = get_object_or_404(User, id=id, isUser=True, is_admin=False)
    e = get_object_or_404(Education, user=id)
    s = get_object_or_404(Skill, user=id)
    ex = get_object_or_404(Experience, user=id)
    context = {
        'user': user,
        'edu': e,
        'skl': s,
        'exp': ex
    }
    return render(request, 'employee/view.html', context)
