
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models



class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    description = models.TextField()  # Thêm trường description
    # Các trường khác của khoá học
    def __str__(self):
        return self.title



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField()

    def __str__(self):
        return self.title


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

# Định nghĩa Choice
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)