CHI_MONTHS = ["Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]

CAN_TABLE = {
    ("Giáp", "Kỷ"): ["Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh"],
    ("Ất", "Canh"): ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"],
    ("Bính", "Tân"): ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân"],
    ("Đinh", "Nhâm"): ["Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"],
    ("Mậu", "Quý"): ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất"]
}

def get_battu_month(solar_longitude: float, year_can: str) -> str:
    """
    Xác định tháng Can Chi Tứ Trụ dựa vào Kinh độ mặt trời (0 - 360 độ).
    - Lập Xuân (Tháng Dần) bắt đầu từ 315 độ.
    """
    # Chuẩn hóa góc mặt trời về khoảng [0, 360)
    lon = solar_longitude % 360
    
    # Tịnh tiến mốc Lập Xuân (315 độ) về gốc 0
    shifted_lon = (lon - 315) % 360
    
    # Mỗi tháng Tiết Khí chiếm đúng 30 độ
    month_idx = int(shifted_lon // 30)
    
    chi = CHI_MONTHS[month_idx]
    
    can = "Không xác định"
    for keys, cans in CAN_TABLE.items():
        if year_can in keys:
            can = cans[month_idx]
            break
            
    return f"{can} {chi}"

