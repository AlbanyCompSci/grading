from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson
from usermanage.models import SchoolClass


@login_required
def lessons_overview(request):
    if request.method == 'POST':
        if request.user.is_staff:
            school_class = SchoolClass.objects.get(id=request.POST['class_id'])
            school_class.password = request.POST['class_pwd']
            school_class.save()

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
