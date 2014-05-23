from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from lessons.models import Lesson, Question
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


def update_questions(questions, lesson_id):
    questions = [q for q in questions if len(q) > 0]
    lesson = Lesson.objects.get(id=lesson_id)
    for question in lesson.questions.all():
        question.title = questions.pop(0)
        question.save()
    if len(questions) > 0:
        for title in questions:
            new_question = Question(title=title)
            new_question.save()
            lesson.questions.add(new_question)
        lesson.save()

@staff_member_required
def edit_lesson(request, id):
    if request.method == 'POST':
        if request.POST['action'] == 'update':
            update_questions(request.POST.getlist('questions[]'), id)
            return HttpResponse(status=200)
        elif request.POST['action'] == 'delete':
            Question.objects.get(id=request.POST['id']).delete()
            return HttpResponse(status=200)

    elif request.method == 'GET':
        lesson = Lesson.objects.get(id=id)
        return render(request, 'edit_lesson.html', {
            'lesson': lesson,
        })
