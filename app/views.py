from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect

from django.contrib.auth.models import User
from .models import CheckIn, Soldier

from django.utils import timezone
from datetime import timedelta, datetime

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile')

    context = {'login_error': '',  'registration_error': ''}

    if request.method == "POST":
        if request.POST.get('login') is not None:
            un = request.POST.get('username')
            pw = request.POST.get('password')
            user = authenticate(username=un, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/profile')
            else:
                context['login_error'] = 'Invalid username or wrong password.'
        elif request.POST.get('register') is not None:
            un = request.POST.get('username')
            pw = request.POST.get('password')
            cp = request.POST.get('password2')
            if len(un) > 0:
                if len(pw) > 0:
                    if pw == cp:
                        if User.objects.filter(username=un).count() == 0:
                            user = User.objects.create_user(un, '', pw, first_name="OK")
                            login(request, user)
                            cin = CheckIn(owner=request.user, status='OK', datetime=timezone.now())
                            cin.save()
                            return HttpResponseRedirect('/profile')
                        else:
                            context['registration_error'] = 'Username already taken by a soldier'
                    else:
                            context['registration_error'] = 'The two passwords does not match. Enter the same password.'
                else:
                    context['registration_error'] = 'Password cannot be empty.'
            else:
                context['registration_error'] = 'Username cannot be empty.'


    return render(request, 'app/index.html', context)

def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    context = {'canpost': False, 'result': '', 'currentuser': request.user}

    if request.method == 'POST':
        if request.POST.get('ok') is not None:
            now = timezone.now()
            if CheckIn.objects.filter(owner=request.user, datetime__year=now.year, datetime__month=now.month, datetime__day=now.day).count() == 0:
                context['result'] = 'You already updated today. Not saving.'
            else:
                cin = CheckIn(owner=request.user, status='OK', datetime=now)
                cin.save()
                context['result'] = 'Update saved.'
        elif request.POST.get('fail') is not None:
            cin = CheckIn(owner=request.user, status='KO', datetime=timezone.now())
            cin.save()
            request.user.first_name = "KO"
            request.user.save()
            context['result'] = 'Update saved. Press F to pay respects.'
        elif request.POST.get('change_rank') is not None:
            if Soldier.objects.filter(user=request.user).count() == 0:
                Soldier.objects.create(user=request.user)
            request.user.soldier.rank = request.POST.get('newrank')
            try:
                request.user.soldier.save()
                context['result'] = "New rank saved."
            except:
                context['result'] = 'Unable to set rank.'
        else:
            context['result'] = 'Didn\'t do anything.'

    context['status'] = request.user.checkin_set.all().order_by('-datetime')[0]
    context['canpost'] = context['status'].status == "OK"

            
    return render(request, 'app/profile.html', context)

def user_view(request):
    context = {'error': '', 'quser': None, 'status': None}
    if request.GET.get('username') is not None:
        users = User.objects.filter(username=request.GET.get('username'))
        if len(users) == 0:
            context['error'] = 'A soldier with that username was not found'
        else:
            context['quser'] = users[0]
            context['status'] = users[0].checkin_set.all().order_by('-datetime')
            date_diff = timezone.now() - users[0].date_joined
            context['days_since_registration_days'] = date_diff.days
            context['days_since_registration_hours'] = date_diff.seconds/3600.0

    return render(request, 'app/soldier.html', context)

def status_view(request):
    context = {'registered': 0, 'ongoing': 0, 'failed': 0, 'success': 0, 'newregister': None, 'newfail': None, 'newgoing': None}

    context['registered'] = User.objects.count()
    context['ongoing'] = User.objects.filter(first_name="OK").count()
    if context['ongoing'] > 0:
        context['ongoing_percent'] = context['ongoing'] / context['registered'] * 100
    else:
        context['ongoing_percent'] = 0

    context['failed'] = User.objects.filter(first_name="KO").count()
    if context['failed'] > 0:
        context['failed_percent'] = context['failed'] / context['registered'] * 100
    else:
        context['failed_percent'] = 0

    context['success'] = CheckIn.objects.filter(datetime__year=2020, status="OK").order_by('owner').values('owner').distinct().count()
    if context['success'] > 0:
        context['success_percent'] = context['success'] / context['registered'] * 100
    else:
        context['success_percent'] = 0

    now = timezone.now()
    yesterday = now - timedelta(days=1)
    context['newregister'] = User.objects.filter(date_joined__gte=yesterday).order_by('-date_joined')
    context['newfail'] = User.objects.filter(first_name="KO", date_joined__gte=yesterday).order_by('-date_joined')
    context['newgoing'] = User.objects.filter(first_name="OK", date_joined__gte=yesterday).order_by('-date_joined')

    days = []

    ongoing_daily = []
    failed_daily = []
    members_daily = []

    ongoing_d = []
    failed_d = []

    startOfYear = datetime(2019, 1, 1, 23, 59, 59, 999)

    now = datetime.now()

    for i in range(367):
        currentq = startOfYear + timedelta(days=i)

        days.append(str(currentq.date()))
        succ_day = CheckIn.objects.filter(datetime__lte=currentq, status='OK').order_by('owner').values('owner').distinct().count()
        fail_day = CheckIn.objects.filter(datetime__lte=currentq, status='KO').count()
        total_members = User.objects.filter(date_joined__lte=currentq).count()
        ongoing_daily.append(succ_day)
        failed_daily.append(fail_day)
        members_daily.append(total_members)

        if currentq > now:
            break

    if (len(days) > 0):
        ongoing_d.append(ongoing_daily[0])
        failed_d.append(failed_daily[0])
        for i in range(1, len(days)):
            ongoing_d.append(ongoing_daily[i] - ongoing_daily[i-1])
            failed_d.append(failed_daily[i] - failed_daily[i-1])

    context['ongoing_day_c'] = ongoing_daily
    context['failed_day_c'] = failed_daily
    context['total_members_c'] = members_daily
    context['ongoing_d'] = ongoing_d
    context['failed_d'] = failed_d
    context['days'] = days

    dayssince = datetime.now() - datetime(2019, 1, 1)
    context['dayssince'] = dayssince.days
    context['dayssince_hours'] = dayssince.seconds / 3600.0
    daysuntil = datetime(2020, 1, 1) - datetime.now()
    context['daysuntil'] = daysuntil.days
    context['daysuntil_hours'] = daysuntil.seconds / 3600.0
    if context['daysuntil'] < 0:
        context['daysuntil'] = 0
        context['daysuntil_hours'] = 0
    
    if context['daysuntil'] == 0 and context['daysuntil_hours'] == 0:
        context['dayspercent'] = 100
    else:
        diff = datetime.now() - datetime(2019, 1, 1)
        context['dayspercent'] = (diff.days / 365.25 + diff.seconds / 31557600) * 100.0
    context['dayspercent_remaining'] = 100.0 - context['dayspercent']

    context['servertime'] = datetime.now()

    return render(request, 'app/status.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def fallen_view(request):
    return render(request, 'app/fallen.html', {'users': User.objects.filter(first_name='KO')})

def fighting_view(request):
    return render(request, 'app/fighting.html', {'users': User.objects.exclude(first_name='KO')})