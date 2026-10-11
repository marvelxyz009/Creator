# Trạng thái hiện hành — 0.4

Đã chuyển hoàn toàn sang chat: xóa giao diện/server/worker và adapter provider. Giữ canon, dependency invalidation, revision-safe packets, nhập PNG, review ảnh và xuất Markdown/CBZ.

Thêm ChatWorkflow: lưu ba vòng lựa chọn có revision, hồ sơ tự suy ra, resume và progress.md/progress.json. CLI chỉ làm thao tác file, không gọi model. Entry skill creator-studio hướng dẫn hỏi trong chat và dùng công cụ ảnh của phiên hiện tại. Dữ liệu stories/ local; .studio/ cũ giữ nguyên.

Cần công cụ ảnh của phiên để vẽ thực tế; việc triển khai này không tạo sẵn truyện hoặc ảnh demo. Tiếp tục một truyện luôn đọc resume trước. Không có hoạt động nền sau khi chat dừng.

Lựa chọn linh hoạt 2–4, mặc định 3. Skill production bổ sung reference pack đã xem, anchor page, visual continuity ledger, đối chiếu từng trang và sửa cục bộ. Chưa có khóa identity tự động; cần kiểm chứng chất lượng bằng ảnh thật khi bắt đầu một truyện.
