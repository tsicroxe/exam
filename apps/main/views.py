from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Travel

def index(request):
    print "Views/index"
    return redirect(reverse('main:main'))

def register(request):
    print "views/register"
    errors = {
        'name_short':'Name needs to be a minimum of 3 characters',
        'username_short':'Username needs to be a minimum of 3 characters',
        'email':'Not a valid email address',
        'password_length':'Password minimum length: 8',
        'mismatch':'Passwords do not match',
        'email_invalid':'Not a valid email account',
        'exists':'Account email does not exist'
        }

    result = User.objects.register(post=request.POST)
    print result[0]
    print result[1]
    if result[0] is True:
        error_list = result[1]
        for key,error in errors.iteritems():
            if key in error_list:
                print key
                messages.error(request, error)
        return redirect(reverse('main:index'))
    else:
        error = "Registration successful. Please login now"
        messages.error(request, error)
        return redirect(reverse('main:index'))

def login(request):
    errors = {
        'username_blank':'Username field cannot be blank. Please enter your username',
        'password_blank':'Password field cannot be blank. Please enter your password',
        'mismatch':'Passwords do not match',
        'username':'Username does not exist',
        }

    if request.method =="POST":

        print "Made it to login process"
        result = User.objects.login(post=request.POST)

        if result[0] is False:
            user = result[1]
            context = dict()
            for key in user:
                request.session[key] = user[key]
                context['key'] = request.session[key]
            print "Redirecting to travels"
            return redirect(reverse('main:travels'))

        elif result[0] is True:
            print result[1]
            error_list = result[1][0]
            print error_list
            for key,error in errors.iteritems():
                if key in error_list:
                    print key
                    messages.error(request, error)
            return redirect(reverse('main:index'))

def main(request):
    return render(request, 'main/index.html')

def add(request):
    return render(request, 'main/add.html')

def create(request):
    print request.POST
    errors = {
        'start_before_today':"Start date cannot be before today's date",
        'start_after_end':'Start date is after end date'
        }
    result = Travel.objects.create(post=request.POST)
    print result[0]
    print result[1]
    if result[0] is True:
        return redirect(reverse('main:travels'))
    else:
        error_list = result[1][0]
        for key,error in errors.iteritems():
            if key in error_list:
                print key
                messages.error(request, error)
        return redirect(reverse('main:add'))

def destination(request, id):
    user = Travel.objects.get(id=request.session['id'])
    context = {
        'user':user
    }
    return render(request, 'main/destination.html', context)

def travels(request):
    # user_to_exclude = User.objects.filter(id=request.session['id'])
    # other_users = Travel.objects.exclude(users=user_to_exclude)
    # other_users = User.objects.filter(id=other_users.id)

    # Joins are the death of me. I got bogged up on the datetimefield and joins

    context = {
    'travels':Travel.objects.all(),
    'other_users':User.objects.all()
    }
    return render(request, 'main/travels.html', context)

def logout(request):
    request.session.clear()
    return redirect(reverse('main:index'))
