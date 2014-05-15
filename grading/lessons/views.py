from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def view_lessons(request):
    return render(request, 'lesson_overview.html', {})