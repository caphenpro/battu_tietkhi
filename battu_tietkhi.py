import datetime

# ==================== CẤU HÌNH BÁT TỰ ====================
CHI_MONTHS = ["Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]
CHI_HOURS = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CANS = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

# Ngũ Dần Ca: Thiên Can của tháng theo Can Năm
# Mỗi can năm có một chuỗi 12 tháng tương ứng
NGU_DAN_CA = {
    "Giáp": ["Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh"],
    "Ất": ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"],
    "Bính": ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân"],
    "Đinh": ["Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"],
    "Mậu": ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất"],
    "Kỷ": ["Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh"],
    "Canh": ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"],
    "Tân": ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân"],
    "Nhâm": ["Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"],
    "Quý": ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất"],
}

# Ngũ Tý Ca: Thiên Can của giờ Tý dựa vào Thiên Can của ngày
NGU_TY_CA = {
    "Giáp": "Giáp",
    "Ất": "Bính",
    "Bính": "Mậu",
    "Đinh": "Canh",
    "Mậu": "Nhâm",
    "Kỷ": "Giáp",
    "Canh": "Bính",
    "Tân": "Mậu",
    "Nhâm": "Canh",
    "Quý": "Nhâm",
}

# ==================== THUẬT TOÁN XỬ LÝ ====================

def _normalize_can(can: str) -> str:
    """Chuẩn hóa tên Can về dạng chuẩn để tránh lỗi nhập liệu."""
    if can is None:
        raise ValueError("Thiên Can không được rỗng")

    normalized = str(can).strip()
    aliases = {
        "giáp": "Giáp",
        "giap": "Giáp",
        "ất": "Ất",
        "at": "Ất",
        "bính": "Bính",
        "binh": "Bính",
        "đinh": "Đinh",
        "dinh": "Đinh",
        "mậu": "Mậu",
        "mau": "Mậu",
        "kỷ": "Kỷ",
        "ky": "Kỷ",
        "canh": "Canh",
        "tân": "Tân",
        "tan": "Tân",
        "nhâm": "Nhâm",
        "nham": "Nhâm",
        "quý": "Quý",
        "quy": "Quý",
        "qui": "Quý",
    }

    normalized = aliases.get(normalized.lower(), normalized)
    if normalized not in CANS:
        raise ValueError(f"Thiên Can không hợp lệ: {can!r}. Các giá trị hợp lệ: {CANS}")
    return normalized


def get_battu_month(solar_longitude: float, year_can: str) -> str:
    """Xác định tháng Can Chi dựa vào Kinh độ mặt trời và Can Năm."""
    if solar_longitude is None:
        raise ValueError("Kinh độ mặt trời không được rỗng")

    lon = float(solar_longitude) % 360.0
    shifted_lon = (lon - 315.0) % 360.0
    month_idx = int(shifted_lon // 30) % 12
    chi = CHI_MONTHS[month_idx]
    can = NGU_DAN_CA[_normalize_can(year_can)][month_idx]
    return f"{can} {chi}"


def get_battu_hour(dt: datetime.datetime, day_can: str) -> str:
    """Xác định giờ Can Chi dựa vào Giờ sinh (datetime) và Thiên Can của Ngày."""
    if not isinstance(dt, datetime.datetime):
        raise TypeError("dt phải là đối tượng datetime.datetime")

    hour = dt.hour
    minute = dt.minute
    total_minutes = hour * 60 + minute

    shifted_minutes = total_minutes % 1440
    hour_idx = int(((total_minutes + 60) % 1440) // 120) % 12
    chi_hour = CHI_HOURS[hour_idx]

    start_can = NGU_TY_CA[_normalize_can(day_can)]
    start_can_idx = CANS.index(start_can)
    target_can_idx = (start_can_idx + hour_idx) % len(CANS)
    can_hour = CANS[target_can_idx]

    return f"{can_hour} {chi_hour}"


__all__ = ["get_battu_month", "get_battu_hour"]
