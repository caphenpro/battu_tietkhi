"""Âm lịch: xác định tháng nhuận theo sóc và trung khí (thuật toán Meeus / Hồ Ngọc Đức).

Chỉ dùng thư viện chuẩn. Múi giờ mặc định UTC+7 (Việt Nam); dùng 8 cho Trung Quốc.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, floor, pi, sin
from datetime import date

__all__ = ["LunarMonth", "leap_month", "lunar_months", "new_moon_day",
           "sun_sector", "jd_from_date", "date_from_jd"]

PI = pi
TRUNG_KHI = ["Xuân phân", "Cốc vũ", "Tiểu mãn", "Hạ chí", "Đại thử", "Xử thử",
             "Thu phân", "Sương giáng", "Tiểu tuyết", "Đông chí", "Đại hàn", "Vũ thủy"]


def jd_from_date(d: int, m: int, y: int) -> int:
    """Ngày dương lịch (Gregory/Julian trước 15/10/1582) -> số ngày Julian (JDN)."""
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    jd = d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045
    if jd < 2299161:
        jd = d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - 32083
    return jd


def date_from_jd(jd: int) -> date:
    if jd > 2299160:
        a = jd + 32044
        b = (4 * a + 3) // 146097
        c = a - b * 146097 // 4
    else:
        b, c = 0, jd + 32082
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    return date(b * 100 + d - 4800 + m // 10, m + 3 - 12 * (m // 10),
                e - (153 * m + 2) // 5 + 1)


def _new_moon_jd(k: int) -> float:
    """Thời điểm sóc thứ k (k=0: sóc đầu 1900-01-01), dạng JD (UT)."""
    T = k / 1236.85
    T2, T3 = T * T, T * T * T
    dr = PI / 180
    jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    jd1 += 0.00033 * sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    C1 = (0.1734 - 0.000393 * T) * sin(M * dr) + 0.0021 * sin(2 * dr * M)
    C1 += -0.4068 * sin(Mpr * dr) + 0.0161 * sin(dr * 2 * Mpr) - 0.0004 * sin(dr * 3 * Mpr)
    C1 += 0.0104 * sin(dr * 2 * F) - 0.0051 * sin(dr * (M + Mpr))
    C1 += -0.0074 * sin(dr * (M - Mpr)) + 0.0004 * sin(dr * (2 * F + M))
    C1 += -0.0004 * sin(dr * (2 * F - M)) - 0.0006 * sin(dr * (2 * F + Mpr))
    C1 += 0.0010 * sin(dr * (2 * F - Mpr)) + 0.0005 * sin(dr * (2 * Mpr + M))
    if T < -11:
        dt = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        dt = -0.000278 + 0.000265 * T + 0.000262 * T2
    return jd1 + C1 - dt


def new_moon_day(k: int, tz: float = 7.0) -> int:
    """JDN (ngày địa phương) chứa sóc thứ k."""
    return floor(_new_moon_jd(k) + 0.5 + tz / 24)


def sun_sector(jdn: int, tz: float = 7.0) -> int:
    """Chỉ số cung 0..11 (mỗi cung 30°) của kinh độ Mặt Trời lúc 0h địa phương ngày jdn.
    Đổi cung giữa hai ngày liên tiếp = ngày đó chứa một trung khí."""
    T = (jdn - 2451545.5 - tz / 24) / 36525
    T2 = T * T
    dr = PI / 180
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * sin(dr * M)
    DL += (0.019993 - 0.000101 * T) * sin(dr * 2 * M) + 0.000290 * sin(dr * 3 * M)
    L = (L0 + DL) * dr
    L -= PI * 2 * floor(L / (PI * 2))
    return int(L / PI * 6)


@dataclass(frozen=True)
class LunarMonth:
    number: int          # 1..12
    leap: bool           # True nếu là tháng nhuận
    start_jd: int        # JDN ngày mùng một
    length: int          # 29 hoặc 30
    trung_khi: str | None  # trung khí chứa trong tháng (None nếu nhuận)

    @property
    def start(self) -> date:
        return date_from_jd(self.start_jd)

    def __str__(self) -> str:
        return f"{'Nhuận ' if self.leap else ''}tháng {self.number} ({self.start}, {self.length} ngày)"


def _k_of_jd(jd: int) -> int:
    return int((jd - 2415021.076998695) / 29.530588853)


def _month_11_start(year: int, tz: float) -> int:
    """JDN mùng một của tháng chứa Đông chí năm `year`."""
    off = jd_from_date(31, 12, year) - 2415021
    k = int(off / 29.530588853)
    nm = new_moon_day(k, tz)
    if sun_sector(nm, tz) >= 9:   # sóc rơi sau Đông chí -> lùi một tháng
        nm = new_moon_day(k - 1, tz)
    return nm


def _leap_offset(a11: int, tz: float) -> int:
    """Chỉ số (1..13) của tháng nhuận trong chu kỳ bắt đầu từ a11, tính từ tháng 11."""
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last, i = 0, 1
    arc = sun_sector(new_moon_day(k + i, tz), tz)
    while True:
        last = arc
        i += 1
        arc = sun_sector(new_moon_day(k + i, tz), tz)
        if arc != last and i < 14:
            continue
        break
    return i - 1


def lunar_months(year: int, tz: float = 7.0) -> list[LunarMonth]:
    """Các tháng âm lịch từ tháng 11 năm `year` đến hết chu kỳ Đông chí kế tiếp
    (12 hoặc 13 tháng; 13 tháng nghĩa là có tháng nhuận)."""
    a11 = _month_11_start(year, tz)
    b11 = _month_11_start(year + 1, tz)
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    n = round((b11 - a11) / 29.530588853)
    leap_idx = _leap_offset(a11, tz) if n == 13 else None
    out: list[LunarMonth] = []
    num, leap = 11, False
    for i in range(n):
        start = new_moon_day(k + i, tz)
        end = new_moon_day(k + i + 1, tz)
        if leap_idx is not None and i == leap_idx:
            num_i, is_leap = num_prev, True
        else:
            if i > 0:
                num = num % 12 + 1
            num_i, is_leap = num, False
        num_prev = num_i
        out.append(LunarMonth(num_i, is_leap, start, end - start, None))
    # gán trung khí: tháng không nhuận chứa đúng một trung khí
    res = []
    for m in out:
        end = m.start_jd + m.length
        # trung khí nằm trong [start, end) khi cung đổi giữa start-1 và end-1
        a, b = sun_sector(m.start_jd - 1, tz), sun_sector(end - 1, tz)
        tk = TRUNG_KHI[b] if a != b else None
        res.append(LunarMonth(m.number, m.leap, m.start_jd, m.length, tk))
    return res


def leap_month(year: int, tz: float = 7.0) -> int | None:
    """Trả về số của tháng nhuận (vd 6 = nhuận tháng 6) của năm âm lịch `year`, hoặc None.
    Năm âm lịch tính từ tháng Giêng; tháng nhuận 11/12 thuộc chu kỳ Đông chí năm trước nên
    được xét qua hai chu kỳ."""
    for y in (year - 1, year):
        for m in lunar_months(y, tz):
            if m.leap and _lunar_year_of(m, y) == year:
                return m.number
    return None


def _lunar_year_of(m: LunarMonth, cycle_year: int) -> int:
    # tháng 11, 12 thuộc năm cycle_year; tháng 1..10 thuộc cycle_year + 1
    return cycle_year if m.number >= 11 else cycle_year + 1
