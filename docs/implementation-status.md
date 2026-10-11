# Creator Story Studio — tiến độ

Bản 0.2 chuyển repo Creator sang xưởng truyện đa thể loại local. Nhánh: story-studio.

Đã triển khai giao diện, SQLite queue, phiên bản và dependency invalidation, provider text, mười skill, cầu nối agent, thư viện tham khảo, reader PNG và xuất Markdown/CBZ. Manga lấy nguồn chương viết đã qua audit; sửa nguồn buộc kiểm tra lại tài liệu và ảnh phụ thuộc.

Đã kiểm tra: unit/integration tests, thao tác giao diện bằng Edge, đóng gói wheel kèm giao diện và skills. Các bài thử dùng provider fixture, không đại diện chất lượng model thật.

Mặc định Codex CLI; có adapter Claude Code CLI. Giao diện local, không cần deploy/model local. Codex CLI có trên máy; chưa chạy thực nghiệm sinh chương bằng tài khoản. Claude CLI chưa được phát hiện trên PATH. Bộ vẽ và review ảnh đi qua agent bridge; chưa có worker sinh hình nền.

Ưu tiên tiếp theo: tích hợp bộ vẽ với model/credentials do người dùng chọn; truy hồi bộ nhớ series lớn; reference importer theo nguồn được phép; vòng sửa sau review; EPUB/PDF. Cập nhật file này cùng mã và kiểm tra khi thay đổi phạm vi.

Đợt UX sáng tạo: năm chặng Ý tưởng/Cốt truyện/Nhân vật/Mỹ thuật/Sản xuất; thêm characters và art vào queue, context và dependency; ba specialist và creative thesis của director. Đã kiểm tra role routing và invalidation khi sửa thiết kế. Chưa có vòng tự vẽ/visual QA/auto-fix thực thi.

Đợt tự động hóa: discovery queue lưu bền, ba vòng ba lựa chọn và tự suy ra project settings. Worker manga độc lập qua MCP agent, PNG validation, actual-image model QA, kiểm tra thoại, hai repair/re-QA, tool-call receipts, checkpoints và source pinning. Kiểm tra bằng fixtures; không gọi một placeholder là demo manga. Hiện CLI Codex chưa có MCP image generation; chưa có kiểm chứng chất lượng render/QA bằng nhà cung cấp thật. Cần kết nối dịch vụ ảnh qua cấu hình CLI.

Kiểm chứng provider thật: discovery bị CLI từ chối vì model mặc định gpt-6.1-sol không được endpoint ChatGPT CLI hỗ trợ. Đã bổ sung lưu model riêng của xưởng và lỗi phân biệt model/đăng nhập. Chưa có phiên đề xuất thật thành công; kiểm tra UI dùng fixture minh bạch. Không thay cấu hình model/MCP toàn máy.
