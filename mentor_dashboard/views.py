from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def mentor_home(request):
    if request.user.role != "MENTOR":
        return redirect("/accounts/no-access/")
    return render(request, "mentor/dashboard.html")