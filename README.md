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

Worker text không cho agent sửa mã nguồn; Claude tắt tools và Codex dùng read-only trong thư mục tạm. Timeout 15 phút, lỗi đăng nhập/quota dừng tác vụ. Worker manga riêng giữ tools MCP và gọi vision với ảnh thật; quyền thực thi của CLI được giữ nguyên, không dùng cờ bypass. Nếu thiếu tool/quyền hoặc ảnh không đạt, tác vụ dừng.

Nếu dùng trực tiếp Codex desktop/Claude trong editor, mở repo và dùng các lệnh agent bridge bên dưới. Giao diện tự cập nhật kết quả từ cùng thư mục dữ liệu. Việc cài skill không tự kết nối một cuộc chat đang mở với worker.

Provider Ollama/OpenAI-compatible vẫn là tùy chọn: đặt `STUDIO_PROVIDER`, `STUDIO_BASE_URL`, `STUDIO_MODEL`; khóa nếu cần qua `STUDIO_API_KEY`. Chúng không phải yêu cầu để chạy xưởng.

## Quy trình

1. AI đưa **3 concept → 3 hướng truyện → 3 hướng mỹ thuật**. Bạn chỉ chọn; gợi ý ban đầu là tùy chọn. Lựa chọn và lịch sử được lưu bền. AI suy ra thể loại, độ dài, style và hướng đọc. Hồ sơ thủ công nằm trong lựa chọn nâng cao.
2. Giao diện: **Ý tưởng → Cốt truyện → Nhân vật → Mỹ thuật → Sản xuất**. Dây chuyền bên dưới: hồ sơ → dàn ý → thiết kế nhân vật → art bible → bản thảo → biên tập → audit continuity.
3. Chốt đúng phiên bản truyện viết đã qua audit; canon_delta được đưa vào hồ sơ chương.
4. Chuyển thể → storyboard có thoại → lettering theo ngữ cảnh → brief vẽ.
5. Worker nền gọi Codex/Claude với MCP bộ vẽ, nhận PNG thật, đưa ảnh vào visual QA, sửa tối đa hai lần/trang và kiểm tra lại. Chỉ trang đạt cả hình và đúng thoại mới được model QA chốt.
6. Xuất truyện viết ZIP/Markdown, hoặc chương manga CBZ qua giao diện/CLI.

**Bán tự động:** tự chạy đến audit, dừng chốt bản gốc; sau đó tự chuẩn bị chuyển thể đến brief. **Tự động:** audit đạt tự chốt bản gốc. **Duyệt từng bước:** dừng mỗi bước. Tất cả chế độ đều yêu cầu review hình thật trước khi xuất CBZ; model QA được ghi rõ là model review, người dùng vẫn có thể đọc kiểm tra thêm.

Queue lưu SQLite, tự nhận biết job bị ngắt sau restart; retry tối đa 3 lần/job. Lỗi continuity dừng có lý do, không tự tuyên bố đạt. Tác vụ giữ prompt và revision cha. Sửa nguồn làm các tài liệu phụ thuộc, kể cả chương tiếp theo và trang manga, bị đánh dấu stale. Không xóa lịch sử. Source chưa chốt hoặc stale không được chuyển thể.

## Cầu nối Codex / bộ vẽ

Các skill đóng gói trong `story_studio/skills/`: studio-director, story-architect, character-designer, art-director, prose-writer, series-memory, prose-to-manga, contextual-lettering, reference-curator, comic-reader-review. Có thể kết hợp `mangaka`, `generatemangapage` và `imagegen` nếu môi trường agent có chúng; không sao chép skill bên thứ ba vào lõi.

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

## Phạm vi bản 0.3

Đã có: ứng dụng local, queue lưu bền, provider text Ollama/OpenAI-compatible, skill packets, nguồn đã chốt, invalidation theo phụ thuộc, thư viện text, editor tạo revision, reader manga, agent bridge và xuất Markdown/CBZ.

Đã thêm worker nền MCP generation → actual-image model QA → repair tối đa hai lần → re-QA, cùng lưu snapshot và báo cáo mỗi lượt.

