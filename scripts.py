import re
from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, Commendation
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random

COMMENDATIONS_TEXT = [
    'Молодец!',
    'Отлично!',
    'Гораздо лучше, чем я ожидал!', 
    'Ты меня приятно удивил! Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
]

def fix_marks(schoolkid_name):
    """remove bad marks of schoolkid"""
    try:
        schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name).get()
    except MultipleObjectsReturned:
        return f'Учеников с именем {schoolkid_name} много'
    except ObjectDoesNotExist:
        return f'Ученик с именем {schoolkid_name} не найден'
    schoolkid_bad_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3],
    )
    schoolkid_bad_marks.update(
        points=F("points") + 2
    )

def remove_chastisements(schoolkid_name):
    """remove remove_chastisements of schoolkid"""
    try:
        schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name).get()
    except MultipleObjectsReturned:
        return f'Учеников с именем {schoolkid_name} много'
    except ObjectDoesNotExist:
        return f'Ученик с именем {schoolkid_name} не найден'
    schoolkid_chastisements = Chastisement.objects.filter(
        schoolkid=schoolkid
    )
    schoolkid_chastisements.delete()


def create_commendation(schoolkid_name, subject_name):
    """create commendations to schoolkid by subject"""
    try:
        schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name).get()
    except MultipleObjectsReturned:
        return f'Учеников с именем {schoolkid_name} много'
    except ObjectDoesNotExist:
        return f'Ученик с именем {schoolkid_name} не найден'
    subject_lessons = Lesson.objects.filter(
        subject__title=subject_name,
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
    )
    if not subject_lessons:
        return f'Предмета с названием {subject_name} не найдено'
    lesson_for_commendation = random.choice(subject_lessons)
    commendation_title = random.choice(COMMENDATIONS_TEXT)
    Commendation.objects.create(
        text=commendation_title,
        created=lesson_for_commendation.date,
        schoolkid=schoolkid,
        subject=lesson_for_commendation.subject,
        teacher=lesson_for_commendation.teacher,
    )




