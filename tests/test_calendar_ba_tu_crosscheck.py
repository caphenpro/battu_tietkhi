"""Đối chiếu độc lập giữa lịch âm nhanh, lịch âm thiên văn và Bát Tự.

Chạy bằng:
    python -m unittest discover -s tests -v

Các kiểm thử này không thay thế đối chiếu với lịch pháp/thiên văn bên ngoài;
chúng phát hiện sai lệch nội bộ và bảo vệ các mốc tham chiếu đã công bố.
"""
import unittest
from datetime import datetime, timedelta, timezone

from amlich.core import lunar_months
from amlich.precise import (
    leap_month_precise,
    lunar_months_precise,
    solar_term,
)
from battu_cli import am_lich, lap_tu_tru
from battu_tietkhi import get_battu_hour, get_battu_month


class StemNormalizationRegressionTests(unittest.TestCase):
    def test_lowercase_accented_giap_is_accepted(self):
        self.assertEqual(get_battu_month(315.0, "giáp"), "Bính Dần")
        self.assertEqual(
            get_battu_hour(datetime(2025, 1, 1, 23, 0), "giáp"),
            "Giáp Tý",
        )

    def test_all_stems_accept_lowercase_forms(self):
        stems = [
            ("giáp", "Giáp"), ("ất", "Ất"), ("bính", "Bính"),
            ("đinh", "Đinh"), ("mậu", "Mậu"), ("kỷ", "Kỷ"),
            ("canh", "Canh"), ("tân", "Tân"), ("nhâm", "Nhâm"),
            ("quý", "Quý"),
        ]
        for lower, canonical in stems:
            with self.subTest(stem=lower):
                self.assertEqual(
                    get_battu_month(315.0, lower),
                    get_battu_month(315.0, canonical),
                )


class LunarCalendarCrossCheckTests(unittest.TestCase):
    def test_fast_and_precise_month_boundaries_agree(self):
        """Đối chiếu ngày đầu tháng, số tháng, tháng nhuận và độ dài tháng."""
        for year in (2023, 2024, 2025, 2033):
            fast = lunar_months(year, tz=7)
            precise = lunar_months_precise(year, tz=7)
            fast_rows = [
                (m.start, m.number, m.leap, m.length) for m in fast
            ]
            precise_rows = [
                (m.start, m.number, m.leap, m.length) for m in precise
            ]
            with self.subTest(year=year):
                self.assertEqual(
                    fast_rows,
                    precise_rows,
                    msg=f"Lịch nhanh và lịch thiên văn lệch nhau trong chu kỳ {year}",
                )

    def test_known_lunar_new_year_dates(self):
        # Các ngày mùng một Tết đã biết theo giờ Việt Nam.
        expected = {
            datetime(2023, 1, 22).date(),
            datetime(2024, 2, 10).date(),
            datetime(2025, 1, 29).date(),
        }
        for year, tet in ((2023, datetime(2023, 1, 22).date()),
                          (2024, datetime(2024, 2, 10).date()),
                          (2025, datetime(2025, 1, 29).date())):
            months = lunar_months_precise(year - 1, tz=7)
            month_one_starts = [
                m.start for m in months if m.number == 1 and not m.leap
            ]
            with self.subTest(year=year):
                self.assertIn(tet, month_one_starts)
        self.assertEqual(len(expected), 3)

    def test_known_leap_month_results_match(self):
        for year, expected in ((2024, None), (2025, 6), (2033, 11)):
            with self.subTest(year=year):
                self.assertEqual(leap_month_precise(year, tz=7), expected)


class BaTuCrossCheckTests(unittest.TestCase):
    def test_published_reference_chart_and_lunar_date(self):
        # Ví dụ tham chiếu trong README: 01/01/2000 12:00, giờ Việt Nam.
        dt = datetime(2000, 1, 1, 12, 0)
        result = lap_tu_tru(dt, tz=7)
        self.assertEqual(result["tru_nam"], "Kỷ Mão")
        self.assertEqual(result["tru_thang"], "Bính Tý")
        self.assertEqual(result["tru_ngay"], "Mậu Ngọ")
        self.assertEqual(result["tru_gio"], "Mậu Ngọ")
        self.assertEqual(am_lich(dt.date(), tz=7), (25, 11, False, 1999))

    def test_ba_tu_year_and_month_change_across_lap_xuan(self):
        # Dùng thời điểm tiết khí thiên văn làm mốc; kiểm tra hai phía cách 10 phút.
        term_utc = solar_term(2025, 315)
        term_local = term_utc.astimezone(timezone(timedelta(hours=7)))
        before = lap_tu_tru(
            (term_local - timedelta(minutes=10)).replace(tzinfo=None), tz=7
        )
        after = lap_tu_tru(
            (term_local + timedelta(minutes=10)).replace(tzinfo=None), tz=7
        )

        self.assertEqual(before["tru_nam"], "Giáp Thìn")
        self.assertEqual(before["tru_thang"], "Đinh Sửu")
        self.assertEqual(after["tru_nam"], "Ất Tị")
        self.assertEqual(after["tru_thang"], "Mậu Dần")

    def test_hour_branch_boundaries(self):
        cases = (
            (datetime(2025, 1, 1, 22, 59), "Hợi"),
            (datetime(2025, 1, 1, 23, 0), "Tý"),
            (datetime(2025, 1, 2, 0, 59), "Tý"),
            (datetime(2025, 1, 2, 1, 0), "Sửu"),
        )
        for dt, branch in cases:
            with self.subTest(dt=dt):
                self.assertTrue(
                    get_battu_hour(dt, "Giáp").endswith(branch)
                )


if __name__ == "__main__":
    unittest.main()
