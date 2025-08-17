from datetime import date, timedelta
from collections import defaultdict
from sqlalchemy.exc import OperationalError, ProgrammingError

def build_attendance_weeks(member_id: int, weeks: int = 52):
    from app import Attendance  # importu fonksiyonun içine aldık
    try:
        end = date.today()
        start = end - timedelta(weeks=weeks)
        rows = (Attendance.query
                .filter(Attendance.member_id == member_id,
                        Attendance.date.between(start, end),
                        Attendance.status == "attended")
                .all())
        counts = defaultdict(int)
        for r in rows:
            counts[r.date] += 1
        align = (start.weekday() + 6) % 7  # Pazartesi ile hizala
        cur = start - timedelta(days=align)
        days = []
        while cur <= end:
            days.append({"date": cur, "count": counts.get(cur, 0)})
            cur += timedelta(days=1)
        weeks_grid = [days[i:i+7] for i in range(0, len(days), 7)]
        return weeks_grid
    except (OperationalError, ProgrammingError):
        return [[]]
