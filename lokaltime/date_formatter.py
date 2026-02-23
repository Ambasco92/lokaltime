import datetime
import re

class DateFormatter:

    @staticmethod
    def date_name(date_str: str, part: str = 'month') -> str | TypeError | None:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            date = datetime.date(int(dp.year(date_str)), int(dp.month(date_str)), int(dp.day(date_str)))
            match part:
                case 'day':
                    return f"{dp.day(date_str):02}"
                case 'week_day':
                    return date.strftime("%A")
                case 'month':
                    return f"{date.strftime("%B"):02}"
                case 'year':
                    return f"{date.strftime("%Y")}"
                case _:
                    return TypeError(
                        "Invalid argument for date_name, part: expects ['day', 'month', 'year', 'week_day']")
        else:
            return TypeError('Invalid date format')

    @staticmethod
    def date_trunc(date_str: str, arg: str = 'year') -> str | TypeError | None:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            if arg == 'day':
                return date_str
            elif arg == 'month':
                pattern = r'^(\d{4})-?(\d{2})?-?(\d{2})?$'
                match = re.fullmatch(pattern, date_str)
                if not match:
                    return None

                yy, mm, dd = match.groups()

                if mm is None and dd is None:
                    return f'{yy}'
                else:
                    return f'{yy}-{mm}-01'
            elif arg == 'year':
                pattern = r'^(\d{4})-?(\d{2})?-?(\d{2})?$'
                match = re.fullmatch(pattern, date_str)
                if not match:
                    return None

                yy, mm, dd = match.groups()

                if mm is None and dd is None:
                    return f'{yy}'
                else:
                    return f'{yy}-01-01'
            else:
                return TypeError("Invalid argument for date_trunc, arg: expects ['day', 'month', 'year']")
        else:
            raise TypeError('Invalid date format')

    @staticmethod
    def end_month(date_str: str) -> str | TypeError:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if dp.month(date_str) == (1 or 3 or 5 or 7 or 8 or 10 or 12):
                return f"{dp.year(date_str)}-{dp.month(date_str):02}-{days_in_month[dp.month(date_str) - 1]}"
            elif dp.month(date_str) == 2:
                if dp.year(date_str) % 4 == 0 and (dp.year(date_str) % 100 != 0 or dp.year(date_str) % 400 == 0):
                    return f"{dp.year(date_str)}-{dp.month(date_str)}-{29}"  # Leap year
                else:
                    return f"{dp.year(date_str)}-{dp.month(date_str)}-{days_in_month[dp.month(date_str) - 1]}"
            else:
                return f"{dp.year(date_str)}-{dp.month(date_str)}-{days_in_month[dp.month(date_str) - 1]}"
        else:
            return TypeError("Invalid date format")

    @staticmethod
    def start_month(date_str: str) -> str | TypeError:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            return DateFormatter.date_trunc(date_str, "month")
        else:
            return TypeError("Invalid date format")

    @staticmethod
    def date_format(date_str: str, d_format: str = 'dd') -> str | TypeError:
        from .date_parser import DateParser as dp
        if dp.is_date(date_str):
            match d_format:
                case 'dd':
                    return DateFormatter.date_name(date_str, 'day')
                case 'ddd':
                    chars = DateFormatter.date_name(date_str, 'week_day')
                    return chars[:3]
                case 'dddd':
                    return DateFormatter.date_name(date_str, 'week_day')
                case 'mm':
                    return str(dp.month(date_str))
                case 'mmm':
                    chars = DateFormatter.date_name(date_str, 'month')
                    return chars[:3]
                case 'mmmm':
                    return DateFormatter.date_name(date_str, 'month')
                case 'yy':
                    chars = DateFormatter.date_name(date_str, 'year')
                    return chars[-2:]
                case 'yyyy':
                    return DateFormatter.date_name(date_str, 'year')
                case 'dd-mmm':
                    mmm = DateFormatter.date_name(date_str, 'month')
                    return f"{dp.date_part(date_str, 'day'):02} {mmm[:3]}"
                case 'dd-mmmm':
                    return f"{dp.date_part(date_str, 'day'):02} {DateFormatter.date_name(date_str, 'month')}"
                case 'mmm-yy':
                    mmm = DateFormatter.date_name(date_str, 'month')
                    yy = DateFormatter.date_name(date_str, 'year')
                    return f"{mmm[:3]} {yy[-2:]}"
                case 'mmm-yyyy':
                    mmm = DateFormatter.date_name(date_str, 'month')
                    return f"{mmm[:3]} {DateFormatter.date_name(date_str, 'year')}"
                case 'mmmm-yyyy':
                    return f"{DateFormatter.date_name(date_str, 'month')} {DateFormatter.date_name(date_str, 'year')}"
                case 'yyyy-mm-dd':
                    return f"{dp.date_part(date_str, 'year')}-{dp.date_part(date_str, 'month'):02}-{dp.date_part(date_str, 'day'):02}"
                case 'dd-mm-yyyy':
                    return f"{dp.date_part(date_str, 'day'):02}-{dp.date_part(date_str, 'month'):02}-{dp.date_part(date_str, 'year')}"
                case 'dd-mmm-yyyy':
                    mmm = DateFormatter.date_name(date_str, 'month')
                    return f"{dp.date_part(date_str, 'day'):02} {mmm[:3]}, {dp.date_part(date_str, 'year')}"
                case 'dd-mmmm-yyyy':
                    return f"{dp.date_part(date_str, 'day'):02} {DateFormatter.date_name(date_str, 'month')}, {dp.date_part(date_str, 'year')}"
                case 'dd-mm-yy':
                    yy = DateFormatter.date_name(date_str, 'year')
                    return f"{dp.date_part(date_str, 'day'):02}-{dp.date_part(date_str, 'month'):02}-{yy[-2:]}"
        else:
            return TypeError("Invalid date format")
