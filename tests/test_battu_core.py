"""Kiểm thử quy tắc Can Chi tháng và giờ Bát Tự."""
import unittest
from datetime import datetime

from battu_tietkhi import get_battu_hour, get_battu_month
from battu_cli import can_chi_ngay, can_chi_nam


class CanChiTests(unittest.TestCase):
    def test_month_changes_at_solar_longitude_boundaries(self):
        self.assertEqual(get_battu_month(315.0, "Bính"), "Canh Dần")
        self.assertEqual(get_battu_month(345.0, "Bính"), "Tân Mão")
        self.assertEqual(get_battu_month(314.999, "Bính"), "Tân Sửu")

    def test_hour_branch_boundaries(self):
        self.assertTrue(get_battu_hour(datetime(2025, 1, 1, 22, 59), "Giáp").endswith("Hợi"))
        self.assertTrue(get_battu_hour(datetime(2025, 1, 1, 23, 0), "Giáp").endswith("Tý"))
        self.assertTrue(get_battu_hour(datetime(2025, 1, 2, 0, 59), "Giáp").endswith("Tý"))
        self.assertTrue(get_battu_hour(datetime(2025, 1, 2, 1, 0), "Giáp").endswith("Sửu"))

    def test_day_pillar_reference_date(self):
        self.assertEqual(can_chi_ngay(datetime(2000, 1, 1).date()), ("Mậu", "Ngọ"))

    def test_year_pillar_reference_years(self):
        self.assertEqual(can_chi_nam(2000), ("Canh", "Thìn"))
        self.assertEqual(can_chi_nam(1999), ("Kỷ", "Mão"))

    def test_invalid_stem_is_rejected(self):
        with self.assertRaises(ValueError):
            get_battu_month(316.0, "không phải can")


if __name__ == "__main__":
    unittest.main()
