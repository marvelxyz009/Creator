# Tái sinh Tề Thiên

Đồng nhân Tây Du • series tu luyện, hành động và lập thế lực • mỹ thuật thần thoại thủy mặc.

## Đọc truyện

- [Chương 1 — Ngày đá biết đau](chapter-01.md): bản biên tập hiện hành đã qua continuity audit của trợ lý.
- [Nền truyện](series-bible.md), [khung phase](phase-outline.md), [nhân vật](characters.md), [mỹ thuật](art-bible.md).
- [Tiến độ sáng tác](writing-progress.md), [ghi chú audit](chapter-01-audit-notes.md), [hồ sơ nguồn](references/tay-du-arc-01.md).

Bản thảo và revision cũ được giữ để truy vết; không dùng thay chapter-01.md. Chưa có manga.

## Lưu trạng thái

Các thư mục chapters/ và tasks/ giữ revision và liên kết nguồn. git-snapshot.json lưu riêng project, mọi artifact với trạng thái approved/stale và phiên lựa chọn tại thời điểm push, để không phụ thuộc database SQLite của máy hiện tại. book.zip là bản xuất đọc truyện đã duyệt. Không xuất dữ liệu của truyện khác.

Sau khi clone, các file Markdown đọc được ngay. Để tiếp tục qua harness trên máy khác, khôi phục project và artifacts từ git-snapshot.json vào database local, giữ nguyên ID, thứ tự artifact, parents, approved và stale. Không chạy create để tạo ID mới rồi ghép revision cũ.

Người dùng đã yêu cầu lưu toàn bộ truyện này vào Git. Khi viết tiếp, cập nhật chương, audit/canon, writing-progress và git-snapshot trước commit/push. Các truyện khác vẫn lưu local mặc định.
