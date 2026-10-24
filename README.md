# Thuật toán Bát Tự Tiết Khí

Thư viện Python hỗ trợ xác định Can Chi của **Tháng** (theo Kinh độ mặt trời / Tiết khí) và Can Chi của **Giờ** (theo định luật Ngũ Tý Ca).

## Cài đặt

### 1) Cài đặt trong môi trường ảo (khuyến nghị)

Đây là cách an toàn nhất và phù hợp với hầu hết người dùng.

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# hoặc trên Windows PowerShell:
# .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install git+https://github.com/caphenpro/battu_tietkhi.git
```

### 2) Cài đặt trực tiếp cho người dùng Linux có lỗi `externally-managed-environment`

Một số distro như Ubuntu, Debian mới có chính sách quản lý Python bởi hệ thống. Khi đó, `pip install` có thể báo lỗi `externally managed environment`.

```bash
python -m pip install --break-system-packages git+https://github.com/caphenpro/battu_tietkhi.git
```

Lưu ý:
- `--break-system-packages` chỉ nên dùng khi bạn đang cài đặt vào môi trường Python do hệ thống quản lý.
- Nếu có thể, hãy ưu tiên dùng `venv` thay vì cài trực tiếp vào hệ thống.

### 3) Cài đặt lại / làm mới cache (khi cần gỡ package cũ)

Nếu bạn từng cài bản cũ và muốn ép tải lại từ GitHub, dùng:

```bash
python -m pip install --no-cache-dir --force-reinstall git+https://github.com/caphenpro/battu_tietkhi.git
```

Nếu đang ở môi trường hệ thống quản lý, có thể thêm:

```bash
python -m pip install --break-system-packages --no-cache-dir --force-reinstall git+https://github.com/caphenpro/battu_tietkhi.git
```

### 4) Cài đặt từ nhánh cụ thể hoặc commit cụ thể (nâng cao)

Nếu bạn muốn cài từ một nhánh hoặc commit nhất định:

```bash
git clone https://github.com/caphenpro/battu_tietkhi.git
cd battu_tietkhi
python -m pip install .
```

Hoặc cài theo commit/nhánh:

```bash
python -m pip install "git+https://github.com/caphenpro/battu_tietkhi.git@main"
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

## Trường hợp nên dùng lệnh nào?

- Dùng `python -m venv .venv` nếu:
  - Bạn đang làm dự án Python cá nhân hoặc muốn tránh xung đột package.
  - Đây là lựa chọn khuyên dùng nhất.

- Dùng `--break-system-packages` nếu:
  - Bạn đang cài trên Ubuntu/Debian mới.
  - `pip` báo lỗi `externally managed environment`.
  - Bạn không muốn tạo môi trường ảo.

- Dùng `--no-cache-dir --force-reinstall` nếu:
  - Bạn muốn ép cài lại từ đầu và bỏ cache cũ.
  - Bạn đã cài bản cũ nhưng muốn cập nhật hoặc sửa lỗi do package cũ.

- Dùng `python -m pip install .` nếu:
  - Bạn đã clone repo về máy và muốn cài local package từ source code.
  - Bạn đang phát triển hoặc test code ở local.

## Kiểm tra sau khi cài đặt

```bash
python -c "from battu_tietkhi import get_battu_month, get_battu_hour; print(get_battu_month(316.0, 'Bính')); print(get_battu_hour(__import__('datetime').datetime(2026, 3, 5, 14, 30), 'Kỷ'))"
```

Nếu lệnh trên chạy mà không báo lỗi import, nghĩa là bạn đã cài đặt đúng.