Chưa có: crawler thư viện, EPUB/PDF và bộ nhớ truy hồi lớn. Chất lượng sáng tác phụ thuộc model. Worker không thay thế kết nối dịch vụ thật. Các test fixture chứng minh cơ chế và giới hạn lỗi; chưa chứng minh chất lượng manga của model thật.

Framework AetherForge cũ được lưu trong `legacy/` để tham khảo bộ biên tập/validator; hướng dẫn cũ ở [docs/legacy-framework.md](docs/legacy-framework.md). Đây là snapshot tham khảo, không phải đường chạy chính mới.

## Hướng sáng tạo

Story Architect thiết kế nhân quả, phase và cách tiết lộ thông tin; Character Designer tạo động lực, quan hệ, giọng nói và nhận dạng; Art Director chốt ngôn ngữ hình ảnh và thoại. Các đầu ra nhân vật/mỹ thuật là phiên bản thật, tham gia dependency của bản thảo và chuyển thể. Sửa chúng làm nội dung phụ thuộc cần cập nhật.

Studio Director giữ lời hứa cảm xúc của tác phẩm và quyết định hướng sáng tạo có lý do. Các tiêu chí review/repair ảnh trong skill được worker dùng khi công cụ ảnh MCP của CLI đã kết nối. Giao diện chính giấu kỹ thuật trong phần chi tiết vận hành.

## Worker manga qua Codex/Claude MCP

Không yêu cầu API ảnh riêng hoặc deploy. Dùng cấu hình MCP và đăng nhập của CLI đã chọn. Công cụ của Codex desktop/chat hiện tại không tự trở thành công cụ của `codex exec`; cấu hình MCP CLI cần có dịch vụ thực sự hỗ trợ image generation/edit. Claude cần công cụ vẽ bên ngoài, còn vision dùng Read ảnh cục bộ. Codex QA nhận PNG qua `--image`.

Dự án tạo từ ba vòng chọn mặc định auto: khi bạn bắt đầu sản xuất chương, worker viết tới brief rồi tự xếp việc vẽ. Dự án thủ công có nút **Vẽ manga tự động qua MCP**. Một tác vụ vẽ tối đa 64 trang; mỗi trang tối đa một bản đầu và hai bản sửa trong một lần chạy. Retry do người dùng chọn có thể phát sinh lượt vẽ mới; tối đa ba lần chạy/job. Các trang đã qua QA được checkpoint để tiếp tục sau lỗi; sửa nguồn buộc tác vụ mới.

Mỗi ảnh cần PNG có cấu trúc/CRC hợp lệ, receipt gọi MCP thành công trong log CLI, và QA của ảnh thật. Lưu prompt/response, tool receipts, snapshots và reports trong `.studio/projects/<id>/media_jobs/`. QA so khớp thoại theo thứ tự đọc; không xem một brief là ảnh. File đã chốt ghi rõ model review; thẩm mỹ và lỗi model vẫn cần đánh giá khi xuất bản.

Máy hiện tại chưa phát hiện MCP image-generation trong cấu hình Codex CLI. Cài/kết nối nó trong CLI trước khi chạy vẽ thật. Công cụ imagegen của cuộc chat không có endpoint ứng dụng để worker gọi trực tiếp. Không lưu token MCP vào repo.

Lỗi kiểm chứng CLI trên máy hiện tại: model mặc định `gpt-6.1-sol` bị endpoint CLI từ chối. Dùng **Tùy chọn trợ lý** để chọn tên model CLI thực sự khả dụng; lựa chọn chỉ lưu cho xưởng, không sửa cấu hình toàn máy. Không tự chuyển model khi tài khoản từ chối. Lỗi này tách biệt với việc thiếu MCP ảnh.

Với MCP bộ vẽ có tên tool riêng không chứa image-generation/edit, đặt `STUDIO_IMAGE_TOOL` đúng tên tool để worker kiểm tra receipt thay vì đoán. Cờ quyền/đăng nhập/MCP của tài khoản được tôn trọng; worker không tự thêm tài khoản hoặc bypass approval.
