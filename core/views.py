from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import AssignmentSolution, Teacher, Course, Student, Update, Assignment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    if request.user.is_authenticated:
        try:
            teacher = Teacher.objects.get(user=request.user)
            if teacher is not None:
                courses = Course.objects.filter(teacher=teacher)
                context = {
                    "courses": courses,
                }
                return render(request, 'core/teacher/teacherhome.html', context)
        except Exception as e:
            print(e)
            pass

        try:
            student = Student.objects.get(user=request.user)
            if student is not None:
                courses = student.courses.all()
                context = {
                    "courses": courses,
                }
                return render(request, 'core/student/studenthome.html', context)
        except Exception as e:
            print(e)
            pass

    return render(request, 'core/index.html')


def registerTeacher(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        college = request.POST["college"]
        password = request.POST["password"]

        user = User.objects.create_user(username, email, password)
        user.first_name = fname
        user.last_name = lname
        user.save()

        teacher = Teacher()
        teacher.college = college
        teacher.user = user
        teacher.save()

        login(request, user)

        return redirect('home')

    return render(request, 'core/teacher/registerteacher.html')


def loginTeacher(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'core/teacher/loginteacher.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def addCourse(request):
    if request.method == "POST":
        name = request.POST["cname"]
        code = request.POST["ccode"]
        description = request.POST["description"]

        c = Course()
        c.teacher = Teacher.objects.get(user=request.user)
        c.description = description
        c.course_id = code
        c.title = name
        c.save()

        return redirect('home')

    return render(request, 'core/teacher/addcourse.html')


def registerStudent(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        roll = request.POST["roll"]
        college = request.POST["college"]
        password = request.POST["password"]

        user = User.objects.create_user(username, email, password)
        user.first_name = fname
        user.last_name = lname
        user.save()

        student = Student()
        student.college = college
        student.user = user
        student.roll = roll
        student.save()

        login(request, user)

        return redirect('home')

    return render(request, 'core/student/registerstudent.html')


def loginStudent(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'core/student/loginstudent.html')


def enrollCourse(request):
    if request.method == "POST":
        student = Student.objects.get(user=request.user)
        code = request.POST["ccode"]
        course = Course.objects.get(course_id=code)
        course.students.add(student)
        
    return redirect('home')


def tClassroom(request, pk):
    try:
        classroom = Course.objects.get(course_id=pk)
        updates = Update.objects.filter(course=classroom)
        assignments = Assignment.objects.filter(course=classroom)
        if classroom.teacher.user != request.user:
            return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')
    
    context = {
        "classroom": classroom,
        "updates": updates,
        "assignments": assignments,
    }

    return render(request, 'core/teacher/classroom.html', context)


def sClassroom(request, pk):
    try:
        classroom = Course.objects.get(course_id=pk)
        updates = Update.objects.filter(course=classroom)
        assignments = Assignment.objects.filter(course=classroom)
        student = Student.objects.get(user=request.user)
        if student not in classroom.students.all():
            return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')

    context = {
        "classroom": classroom,
        "updates": updates,
        "assignments": assignments,
    }

    return render(request, 'core/student/classroom.html', context)


def submitUpdate(request, pk):
    course = Course.objects.get(course_id=pk)
    if request.method == "POST":
        description = request.POST["description"]
        update = Update()
        update.description = description
        update.course = course
        update.save()

    return redirect('t-classroom', pk=course.course_id)


def createAssignment(request, pk):
    course = Course.objects.get(course_id=pk)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        endtime = request.POST["endtime"]
        assignment = Assignment()
        assignment.title = title
        assignment.description = description
        assignment.endtime = endtime
        print(endtime)
        assignment.course = course
        assignment.save()
        return redirect('t-classroom', pk=course.course_id)
    
    return render(request, 'core/assignment/create.html')


from django.core.files.storage import FileSystemStorage
def assignment(request, pk):
    try:
        student = Student.objects.get(user=request.user)
        ass = Assignment.objects.get(id=pk)
        context = {
            "ass": ass,
        }
        try:
            sol = AssignmentSolution.objects.filter(student=student).filter(assignment=ass)
            if (sol.exists()):
                print(sol.first().marks)
                context = {
                    "ass": ass,
                    "submitted": True,
                    "sol": sol.first(),
                }
                return render(request, 'core/assignment/home.html', context)
        except Exception as e:
            print(e)
            
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            sol = AssignmentSolution()
            student = Student.objects.get(user=request.user)
            sol.student = student
            sol.assignment = ass
            sol.file = uploaded_file_url
            sol.save()
            return redirect('home')
    except Exception as e:
        print(e)
        pass

    try:
        teacher = Teacher.objects.get(user = request.user)
        ass = Assignment.objects.get(id=pk)
        sols = AssignmentSolution.objects.filter(assignment=ass)
        context = {
            "ass": ass,
            "sols": sols,
        }
        return render(request, 'core/assignment/homet.html', context)
    except Exception as e:
        print(e)
        pass

    return render(request, 'core/assignment/home.html', context)


def submitScore(request, pk, username):
    user = User.objects.get(username=username)
    ass = Assignment.objects.get(id=pk)
    if request.method == "POST":
        score = request.POST["score"]
        student = Student.objects.get(user=user)
        sol = AssignmentSolution.objects.filter(student=student).filter(assignment=ass)
        if (sol.exists):
            sol = sol.first()
            print(sol.student.user.username)
            sol.marks = score
            sol.save()
            print(sol.marks)
            return redirect('assignment', pk=pk)

    return redirect('assignment', pk=pk)


def setClassTime(request, pk):
    course = Course.objects.get(course_id=pk)
    if request.method == "POST":
        startime = request.POST["starttime"]
        endtime = request.POST["endtime"]
        course.classStartTime = startime
        course.classEndTime = endtime
        course.save()
        recipient_list = []
        for student in course.students.all():
            recipient_list.append(student.user.email)
        from_email = settings.EMAIL_HOST_USER
        send_mail(f"Class Timing - {course.title}", f"Your new class timings are from {startime} to {endtime}", from_email, recipient_list)
        return redirect('t-classroom', pk=pk)
    return redirect('t-classroom', pk=pk)

