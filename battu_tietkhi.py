import datetime

# ==================== CẤU HÌNH BÁT TỰ ====================
CHI_MONTHS = ["Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]
CHI_HOURS = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CANS = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

# Ngũ Dần Ca: Tra Thiên Can của tháng dựa vào Thiên Can của Năm
NGU_DAN_CA = {
    ("Giáp", "Kỷ"): ["Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh"],
    ("Ất", "Canh"): ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"],
    ("Bính", "Tân"): ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân"],
    ("Đinh", "Nhâm"): ["Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"],
    ("Mậu", "Quý"): ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất"]
}

# Ngũ Tý Ca: Tra Thiên Can của giờ Tý dựa vào Thiên Can của Ngày
NGU_TY_CA = {
    ("Giáp", "Kỷ"): "Giáp",
    ("Ất", "Canh"): "Bính",
    ("Bính", "Tân"): "Mậu",
    ("Đinh", "Nhâm"): "Canh",
    ("Mậu", "Quý"): "Nhâm"
}

# ==================== THUẬT TOÁN XỬ LÝ ====================

def get_battu_month(solar_longitude: float, year_can: str) -> str:
    """Xác định tháng Can Chi dựa vào Kinh độ mặt trời và Can Năm."""
    lon = solar_longitude % 360
    shifted_lon = (lon - 315) % 360
    month_idx = int(shifted_lon // 30)
    
    chi = CHI_MONTHS[month_idx]
    can = "Không xác định"
    for keys, cans in NGU_DAN_CA.items():
        if year_can in keys:
            can = cans[month_idx]
            break
    return f"{can} {chi}"

def get_battu_hour(dt: datetime.datetime, day_can: str) -> str:
    """Xác định giờ Can Chi dựa vào Giờ sinh (datetime) và Thiên Can của Ngày."""
    hour = dt.hour
    minute = dt.minute
    total_minutes = hour * 60 + minute

    shifted_minutes = (total_minutes + 60) % 1440
    hour_idx = int(shifted_minutes // 120)
    chi_hour = CHI_HOURS[hour_idx]

    start_can = "Giáp"
    for keys, start_can_name in NGU_TY_CA.items():
        if day_can in keys:
            start_can = start_can_name
            break

    start_can_idx = CANS.index(start_can)
    target_can_idx = (start_can_idx + hour_idx) % 10
    can_hour = CANS[target_can_idx]

    return f"{can_hour} {chi_hour}"
