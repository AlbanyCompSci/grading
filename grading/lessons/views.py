from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from lessons.models import Lesson, Question, Response
from usermanage.models import SchoolClass


@login_required
def lessons_overview(request):
    if request.method == 'POST':
        if request.user.is_staff:
            school_class = SchoolClass.objects.get(id=request.POST['class_id'])
            school_class.password = request.POST['class_pwd']
            school_class.save()

    if request.user.is_staff:
        classes = request.user.teachers.select_related()
    else:
        classes = request.user.students.select_related()
    return render(request, 'lessons_overview.html', {
        'classes': classes,
    })


@login_required
def lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    if request.GET.get('grade_class'):
        school_class = SchoolClass.objects.get(id=request.GET['grade_class'])
    else:
        school_class = None
    return render(request, 'lesson.html', {
        'lesson': lesson,
        'school_class': school_class,
    })


@staff_member_required
def grade_question(request, class_id, id):
    question = Question.objects.get(id=id)

    school_class = SchoolClass.objects.get(id=class_id)
    students = school_class.students.all()
    responses = Response.objects.filter(
        answerer__in=students,
        question=question
    )

    unanswered_students = []
    for student in students:
        try:
            Response.objects.get(answerer=student, question=question)
        except Response.DoesNotExist:
            unanswered_students.append(student.get_full_name())
    unanswered_students = ', '.join(unanswered_students) if unanswered_students else None

    return render(request, 'question.html', {
        'question': question,
        'responses': responses,
        'unanswered_students': unanswered_students,
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


@staff_member_required
def mark_response_seen(request):
    response = Response.objects.get(id=request.POST['id'])
    response.seen = True
    response.save()
    return HttpResponse(status=200)


@staff_member_required
def save_comment(request):
    for id in request.POST.keys():
        response = Response.objects.get(id=id)
        response.seen = True  # redundant
        response.comment = request.POST[id]
        response.save()
    return HttpResponse(status=200)


@login_required
def save_responses(request):
    responses = request.POST.items()
    # first element of list is the lesson id:
    lesson = Lesson.objects.get(id=responses.pop(0)[1])
    for id in responses:
        try:
            response = Response.objects.get(id=id[0], answerer=request.user)
            response.text = request.POST[id[0]]
            response.save()
        except ValueError:
            response = Response(
                text=request.POST[id[0]],
                answerer=request.user,
                question=Question.objects.get(id=id[0][4:]),
                lesson=lesson
            )
            response.save()
    return HttpResponse(status=200)
