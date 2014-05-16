from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson


@login_required
def lessons_overview(request):
    classes = request.user.students.select_related()
    return render(request, 'lessons_overview.html', {
        'classes': classes,
    })

@login_required
def lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    return render(request, 'lesson.html', {
        'lesson': lesson,
    })