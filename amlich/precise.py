"""Tháng nhuận âm lịch dựa trên thiên văn chính xác đến giây (thư viện `astronomy-engine`).

Quy trình:
  1. Tính thời điểm sóc (trăng mới) và 12 trung khí bằng thiên văn học, theo UTC, độ chính xác ~giây.
  2. Đổi sang múi giờ địa phương (VN = UTC+7), chỉ lấy NGÀY địa phương để xếp tháng.
  3. Mỗi tháng âm lịch = [ngày chứa sóc này, ngày chứa sóc kế tiếp). Gắn các trung khí vào tháng.
  4. Tháng chứa Đông chí là tháng 11. Nếu từ Đông chí này tới Đông chí sau có 13 tháng,
     tháng đầu tiên không có trung khí là tháng nhuận.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

import astronomy as _ast

__all__ = ["PreciseMonth", "new_moons", "solar_term", "solar_terms",
           "lunar_months_precise", "leap_month_precise", "TIET_KHI"]

# (tên, kinh độ Mặt Trời). Trung khí = bội của 30°.
TIET_KHI = [
    ("Xuân phân", 0), ("Thanh minh", 15), ("Cốc vũ", 30), ("Lập hạ", 45),
    ("Tiểu mãn", 60), ("Mang chủng", 75), ("Hạ chí", 90), ("Tiểu thử", 105),
    ("Đại thử", 120), ("Lập thu", 135), ("Xử thử", 150), ("Bạch lộ", 165),
    ("Thu phân", 180), ("Hàn lộ", 195), ("Sương giáng", 210), ("Lập đông", 225),
    ("Tiểu tuyết", 240), ("Đại tuyết", 255), ("Đông chí", 270), ("Tiểu hàn", 285),
    ("Đại hàn", 300), ("Lập xuân", 315), ("Vũ thủy", 330), ("Kinh trập", 345),
]


def _to_dt(t) -> datetime:
    return t.Utc().replace(tzinfo=timezone.utc)


def _from_dt(dt: datetime):
    dt = dt.astimezone(timezone.utc)
    return _ast.Time.Make(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                          dt.second + dt.microsecond / 1e6)


def new_moons(start: datetime, end: datetime) -> list[datetime]:
    """Các thời điểm sóc (UTC, aware) trong [start, end]."""
    out, t = [], _from_dt(start)
    limit = _from_dt(end)
    while True:
        nm = _ast.SearchMoonPhase(0, t, 40)
        if nm is None or nm.ut > limit.ut:
            return out
        out.append(_to_dt(nm))
        t = nm.AddDays(1)


def solar_term(year: int, longitude: float) -> datetime:
    """Thời điểm (UTC) Mặt Trời đạt `longitude` độ lần đầu tiên từ 1/1/year."""
    # Ước lượng từ Xuân phân (~20/3, kinh độ 0°). Chuẩn hóa góc về
    # [-180°, 180°) để tránh đẩy các kinh độ 315°–345° sang sai thời điểm.
    # Sau đó đưa ước lượng về đúng năm dương lịch được yêu cầu. Ví dụ:
    # 315° (Lập Xuân) phải rơi vào đầu tháng 2, còn 270° (Đông chí)
    # phải rơi vào cuối tháng 12 của chính năm đó.
    lon = float(longitude) % 360.0
    delta_lon = (lon + 180.0) % 360.0 - 180.0
    est = datetime(year, 3, 20, tzinfo=timezone.utc) + timedelta(
        days=delta_lon / 360.0 * 365.2422
    )
    year_start = datetime(year, 1, 1, tzinfo=timezone.utc)
    year_end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    if est < year_start:
        est += timedelta(days=365.2422)
    elif est >= year_end:
        est -= timedelta(days=365.2422)

    t = _ast.SearchSunLongitude(lon, _from_dt(est - timedelta(days=20)), 40)
    if t is None:
        raise RuntimeError(f"không tìm được kinh độ {longitude} năm {year}")
    return _to_dt(t)


def solar_terms(year: int, tz: float = 7.0) -> list[tuple[str, datetime]]:
    """24 tiết khí của năm dương lịch `year`, theo giờ địa phương (aware), sắp theo thời gian."""
    zone = timezone(timedelta(hours=tz))
    res = [(n, solar_term(year, lon).astimezone(zone)) for n, lon in TIET_KHI]
    return sorted(res, key=lambda x: x[1])


@dataclass(frozen=True)
class PreciseMonth:
    number: int
    leap: bool
    new_moon: datetime              # thời điểm sóc, giờ địa phương (aware), chính xác đến giây
    start: date                     # ngày mùng một
    end: date                       # ngày mùng một tháng sau (không thuộc tháng này)
    trung_khi: list[tuple[str, datetime]] = field(default_factory=list)

    @property
    def length(self) -> int:
        return (self.end - self.start).days

    def __str__(self) -> str:
        tk = ", ".join(n for n, _ in self.trung_khi) or "—"
        return (f"{'Nhuận ' if self.leap else ''}tháng {self.number}: {self.start} "
                f"({self.length} ngày), sóc {self.new_moon:%Y-%m-%d %H:%M:%S}, trung khí: {tk}")


def lunar_months_precise(year: int, tz: float = 7.0) -> list[PreciseMonth]:
    """Các tháng từ tháng 11 (chứa Đông chí năm `year`) đến hết tháng 10 (hoặc nhuận 10)
    trước Đông chí năm sau."""
    zone = timezone(timedelta(hours=tz))
    ld = lambda dt: dt.astimezone(zone).date()   # noqa: E731

    dc0 = solar_term(year, 270)
    dc1 = solar_term(year + 1, 270)
    socs = new_moons(dc0 - timedelta(days=35), dc1 + timedelta(days=35))

    i0 = max(i for i, s in enumerate(socs) if ld(s) <= ld(dc0))
    i1 = max(i for i, s in enumerate(socs) if ld(s) <= ld(dc1))
    n = i1 - i0
    assert n in (12, 13), f"số tháng bất thường: {n}"

    # tất cả trung khí trong khoảng, theo giờ địa phương
    tks = []
    for y in (year, year + 1):
        for name, lon in TIET_KHI:
            if lon % 30 == 0:
                tks.append((name, solar_term(y, lon).astimezone(zone)))
    tks.sort(key=lambda x: x[1])

    raw = []
    for i in range(i0, i1):
        start, end = ld(socs[i]), ld(socs[i + 1])
        inside = [(nm, t) for nm, t in tks if start <= t.date() < end]
        raw.append((socs[i].astimezone(zone), start, end, inside))

    leap_idx = None
    if n == 13:
        leap_idx = next(i for i, r in enumerate(raw) if i > 0 and not r[3])

    # Đánh số tuần tự: tháng chứa Đông chí = 11, tháng nhuận lấy lại số tháng trước.
    # (Không đặt tên theo trung khí, vì có năm một tháng chứa 2 trung khí, vd. 2033.)
    months, num = [], 11
    for i, (nm, start, end, inside) in enumerate(raw):
        if i == leap_idx:
            months.append(PreciseMonth(num, True, nm, start, end, inside))
        else:
            if i > 0:
                num = num % 12 + 1
            months.append(PreciseMonth(num, False, nm, start, end, inside))
    return months


def leap_month_precise(year: int, tz: float = 7.0) -> int | None:
    """Số tháng nhuận của năm âm lịch `year` (None nếu không nhuận)."""
    for cy in (year - 1, year):
        for m in lunar_months_precise(cy, tz):
            if m.leap and (cy if m.number >= 11 else cy + 1) == year:
                return m.number
    return None
