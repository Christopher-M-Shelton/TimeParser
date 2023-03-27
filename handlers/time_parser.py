import logging
from structlog import wrap_logger
import re

logger = wrap_logger(logging.getLogger())

numbers = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
    "twenty-one",
    "twenty-two",
    "twenty-three",
    "twenty-four",
    "twenty-five",
    "twenty-six",
    "twenty-seven",
    "twenty-eight",
    "twenty-nine",
]


class TimeParser:
    def __init__(self, time_string):
        self.time_string = time_string
        self.log = logger.new(string=self.time_string)

    async def run(self):
        # HH:MM
        time_regex = r"([01]?[0-9]|2[0-3]):[0-5][0-9]"  # TODO: Regex to validate values with correct format over 24h

        if re.match(time_regex, self.time_string):
            return await self.print_time()
        else:
            self.log.error(f"Time input failed regex validation")
            raise ValueError("Invalid time input, format should be HH:MM with a maximum value of 23:59")

    async def print_time(self):

        hour = int(self.time_string[0:2])
        minutes = int(self.time_string[3:5])

        if hour >= 12:
            meridiem = "pm"
        else:
            meridiem = "am"

        if hour == 12 and minutes == 0:
            time_string = "midday"
            return time_string

        if (hour == 0 and minutes == 0) or hour == 24 and minutes == 0:
            time_string = "midnight"
            return time_string

        if hour > 12:
            hour = hour-12

        minutes_edge_cases = {
            "0": f"{numbers[hour]} o'clock {meridiem}",
            "15": f"quarter past {numbers[hour]} {meridiem}",
            "30": f"half past {numbers[hour]} {meridiem}",
            "45": f"quarter to {numbers[hour+1]}"
        }

        if minutes_edge_cases.get(str(minutes)):
            return minutes_edge_cases[str(minutes)]

        elif minutes > 30:
            minutes = 60 - minutes
            return f"{numbers[minutes]} to {numbers[hour+1]} {meridiem}"

        elif minutes < 30:
            return f"{numbers[minutes]} past {numbers[hour]} {meridiem}"
