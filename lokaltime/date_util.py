import datetime
import re

class DateUtil:
    @staticmethod
    def week(date_str: str) -> int | TypeError | None:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            d = datetime.date(int(dp.year(date_str)), int(dp.month(date_str)), int(dp.day(date_str)))
            return d.isocalendar()[1]
        else:
            return TypeError('Invalid date')

    @staticmethod
    def week_day(date_str: str) -> int | TypeError:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            d = datetime.date(int(dp.year(date_str)), int(dp.month(date_str)), int(dp.day(date_str)))
            return d.weekday()
        else:
            return TypeError('Invalid date')

    @staticmethod
    def quarter(date_str: str) -> int | TypeError:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            return (dp.month(date_str) - 1) // 3 + 1
        else:
            return TypeError('Invalid date')

    @staticmethod
    def day_week(date_str: str) -> str | TypeError:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            d = datetime.date(int(dp.year(date_str)), int(dp.month(date_str)), int(dp.day(date_str)))
            return d.strftime("%A")
        else:
            return TypeError('Invalid date')

    @staticmethod
    def day_year(date_str: str) -> int | TypeError:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            d = datetime.date(int(dp.year(date_str)), int(dp.month(date_str)), int(dp.day(date_str)))
            return int(d.strftime("%j"))
        else:
            return TypeError('Invalid date')

    @staticmethod
    def is_date(date_str: str) -> bool:
        pattern = r'^\d{4}-?(?:\d{2})?-?(?:\d{2})?$'
        if not re.fullmatch(pattern, date_str):
            return False
        parts = date_str.split('-')

        # Year check
        yy: int = int(parts[0])
        if not (1900 <= yy <= 2100):
            return False

        if len(parts) > 1:
            # Month check
            mm: int = int(parts[1])
            if not (1 <= mm <= 12):
                return False

            if len(parts) > 2:
                # Day check
                dd: int = int(parts[2])

                days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if mm == 2 and (yy % 4 == 0 and (yy % 100 != 0 or yy % 400 == 0)):
                    max_day = 29  # Leap year
                else:
                    max_day = days_in_month[mm - 1]

                if not (1 <= dd <= max_day):
                    return False
        return True
