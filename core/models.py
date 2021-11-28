from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.base import Model

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=200, default=' ')
    pic = models.ImageField(upload_to='teachers/', default='teacher.jpg')

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=200, default=' ')
    roll = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='students/', default='student.jpg')

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=100, default=' ')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses')
    course_id = models.CharField(max_length=20)
    description = models.CharField(max_length=400, default=' ')
    classStartTime = models.TimeField(null=True, blank=True)
    classEndTime = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.course_id


class Update(models.Model):
    description = models.TextField(default=' ')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='updates')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course.title} - {self.datetime}'

    class Meta:
        ordering = ['-datetime',]


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default=' ')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    datetime = models.DateTimeField(auto_now_add=True)
    endtime = models.DateTimeField(blank=True)
    # solutions = models.ManyToManyField('AssignmentSolution')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-datetime',]


class AssignmentSolution(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE)
    marks = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    
    def __str__(self):
        return f'{self.student.user.username} - {self.assignment.title}'


