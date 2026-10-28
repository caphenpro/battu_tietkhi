"""
Lịch Âm Dương – Bát Tự
- Flask web app
- battu-tietkhi: tháng/giờ Bát Tự
- amlich: lịch âm và tiết khí
- Skyfield + JPL DE421: kinh độ biểu kiến của Mặt Trời

Lưu ý:
* Đây là bản khởi đầu có thể chạy và mở rộng; cần đối chiếu bộ test trước khi dùng
  cho nghiên cứu hoặc lập lá số quan trọng.
* lunardate hỗ trợ phạm vi lịch giới hạn (thường 1900–2099).
* Skyfield tải tệp DE421 lần đầu khi chạy; cần kết nối Internet lần đầu.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, request, render_template_string

from lunardate import LunarDate
from skyfield.api import load
from battu_tietkhi import get_battu_month, get_battu_hour

app = Flask(__name__)
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu",
       "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ",
       "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Nạp JPL DE421. Skyfield sẽ tải tệp nếu chưa có trong cache.
ts = load.timescale()
eph = load("de421.bsp")
earth = eph["Earth"]
sun = eph["Sun"]


def solar_longitude_deg(dt_local: datetime) -> float:
    """Kinh độ hoàng đạo biểu kiến địa tâm của Mặt Trời, độ 0..360."""
    if dt_local.tzinfo is None:
        dt_local = dt_local.replace(tzinfo=VN_TZ)
    dt_utc = dt_local.astimezone(ZoneInfo("UTC"))
    t = ts.from_datetime(dt_utc)
    apparent = earth.at(t).observe(sun).apparent()
    # Use the true ecliptic and equinox of date. Skyfield defaults to J2000
    # when epoch is omitted, which introduces a precession-related offset.
    _, longitude, _ = apparent.ecliptic_latlon(epoch="date")
    return longitude.degrees % 360.0


def julian_day_number(date_obj) -> int:
    """Số ngày Julius nguyên cho ngày dân dụng Gregorian."""
    a = (14 - date_obj.month) // 12
    y = date_obj.year + 4800 - a
    m = date_obj.month + 12 * a - 3
    return (date_obj.day + (153 * m + 2) // 5 + 365 * y
            + y // 4 - y // 100 + y // 400 - 32045)


def day_pillar(date_obj):
    """
    Tính Can Chi ngày theo chu kỳ 60 ngày.
    Mốc dùng để kiểm thử: 07/01/2000 là ngày Giáp Tý.
    """
    idx = (julian_day_number(date_obj) + 49) % 60
    return CAN[idx % 10], CHI[idx % 12]


def year_pillar(dt_local: datetime, longitude: float):
    """Năm Bát Tự đổi tại Lập Xuân (kinh độ Mặt Trời 315°)."""
    year = dt_local.year
    # Trước Lập Xuân trong tháng 1/đầu tháng 2 vẫn thuộc năm Bát Tự trước.
    if dt_local.month <= 2 and longitude < 315.0:
        year -= 1
    idx = (year - 1984) % 60  # 1984 là năm Giáp Tý
    return CAN[idx % 10], CHI[idx % 12], year


def format_pillar(pair):
    return f"{pair[0]} {pair[1]}"


def calculate(dt_local: datetime):
    longitude = solar_longitude_deg(dt_local)
    lunar = LunarDate.fromSolarDate(
        dt_local.year, dt_local.month, dt_local.day
    )

    can_nam, chi_nam, bazi_year = year_pillar(dt_local, longitude)
    can_ngay, chi_ngay = day_pillar(dt_local.date())

    # API battu-tietkhi nhận tên Thiên Can bằng tiếng Việt có dấu.
    thang = get_battu_month(longitude, can_nam)
    gio = get_battu_hour(dt_local.replace(tzinfo=None), can_ngay)

    return {
        "duong": dt_local.strftime("%d/%m/%Y %H:%M"),
        "am": (
            f"{lunar.day:02d}/{lunar.month:02d}/"
            f"{lunar.year} {'(nhuận)' if lunar.isLeapMonth else ''}"
        ).strip(),
        "thu": dt_local.strftime("%A"),
        "kinh_do": f"{longitude:.6f}°",
        "nam": format_pillar((can_nam, chi_nam)),
        "thang": str(thang),
        "ngay": format_pillar((can_ngay, chi_ngay)),
        "gio": str(gio),
        "nam_bazi": str(bazi_year),
    }


HTML = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lịch Âm Dương – Bát Tự</title>
<style>
body{font-family:system-ui,sans-serif;max-width:760px;margin:24px auto;padding:0 14px;
background:#f5f1e8;color:#252525}
.card{background:white;border-radius:14px;padding:20px;margin:14px 0;
box-shadow:0 2px 12px #0001}
h1{font-size:1.55rem}label{display:block;margin:12px 0 5px}
input,button{font:inherit;padding:10px;border:1px solid #bbb;border-radius:8px}
button{background:#263c32;color:white;border:0;margin-top:16px;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.pillar{padding:12px;background:#f3f0e8;border-radius:10px}
.value{font-size:1.15rem;font-weight:700;margin-top:6px}
small{color:#555}.error{color:#a00}
@media(max-width:480px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<h1>🗓️ Lịch Âm Dương – Bát Tự</h1>
<div class="card">
<form method="post">
<label for="birth">Ngày giờ dương lịch (giờ Việt Nam)</label>
<input id="birth" name="birth" type="datetime-local" required value="{{ value }}">
<br><button type="submit">Tính lịch và Tứ trụ</button>
</form>
</div>
{% if error %}<div class="card error">{{ error }}</div>{% endif %}
{% if result %}
<div class="card">
<h2>Lịch ngày</h2>
<p><b>Dương lịch:</b> {{ result.duong }}</p>
<p><b>Âm lịch:</b> {{ result.am }}</p>
<p><b>Kinh độ Mặt Trời:</b> {{ result.kinh_do }}</p>
<small>Thời gian nhập được hiểu là giờ Việt Nam (UTC+7).</small>
</div>
<div class="card">
<h2>Tứ trụ Bát Tự</h2>
<div class="grid">
<div class="pillar">Trụ năm<div class="value">{{ result.nam }}</div></div>
<div class="pillar">Trụ tháng<div class="value">{{ result.thang }}</div></div>
<div class="pillar">Trụ ngày<div class="value">{{ result.ngay }}</div></div>
<div class="pillar">Trụ giờ<div class="value">{{ result.gio }}</div></div>
</div>
<p><small>Năm Bát Tự được xét theo Lập Xuân; tháng dựa trên kinh độ Mặt Trời.
Cần kiểm thử độc lập các quy ước đổi ngày lúc 23:00 và giờ chân thái dương
trước khi dùng làm công cụ lập lá số chính thức.</small></p>
</div>
{% endif %}
<div class="card">
<b>Nền tảng tính toán</b>
<p><small>battu-tietkhi · lunardate · Skyfield · JPL DE421</small></p>
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    now = datetime.now(VN_TZ).replace(second=0, microsecond=0)
    value = now.strftime("%Y-%m-%dT%H:%M")
    result = None
    error = None

    if request.method == "POST":
        value = request.form.get("birth", "").strip()
        try:
            dt = datetime.strptime(value, "%Y-%m-%dT%H:%M").replace(tzinfo=VN_TZ)
            if not 1900 <= dt.year <= 2099:
                raise ValueError("Bản hiện tại giới hạn năm 1900–2099 do phạm vi lunardate.")
            result = calculate(dt)
        except Exception as exc:
            error = f"Không tính được dữ liệu: {exc}"

    return render_template_string(
        HTML, value=value, result=result, error=error
    )


if __name__ == "__main__":
    # Mở trình duyệt tại http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=False)
