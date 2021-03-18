from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Предмет
# Группа
# Номер группы
# Студент
# Преподаватель

class Subject(models.Model):
    name = models.CharField('Название', max_length=100)
    desc = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField('Название', max_length=100)
    desc = models.TextField('Описание', blank=True)
    # max_student = models.PositiveSmallIntegerField('Макс. студентов')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name

class NumGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    name = models.CharField('Название', max_length=100)
    course = models.PositiveSmallIntegerField('Курс')
    subjects = models.ManyToManyField(Subject, verbose_name='Предметы')

    class Meta:
        verbose_name = 'Номер группы'
        verbose_name_plural = 'Номера групп'

    def __str__(self):
        return f'{self.group} - {self.name}'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    num_group = models.ForeignKey(NumGroup, on_delete=models.SET_NULL, null=True, verbose_name='Номер группы')

    class Meta:
        ordering = ('num_group', )
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.user.username}: {self.num_group}'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    num_groups = models.ManyToManyField(NumGroup, verbose_name='Номера групп')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f'{self.user.username}:  {self.str_groups()}'

    def str_groups(self):
        return ','.join(self.num_groups.all().values_list('name', flat=True))
