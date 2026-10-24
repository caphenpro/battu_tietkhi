# Thuật toán Bát Tự Tiết Khí

Thư viện Python hỗ trợ xác định Can Chi của **Tháng** (theo Kinh độ mặt trời / Tiết khí) và Can Chi của **Giờ** (theo định luật Ngũ Tý Ca).

## Cách cài đặt trực tiếp
```bash
pip install git+ttps://github.com/caphenpro/battu_tietkhi/
```

## Cách gọi sử dụng trong Code
```python
from battu_tietkhi import get_battu_month, get_battu_hour

# Tính tháng Bát Tự từ Kinh độ mặt trời (Ví dụ: 316 độ, năm Bính)
thang = get_battu_month(316.0, "Bính")

# Tính giờ Bát Tự từ thời gian và Can Ngày (Ví dụ: 14h30, ngày Kỷ)
import datetime
gio = get_battu_hour(datetime.datetime(2026, 3, 5, 14, 30), "Kỷ")
```
