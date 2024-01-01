from random import choice
from enum import Enum
from math import sqrt

MAX_RATING = 100
RATING_MULTIPLIER = 0.8  # If there is a lesson latter then LATE_HOUR then we will be subtracting LATE_HOUR_PENALTY.
LATE_HOUR = 12
LATE_HOUR_PENALTY = 20


class Day(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5


class Lecture:
    def __init__(self, start_hour: float, end_hour: float, day: Day):
        if start_hour >= end_hour:
            raise Exception('Start or end hour is not correct!')

        self.start_hour = start_hour
        self.end_hour = end_hour
        self.day = day


class Schedule:
    def __init__(self, lectures: list[Lecture]):
        self.monday = []
        self.tuesday = []
        self.wednesday = []
        self.thursday = []
        self.friday = []
        self.week = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday]

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


def create_schedule():
    return Schedule([
        choice(CALCULUS_LAB_LECTURES),
        choice(CALCULUS_THEORY_LECTURES),
        choice(PHY_THEORY_LECTURES),
        choice(PHY_LAB_LECTURES),
        choice(DL_LECTURES),
        choice(DL_LECTURES)
    ])


CALCULUS_LAB_LECTURES = [
    Lecture(12, 14, Day.Monday),
    Lecture(14, 16, Day.Tuesday),
    Lecture(14.5, 16.5, Day.Friday)
]

CALCULUS_THEORY_LECTURES = [
    Lecture(12, 15, Day.Tuesday),
    Lecture(15, 18, Day.Wednesday)
]

PHY_LAB_LECTURES = [
    Lecture(15, 17, Day.Thursday),
    Lecture(9.5, 11.5, Day.Monday),
    Lecture(12, 14, Day.Friday)
]

PHY_THEORY_LECTURES = [
    Lecture(8.5, 11.5, Day.Wednesday),
    Lecture(8.5, 11.5, Day.Tuesday)
]

ENG_LECTURES = [
    Lecture(11.5, 14.5, Day.Monday),
    Lecture(12.5, 15.5, Day.Wednesday)
]

DL_LECTURES = [
    Lecture(14.5, 17.5, Day.Thursday),
    Lecture(12.5, 15.5, Day.Monday),
    Lecture(15, 18, Day.Friday),
]


SCHEDULES: list[Schedule] = []
repeat = 10

for i in range(repeat):
    SCHEDULES.append(create_schedule())

sorted_schedules = sorted(SCHEDULES, key=lambda x: x.rating, reverse=True)

print(sorted_schedules[0].rating)
