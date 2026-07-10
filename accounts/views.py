from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role != role and not user.is_superuser:
                    return render(request, 'registration/login.html', {'error': 'Role does not match this account.'})
            except UserProfile.DoesNotExist:
                if not user.is_superuser:
                    return render(request, 'registration/login.html', {'error': 'No profile found for this account.'})

            login(request, user)
            return redirect('dashboard_redirect')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return render(request, 'dashboards/admin_dashboard.html')
    try:
        profile = UserProfile.objects.get(user=request.user)
        return render(request, f'dashboards/{profile.role}_dashboard.html')
    except UserProfile.DoesNotExist:
        return render(request, 'registration/login.html', {'error': 'No role assigned. Contact admin.'})