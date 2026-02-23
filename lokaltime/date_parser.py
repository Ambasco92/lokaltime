import re

class DateParser:
    @staticmethod
    def day(date_str: str) -> int | None:
        pattern = r'^\d{4}-\d{2}-(\d{2})$'
        match = re.search(pattern, date_str)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def month(date_str: str) -> int | None:
        pattern = r'^\d{4}-(\d{2})-\d{2}$'
        match = re.search(pattern, date_str)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def year(date_str: str) -> int | None:
        pattern = r'^(\d{4})-\d{2}-\d{2}$'
        match = re.search(pattern, date_str)
        if match:
            return int(match.group(1))
        return None

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

    @staticmethod
    def date_part(date_str: str, part: str = 'year') -> int | TypeError | None:
        from .date_util import DateUtil
        if DateParser.is_date(date_str):
            match part:
                case 'day':
                    return DateParser.day(date_str)
                case 'month':
                    return DateParser.month(date_str)
                case 'year':
                    return DateParser.year(date_str)
                case 'week':
                    return DateUtil.week(date_str)
                case 'week_day':
                    return DateUtil.week_day(date_str)
                case 'quarter':
                    return DateUtil.quarter(date_str)
                case _:
                    return TypeError(
                        "Invalid argument for date_part, part: "
                        "expects ['day', 'month', 'year', 'week', 'week_day', 'quarter']")
        else:
            raise TypeError('Invalid date format')
