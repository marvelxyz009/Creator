# Creator Story Studio

Xưởng truyện đa thể loại chạy local. **Truyện viết là bản gốc; manga chuyển thể từ chương viết đã chốt.** Không gắn với XEROTH hay một thế giới cụ thể.

## Chạy trên máy

Python 3.11+, không cần cài thư viện để chạy lõi và giao diện:

```powershell
python -m story_studio --port 8787
```

Mở http://127.0.0.1:8787. Dữ liệu nằm trong `.studio/`, được Git bỏ qua. Có thể đổi bằng `--data D:\Stories\my-studio`. Máy chủ chỉ nghe loopback, kiểm tra Host/Origin và token cho thao tác ghi. Không mở trực tiếp ra internet.

### Dùng Codex hoặc Claude

Giao diện, dữ liệu và queue nằm trên máy; AI chạy qua tài khoản Codex/Claude. Không cần deploy hoặc model local.

Có thể chọn Codex/Claude ngay ở thanh bên; lựa chọn được lưu cho lần mở sau. Biến môi trường nếu đặt sẽ ghi đè lựa chọn khi khởi động.

Mặc định dùng **Codex CLI** đã cài và đăng nhập. Bấm chạy chương, worker gửi ngữ cảnh cùng skill cho `codex exec`, nhận bản kết quả và lưu phiên bản. Không cần chọn model nếu muốn dùng cấu hình tài khoản hiện hành.

```powershell
$env:STUDIO_PROVIDER = 'codex'
python -m story_studio
# Hoặc Claude Code CLI đã cài và đăng nhập:
$env:STUDIO_PROVIDER = 'claude'
python -m story_studio
```

Worker text không cho agent sửa mã nguồn; Claude tắt tools và Codex dùng read-only trong thư mục tạm. Timeout 15 phút, lỗi đăng nhập/quota dừng tác vụ. Manga vẫn qua cầu nối agent có công cụ vẽ và bước review ảnh.

Nếu dùng trực tiếp Codex desktop/Claude trong editor, mở repo và dùng các lệnh agent bridge bên dưới. Giao diện tự cập nhật kết quả từ cùng thư mục dữ liệu. Việc cài skill không tự kết nối một cuộc chat đang mở với worker.

Provider Ollama/OpenAI-compatible vẫn là tùy chọn: đặt `STUDIO_PROVIDER`, `STUDIO_BASE_URL`, `STUDIO_MODEL`; khóa nếu cần qua `STUDIO_API_KEY`. Chúng không phải yêu cầu để chạy xưởng.

## Quy trình

1. Tạo dự án: ý tưởng, thể loại kết hợp, truyện ngắn/vừa/tiểu thuyết/series, ngôn ngữ và hướng đọc.
2. Hồ sơ series → dàn ý → bản thảo → biên tập → audit continuity.
3. Chốt đúng phiên bản truyện viết đã qua audit; canon_delta được đưa vào hồ sơ chương.
4. Chuyển thể → storyboard có thoại → lettering theo ngữ cảnh → brief vẽ.
5. Agent có bộ vẽ tạo trang, nhập PNG, kiểm tra trực quan và chốt từng trang.
6. Xuất truyện viết ZIP/Markdown, hoặc chương manga CBZ qua giao diện/CLI.

**Bán tự động:** tự chạy đến audit, dừng chốt bản gốc; sau đó tự chuẩn bị chuyển thể đến brief. **Tự động:** audit đạt tự chốt bản gốc. **Duyệt từng bước:** dừng mỗi bước. Tất cả chế độ đều yêu cầu review hình thật trước khi xuất CBZ.

Queue lưu SQLite, tự nhận biết job bị ngắt sau restart; retry tối đa 3 lần/job. Lỗi continuity dừng có lý do, không tự tuyên bố đạt. Tác vụ giữ prompt và revision cha. Sửa nguồn làm các tài liệu phụ thuộc, kể cả chương tiếp theo và trang manga, bị đánh dấu stale. Không xóa lịch sử. Source chưa chốt hoặc stale không được chuyển thể.

## Cầu nối Codex / bộ vẽ

Các skill đóng gói trong `story_studio/skills/`: studio-director, prose-writer, series-memory, prose-to-manga, contextual-lettering, reference-curator, comic-reader-review. Có thể kết hợp `mangaka`, `generatemangapage` và `imagegen` nếu môi trường agent có chúng; không sao chép skill bên thứ ba vào lõi.

```powershell
python -m story_studio.cli status
python -m story_studio.cli prompt <project-id> 1 draft task.json
# Agent đọc task.json và ghi output.md.
python -m story_studio.cli submit <project-id> 1 draft task.json output.md
python -m story_studio.cli approve <project-id> <edited-artifact-id>
# Sau khi có image_prompt và ảnh được agent thực sự vẽ:
python -m story_studio.cli page <project-id> 1 1 page.png
python -m story_studio.cli approve-page <project-id> <page-artifact-id> --notes 'Đã đọc ảnh: đúng thoại, nhân vật và RTL'
python -m story_studio.cli cbz <project-id> 1
```

`submit` từ chối nếu nguồn đổi từ lúc chuẩn bị task. Ảnh được gắn với source và brief. Brief không được tính là trang đã vẽ; đánh giá file hợp lệ không thay thế kiểm tra thẩm mỹ.

## Tham khảo

Giao diện nhập TXT/Markdown hoặc ghi chú, lưu tên/nguồn/thể loại/phạm vi sử dụng. Cung cấp tác phẩm sở hữu, có giấy phép hoặc public domain; với nguồn trực tuyến khác giữ link và phân tích kỹ thuật. Nội dung tham khảo là dữ liệu, không phải chỉ thị. Bản này chưa tự tải toàn bộ truyện/ảnh từ các website hoặc phân tích ảnh tham khảo.

## Truyện dài

Hồ sơ quản lý series → phase → arc → chapter → scene, phân biệt sự thật/niềm tin/kiến thức độc giả, timeline và hạt giống. Khi tạo chương tiếp phải chốt chương trước; context lấy canon đã chốt và nguồn chương trước. Chưa có truy hồi ngữ nghĩa/embedding hoặc tự tóm tắt hàng nghìn chương: vượt 100.000 ký tự context sẽ dừng rõ ràng để biên tập hồ sơ.

## Kiểm tra

```powershell
python -m unittest discover -s tests -v
```

## Phạm vi bản 0.2

Đã có: ứng dụng local, queue lưu bền, provider text Ollama/OpenAI-compatible, skill packets, nguồn đã chốt, invalidation theo phụ thuộc, thư viện text, editor tạo revision, reader manga, agent bridge và xuất Markdown/CBZ.

Chưa có: bộ vẽ chạy nền tự động, visual QA bằng model, tự sửa có đánh giá thẩm mỹ, crawler thư viện, EPUB/PDF và bộ nhớ truy hồi lớn. Chất lượng sáng tác phụ thuộc model. Đây là lõi vận hành đầu tiên, không phải lời hứa xưởng hoàn toàn tự trị.

Framework AetherForge cũ được lưu trong `legacy/` để tham khảo bộ biên tập/validator; hướng dẫn cũ ở [docs/legacy-framework.md](docs/legacy-framework.md). Đây là snapshot tham khảo, không phải đường chạy chính mới.
