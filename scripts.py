import logging
import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import F

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)

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


logging.basicConfig(
    format="%(pathname)s %(lineno)d %(message)s",
    filename='logs_for_script.log',
    encoding='utf-8',
)


def get_schoolkid(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(
            full_name__contains=schoolkid_name,
        )
    except MultipleObjectsReturned:
        logging.error(f'Учеников с именем {schoolkid_name} много')
    except ObjectDoesNotExist:
        logging.error(f'Ученик с именем {schoolkid_name} не найден')
    else:
        return schoolkid


def fix_marks(schoolkid_name):
    """remove bad marks of schoolkid"""
    schoolkid = get_schoolkid(schoolkid_name=schoolkid_name)
    if not schoolkid:
        return None
    schoolkid_bad_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3],
    )
    schoolkid_bad_marks.update(
        points=F("points") + 2
    )


def remove_chastisements(schoolkid_name):
    """remove remove_chastisements of schoolkid"""
    schoolkid = get_schoolkid(schoolkid_name=schoolkid_name)
    if not schoolkid:
        return None
    schoolkid_chastisements = Chastisement.objects.filter(
        schoolkid=schoolkid
    )
    schoolkid_chastisements.delete()


def create_commendation(schoolkid_name, subject_name):
    """create commendations to schoolkid by subject"""
    schoolkid = get_schoolkid(schoolkid_name=schoolkid_name)
    if not schoolkid:
        return None
    subject_lessons = Lesson.objects.filter(
        subject__title=subject_name,
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
    )

    if not subject_lessons:
        logging.error(f'Предмета с названием {subject_name} не найдено')
        return None
    lesson_for_commendation = random.choice(subject_lessons)
    commendation_title = random.choice(COMMENDATIONS_TEXT)
    Commendation.objects.create(
        text=commendation_title,
        created=lesson_for_commendation.date,
        schoolkid=schoolkid,
        subject=lesson_for_commendation.subject,
        teacher=lesson_for_commendation.teacher,
    )
