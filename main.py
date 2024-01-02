from random import choice
from enum import Enum
from math import sqrt

MAX_RATING = 100
LATE_HOUR = 12  # If there is a lesson latter then LATE_HOUR then we will be subtracting LATE_HOUR_PENALTY.
LATE_HOUR_PENALTY = 20


class Day(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5


class Lecture:
    def __init__(self, name, start_hour: float, end_hour: float, lecture_day: Day):
        if start_hour >= end_hour:
            raise Exception('Start or end hour is not correct!')

        self.name = name
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.lecture_day = lecture_day


class Schedule:
    def __init__(self, lectures: list[Lecture]):
        self.monday = []
        self.tuesday = []
        self.wednesday = []
        self.thursday = []
        self.friday = []
        self.week = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday]

        if lectures is not None:
            for element in lectures:
                if element.lecture_day == Day.Monday:
                    self.monday.append(element)

                elif element.lecture_day == Day.Tuesday:
                    self.tuesday.append(element)

                elif element.lecture_day == Day.Wednesday:
                    self.wednesday.append(element)

                elif element.lecture_day == Day.Thursday:
                    self.thursday.append(element)

                elif element.lecture_day == Day.Friday:
                    self.friday.append(element)

    @staticmethod
    def is_overlapping(lecture1: Lecture, lecture2: Lecture) -> bool:
        return not (lecture1.end_hour <= lecture2.start_hour or lecture1.start_hour >= lecture2.end_hour)

    @staticmethod
    def calculate_distance(lecture1: Lecture, lecture2: Lecture) -> float:
        return abs(lecture1.end_hour - lecture2.start_hour)

    @property
    def rating(self) -> float:
        """
        Rating of this Schedule.

        :return: float
        """
        rating = 0

        for day in self.week:
            if not day:  # If the day has no lectures
                rating += MAX_RATING

            elif len(day) > 1:  # If there is more than one lecture in that day
                for i in range(len(day)):
                    for j in range(i + 1, len(day)):
                        if self.is_overlapping(day[i], day[j]):
                            return -100  # Return -100 if there is an overlap

                        if day[i].start_hour < LATE_HOUR or day[j].start_hour < LATE_HOUR:
                            rating -= LATE_HOUR_PENALTY

                        distance = self.calculate_distance(day[i], day[j])
                        if day[i].start_hour < LATE_HOUR or day[j].start_hour < LATE_HOUR:
                            rating += (MAX_RATING / sqrt((distance + 1)))

        return rating


def create_schedule() -> Schedule:
    return Schedule([
        choice(CALCULUS_LAB_LECTURES),
        choice(CALCULUS_THEORY_LECTURES),
        choice(PHY_THEORY_LECTURES),
        choice(PHY_LAB_LECTURES),
        choice(DL_LECTURES),
        choice(DL_LECTURES)
    ])


CALCULUS_LAB_LECTURES = [
    Lecture('Calculus L', 12, 14, Day.Monday),
    Lecture('Calculus L', 14, 16, Day.Tuesday),
    Lecture('Calculus L', 14.5, 16.5, Day.Friday)
]

CALCULUS_THEORY_LECTURES = [
    Lecture('Calculus T', 12, 15, Day.Tuesday),
    Lecture('Calculus T', 15, 18, Day.Wednesday)
]

PHY_LAB_LECTURES = [
    Lecture('Phy Lab', 15, 17, Day.Thursday),
    Lecture('Phy Lab', 9.5, 11.5, Day.Monday),
    Lecture('Phy Lab', 12, 14, Day.Friday)
]

PHY_THEORY_LECTURES = [
    Lecture('Phy Theory', 8.5, 11.5, Day.Wednesday),
    Lecture('Phy Theory', 8.5, 11.5, Day.Tuesday)
]

ENG_LECTURES = [
    Lecture('English', 11.5, 14.5, Day.Monday),
    Lecture('English', 12.5, 15.5, Day.Wednesday)
]

DL_LECTURES = [
    Lecture('Digital Logic', 14.5, 17.5, Day.Thursday),
    Lecture('Digital Logic', 12.5, 15.5, Day.Monday),
    Lecture('Digital Logic', 15, 18, Day.Friday),
]


schedules: list[Schedule] = []
repeat = 1000

for i in range(repeat):
    schedules.append(create_schedule())

sorted_schedules = sorted(schedules, key=lambda x: x.rating, reverse=True)
best = sorted_schedules[0].rating

for sort in sorted_schedules:
    if not sort.rating < best:
        print('------------')
        for day in sort.week:
            if not day == []:
                print('Day:', day[0].lecture_day.__str__().removeprefix('Day.'))
                for lecture in day:
                    print(f'-> {lecture.name}')

                print()
