from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def lessons_overview(request):
    return render(request, 'lessons_overview.html', {})

def lesson(request, id):
	return render(request, 'lesson.html', {})