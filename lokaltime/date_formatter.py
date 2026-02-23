import datetime
import re

class DateFormatter:

    @staticmethod
    def date_name(date_str: str, part: str = 'month') -> str:
        """
            Returns a string representation of a specific part of a date.

            Args:
                date_str: A string representing a date.
                part: One of ['day', 'week_day', 'month', 'year'].

            Returns:
                str: The requested part of the date.

            Raises:
                TypeError: If the date is invalid or the part is unknown.
        """
        from .date_parser import DateParser as dp

        if not dp.is_date(date_str):
            raise TypeError('Invalid date format')

        dt = date(
            year = int(dp.year(date_str)),
            month = int(dp.month(date_str)),
            day = int(dp.day(date_str))
        )

        mapping = {
            'day': f"{dp.day(date_str):02}",
            'week_day': dt.strftime("%A"),
            'month': f"{dt.strftime("%B"):02}",
            'year': dt.strftime("%Y")
        }

        try:
            return mapping[part]
        except KeyError:
            raise TypeError("Invalid argument for date_name, part: expects ['day', 'month', 'year', 'week_day']")

    @staticmethod
    def date_trunc(date_str: str, arg: str = 'year') -> str | None:
        """
            Truncate a date string to the start of the day, month, or year.

            Args:
                date_str: A string representing a date.
                arg: One of ['day', 'month', 'year'].

            Returns:
                str: The truncated date string.
                None: If input format is invalid.

            Raises:
                TypeError: If `arg` is not 'day', 'month', or 'year'.
        """
        from .date_parser import DateParser as dp

        if not arg in ['day', 'month', 'year']:
            raise TypeError("Invalid argument for date_trunc, arg: expects ['day', 'month', 'year']")

        # If valid date, parse into date object
        if dp.is_date(date_str):
            dt = date(
                year=int(dp.year(date_str)),
                month=int(dp.month(date_str)),
                day=int(dp.day(date_str))
            )
            if arg == 'year':
                return f"{dt.year}-01-01"
            elif arg == 'month':
                return f"{dt.year}-{dt.month:02}-01"
            elif arg == 'day':
                return f"{dt.year}-{dt.month:02}-{dt.day:02}"

        # If invalid date, try partial parsing using regex
        pattern = r'^(\d{4})-?(\d{2})?-?(\d{2})?$'
        match = re.fullmatch(pattern, date_str)
        if not match:
            return None

        yy, mm, dd = match.groups()

        if arg == 'year':
            return f"{yy}-01-01"
        elif arg == 'month':
            if mm is None:
                return yy
            return f"{yy}-{mm}-01"
        elif arg == 'day':
            if mm is None or dd is None:
                return date_str  # fallback to original if incomplete
            return f"{yy}-{mm}-{dd}"
        return None

    @staticmethod
    def end_month(date_str: str) -> str:
        """
        Returns the last day of the month for a given date string.

        Args:
            date_str: A string representing a date.

        Returns:
            str: Date string for the last day of the month in YYYY-MM-DD format.

        Raises:
            TypeError: If the date format is invalid.
        """
        from .date_parser import DateParser as dp

        if not dp.is_date(date_str):
            raise TypeError("Invalid date format")

        year = int(dp.year(date_str))
        month = int(dp.month(date_str))

        # Use calendar module to get number of days in month
        last_day = calendar.monthrange(year, month)[1]

        return f"{year}-{month:02}-{last_day:02}"

    @staticmethod
    def start_month(date_str: str) -> str:
        """
        Returns the first day of the month for a given date string.

        Args:
            date_str: A string representing a date.

        Returns:
            str: Date string in YYYY-MM-DD format.

        Raises:
            TypeError: If the date format is invalid.
        """
        from .date_parser import DateParser as dp
        
        if not dp.is_date(date_str):
            raise TypeError("Invalid date format")

        # Delegate to date_trunc for month
        return DateFormatter.date_trunc(date_str, "month")

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


