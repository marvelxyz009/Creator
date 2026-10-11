# Creator Story Studio — tiến độ

Bản 0.2 chuyển repo Creator sang xưởng truyện đa thể loại local. Nhánh: story-studio.

Đã triển khai giao diện, SQLite queue, phiên bản và dependency invalidation, provider text, bảy skill, cầu nối agent, thư viện tham khảo, reader PNG và xuất Markdown/CBZ. Manga lấy nguồn chương viết đã qua audit; sửa nguồn buộc kiểm tra lại tài liệu và ảnh phụ thuộc.

Đã kiểm tra: unit/integration tests, thao tác giao diện bằng Edge, đóng gói wheel kèm giao diện và skills. Các bài thử dùng provider fixture, không đại diện chất lượng model thật.

Mặc định Codex CLI; có adapter Claude Code CLI. Giao diện local, không cần deploy/model local. Codex CLI có trên máy; chưa chạy thực nghiệm sinh chương bằng tài khoản. Claude CLI chưa được phát hiện trên PATH. Bộ vẽ và review ảnh đi qua agent bridge; chưa có worker sinh hình nền.

Ưu tiên tiếp theo: tích hợp bộ vẽ với model/credentials do người dùng chọn; truy hồi bộ nhớ series lớn; reference importer theo nguồn được phép; vòng sửa sau review; EPUB/PDF. Cập nhật file này cùng mã và kiểm tra khi thay đổi phạm vi.
