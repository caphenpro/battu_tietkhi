# Thuật toán Bát Tự Tiết Khí

Thư viện Python hỗ trợ xác định Can Chi của **Tháng** (theo Kinh độ mặt trời / Tiết khí) và Can Chi của **Giờ** (theo định luật Ngũ Tý Ca).

## Cài đặt

```bash
pip install battu-tietkhi
```

Cập nhật lên bản mới nhất:

```bash
pip install -U battu-tietkhi
```

Nếu `pip` báo lỗi `externally-managed-environment` (Ubuntu, Debian mới), hãy dùng môi trường ảo:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# Windows PowerShell: .\.venv\Scripts\Activate.ps1

pip install battu-tietkhi
```

## Cách gọi sử dụng trong Code

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

## Kiểm tra sau khi cài đặt

```bash
python -c "from battu_tietkhi import get_battu_month, get_battu_hour; print(get_battu_month(316.0, 'Bính')); print(get_battu_hour(__import__('datetime').datetime(2026, 3, 5, 14, 30), 'Kỷ'))"
```

Nếu lệnh trên chạy mà không báo lỗi import, nghĩa là bạn đã cài đặt đúng.

## Cài từ mã nguồn (dành cho lập trình viên)

```bash
git clone https://github.com/caphenpro/battu_tietkhi.git
cd battu_tietkhi
pip install .
```

## Giấy phép

MIT License.
