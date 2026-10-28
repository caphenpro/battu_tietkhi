# Quy trình phát hành battu-tietkhi

Quy trình phát hành chính thức chạy từ GitHub Actions và sử dụng PyPI Trusted Publishing (OIDC), không lưu PyPI API token trong mã nguồn.

## Checklist phát hành

1. Hoàn tất thay đổi mã nguồn và bổ sung kiểm thử hồi quy.
2. Cập nhật phiên bản trong `setup.py` và ghi chú trong `CHANGELOG.md`.
3. Đẩy thay đổi lên nhánh `main`; chờ workflow **Test** xanh trên Python 3.9–3.13 và bước build package thành công.
4. Mở **Releases → Draft a new release** trên GitHub.
5. Tạo tag mới theo dạng `vX.Y.Z` (ví dụ `v1.2.3`) từ `main`, điền ghi chú phát hành rồi chọn **Publish release**.
6. Workflow **Publish to PyPI** sẽ chạy lại toàn bộ kiểm thử, xác nhận tag khớp phiên bản trong `setup.py`, build wheel/sdist, chạy `twine check`, rồi mới gửi gói lên PyPI.
7. Xác minh trang PyPI và cài bản phát hành trong môi trường sạch.

## Quy tắc phiên bản

- **PATCH** (`1.2.3`): sửa lỗi tương thích hoặc lỗi tính toán mà không đổi API.
- **MINOR** (`1.3.0`): bổ sung tính năng tương thích ngược.
- **MAJOR** (`2.0.0`): thay đổi API hoặc hành vi không tương thích ngược.

Không tái sử dụng phiên bản đã phát hành lên PyPI. Nếu kiểm thử hoặc xác minh build thất bại, không xuất bản release; sửa lỗi, tăng phiên bản phù hợp rồi chạy lại.
