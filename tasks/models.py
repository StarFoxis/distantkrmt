from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from registration.models import Student, Teacher, Subject, NumGroup

# Create your models here.
# Оценка
# Задание
# Задание-студент
# Ответ

class Appraisal(models.Model):
    name = models.CharField('Название', max_length=100)
    number = models.PositiveSmallIntegerField('Оценка')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField('Название', max_length=200)
    task = models.FileField(upload_to ='tasks/%Y/%m/%d/', verbose_name='Задание')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')
    num_group = models.ForeignKey(NumGroup, on_delete=models.CASCADE, verbose_name='Номер группы')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет') 
    date_start = models.DateField('Дата создания', default=timezone.now)
    date_end = models.DateField('Дата окончания', default=timezone.now)
    active = models.BooleanField('Открыто', default=True)
    date_opening = models.DateField('Дата открытия', blank=True, null=True)

    def openTask(self):
        date_now = timezone.now()
        if not self.active and self.date_opening:
            date_now = timezone.now().date()
            if date_now>=self.date_opening:
                self.active = True
                self.save()
                return True
            return False
        return True

    def closeTask(self):
        date_now = timezone.now().date()
        return date_now>self.date_end

    def seenTask(self):
        date_seen = timezone.now().date()
        result = self.date_end-date_seen
        return abs(result.days)<=7

    def get_absolute_url(self):
        return reverse('detail-task', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        self.openTask()
        return f'{self.teacher} - {self.name}'

class Answer(models.Model):
    name = models.CharField('Название', max_length=200, blank=True)
    answer = models.FileField(upload_to ='answers/%Y/%m/%d/', verbose_name='Ответ')
    # student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    # task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задание')
    date_present = models.DateField('Дата отправки', default=timezone.now)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.name

class TaskStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задание')
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ответ')
    appraisal = models.ForeignKey(Appraisal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оценка')
    state = models.BooleanField('Сделано', default=False)

    def get_absolute_url(self):
        return reverse('list-answer', kwargs={'task': self.task_id})

    class Meta:
        verbose_name = 'Студент-Задание'
        verbose_name_plural = 'Студент-Задания'

    def __str__(self):
        return f'{self.student} - {self.task} - {self.state}'

@receiver(post_save, sender=Task)
def create_task_student(sender, instance, created, **kwargs):
    if created:
        students = Student.objects.filter(num_group=instance.num_group)
        for student in students:
            task_student = TaskStudent.objects.create(student=student, task=instance).save()