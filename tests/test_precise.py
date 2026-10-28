"""Kiểm thử hồi quy cho thuật toán tính thời điểm tiết khí.

Chạy từ thư mục gốc:
    python -m unittest discover -s tests -v
"""
import unittest

from amlich.precise import solar_term, solar_terms


class SolarTermRegressionTests(unittest.TestCase):
    def test_lap_xuan_is_in_early_february(self):
        # Lập Xuân 2025: khoảng 03/02 theo UTC+7.
        self.assertEqual(solar_term(2025, 315).date().isoformat(), "2025-02-03")

    def test_dong_chi_is_in_december_of_requested_year(self):
        # Đông Chí 2025 phải nằm cuối năm 2025, không phải cuối năm trước.
        self.assertEqual(solar_term(2025, 270).date().isoformat(), "2025-12-21")

    def test_january_term_is_in_requested_year(self):
        # Tiểu Hàn 2025 theo UTC thường rơi vào ngày 5 tháng 1.
        self.assertEqual(solar_term(2025, 285).date().isoformat(), "2025-01-05")

    def test_all_24_terms_are_sorted_and_in_local_calendar_year(self):
        terms = solar_terms(2025, tz=7)
        self.assertEqual(len(terms), 24)
        times = [dt for _, dt in terms]
        self.assertEqual(times, sorted(times))
        self.assertTrue(all(dt.year == 2025 for dt in times))


if __name__ == "__main__":
    unittest.main()
