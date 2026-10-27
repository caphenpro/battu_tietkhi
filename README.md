# Thuật toán Bát Tự Tiết Khí

Thư viện Python hỗ trợ:

- Xác định Can Chi của **Tháng** (theo Kinh độ mặt trời / Tiết khí) và Can Chi của **Giờ** (theo định luật Ngũ Tý Ca).
- Xác định **tháng nhuận âm lịch** theo sóc (trăng mới) và trung khí, có bộ thiên văn chính xác đến giây (gói `amlich`).
- Lập **Tứ Trụ** và đổi âm lịch từ ngày giờ sinh dương lịch (chương trình `battu_cli`).

## Cài đặt

```bash
pip install battu-tietkhi
```

Cài thêm bộ thiên văn chính xác (cần cho tháng nhuận chính xác theo giây, tiết khí, và `battu_cli`):

```bash
pip install "battu-tietkhi[precise]"
```

Cập nhật lên bản mới nhất:

```bash
pip install -U "battu-tietkhi[precise]"
```

Nếu `pip` báo lỗi `externally-managed-environment` (Ubuntu, Debian mới), hãy dùng môi trường ảo:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# Windows PowerShell: .\.venv\Scripts\Activate.ps1

pip install "battu-tietkhi[precise]"
```

## Cách gọi sử dụng trong Code

### 1. Tháng và giờ Bát Tự

```python
from battu_tietkhi import get_battu_month, get_battu_hour

# Tính tháng Bát Tự từ Kinh độ mặt trời (Ví dụ: 316 độ, năm Bính)
thang = get_battu_month(316.0, "Bính")
print(thang)  # Ví dụ: "Canh Dần"

# Tính giờ Bát Tự từ thời gian và Can Ngày (Ví dụ: 14h30, ngày Kỷ)
import datetime
gio = get_battu_hour(datetime.datetime(2026, 3, 5, 14, 30), "Kỷ")
print(gio)
```

### 2. Tháng nhuận âm lịch

Quy tắc trung khí: tháng chứa Đông chí là tháng 11. Nếu từ Đông chí này đến Đông chí sau có 13 tháng,
**tháng đầu tiên không chứa trung khí** là tháng nhuận.

Bộ nhanh (không cần thư viện ngoài, công thức Meeus):

```python
from amlich import leap_month, lunar_months

leap_month(2025)         # 6     -> năm 2025 nhuận tháng 6
leap_month(2024)         # None  -> không nhuận
leap_month(2025, tz=8)   # múi giờ Trung Quốc (UTC+8); mặc định tz=7 là Việt Nam
```

Bộ chính xác theo giây (cần `astronomy-engine`):

```python
from amlich import leap_month_precise, lunar_months_precise, solar_terms, new_moons

leap_month_precise(2025)   # 6
leap_month_precise(2033)   # 11  (năm đặc biệt: một tháng chứa 2 trung khí)

for m in lunar_months_precise(2024):   # chu kỳ Đông chí 2024 -> Đông chí 2025
    print(m)
# ...
# Nhuận tháng 6: 2025-07-25 (29 ngày), sóc 2025-07-25 02:11:43, trung khí: —
```

Mỗi phần tử là `PreciseMonth` gồm: `number` (số tháng), `leap` (True nếu nhuận), `new_moon` (thời điểm sóc, giờ địa phương),
`start`/`end` (ngày mùng một và ngày mùng một tháng sau), `length` (29 hoặc 30), `trung_khi` (các trung khí nằm trong tháng).

Tiết khí và sóc chính xác đến giây:

```python
for ten, gio in solar_terms(2025)[:3]:   # 24 tiết khí năm 2025, giờ VN
    print(ten, gio)
# Tiểu hàn 2025-01-05 09:32:41+07:00
# Đại hàn 2025-01-20 03:00:02+07:00
# Lập xuân 2025-02-03 21:10:29+07:00
```

Các hàm của `amlich`:

| Hàm | Công dụng |
|---|---|
| `leap_month(năm, tz=7)` | Số tháng nhuận của năm âm lịch, hoặc `None` (bộ nhanh) |
| `lunar_months(năm, tz=7)` | Các tháng của chu kỳ Đông chí (bộ nhanh) |
| `leap_month_precise(năm, tz=7)` | Như `leap_month`, dùng thiên văn chính xác |
| `lunar_months_precise(năm, tz=7)` | Các tháng, kèm thời điểm sóc và trung khí chính xác |
| `solar_terms(năm, tz=7)` | 24 tiết khí của năm dương lịch, theo giờ địa phương |
| `solar_term(năm, kinh_độ)` | Thời điểm (UTC) Mặt Trời đạt một kinh độ |
| `new_moons(bắt_đầu, kết_thúc)` | Danh sách thời điểm sóc trong một khoảng |

Lưu ý: chỉ so sánh theo **ngày** địa phương khi xếp tháng. Việt Nam dùng UTC+7, Trung Quốc UTC+8 nên đôi khi
ngày mùng một hoặc tháng nhuận khác nhau giữa hai lịch.

### 3. Lập Tứ Trụ từ ngày giờ sinh

Chương trình `battu_cli` dùng `get_battu_month`, `get_battu_hour` cùng kinh độ Mặt Trời chính xác tại đúng giờ sinh:

```bash
python -m battu_cli 2000-01-01 12:00
```

```
Âm lịch    : 25/11 năm Kỷ Mão (1999)
Kinh độ MT : 280.0713°
Tiết       : Đại tuyết 07/12 20:48:01  ->  Tiểu hàn 06/01 08:00:55

      Giờ          Ngày         Tháng         Năm
  Mậu Ngọ      Mậu Ngọ      Bính Tý      Kỷ Mão
```

Tùy chọn: `--tz 8` (đổi múi giờ), `--ty-som` (từ 23h tính sang ngày hôm sau). Chạy không tham số thì chương trình hỏi từng bước.
Năm Bát Tự đổi tại Lập Xuân (kinh độ 315°), không đổi tại 1/1 hay Tết.

## Kiểm tra sau khi cài đặt

```bash
python -c "from battu_tietkhi import get_battu_month, get_battu_hour; print(get_battu_month(316.0, 'Bính')); print(get_battu_hour(__import__('datetime').datetime(2026, 3, 5, 14, 30), 'Kỷ'))"
```

Kiểm tra phần tháng nhuận (kết quả đúng là `6`):

```bash
python -c "from amlich import leap_month; print(leap_month(2025))"
```

Nếu các lệnh trên chạy mà không báo lỗi, nghĩa là bạn đã cài đặt đúng.

## Cài từ mã nguồn (dành cho lập trình viên)

```bash
git clone https://github.com/caphenpro/battu_tietkhi.git
cd battu_tietkhi
pip install ".[precise]"
```

## Giấy phép

MIT License.
