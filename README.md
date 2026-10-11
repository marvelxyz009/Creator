# Creator — xưởng truyện trong chat

**Thao tác hoàn toàn trên chat. Truyện viết là bản gốc; manga chuyển thể từ chương đã chốt.** Dùng AI và công cụ vẽ có sẵn trong phiên Codex/Claude hiện tại, lưu mọi kết quả vào folder trên máy. Không giao diện web, server local, worker nền, provider API hay gọi một Codex/Claude CLI khác.

## Cách dùng

Mở repo trong Codex/Claude hoặc dùng skill **creator-studio**. Nói ý tưởng, hoặc yêu cầu AI đề xuất. Trợ lý hỏi lựa chọn trực tiếp trong chat:

1. Ba concept → bạn chọn.
2. Ba hướng truyện dựa trên concept → bạn chọn.
3. Ba hướng mỹ thuật phù hợp → bạn chọn.
4. AI viết, biên tập, audit và lưu chương; chuyển thể, vẽ bằng công cụ của phiên chat, xem ảnh thật rồi sửa nếu cần.

Không cần nhập form title/style/direction/mode hay cấu hình model CLI. Trợ lý suy ra các thông số, lưu đúng câu trả lời và đọc lại chúng khi tiếp tục. Bạn có thể đổi yêu cầu hoặc tự đưa hướng cụ thể. Chỉ hỏi ở điểm lựa chọn có ý nghĩa; các bước kỹ thuật do trợ lý xử lý.

## Lưu ở đâu

Mặc định **`D:\Creator\stories`** khi làm việc trong checkout này. Repo khác dùng `<repo>/stories`. `STUDIO_DATA` hoặc `--data` có thể đổi thư mục.

```text
stories/
  studio.sqlite3
  sessions/<id>/
    session.json              # đề xuất, lựa chọn, lịch sử
    progress.md
  projects/<id>/
    project.json              # premise và hướng đã chọn
    progress.md               # phần đang làm, bước tiếp theo
    progress.json
    tasks/*.json              # context + revision cha
    chapters/0001/*.md        # các bản truyện, storyboard, lettering
    pages/*.png               # ảnh thật đã lưu
    reviews/*.json            # review đúng ảnh, kể cả chưa đạt
    book.zip / chapter-0001.cbz
```

Nội dung truyện được Git bỏ qua mặc định. Code và skill được push riêng. Dữ liệu `.studio/` cũ được giữ nguyên; đọc bằng `--data D:\Creator\.studio` khi cần, không tự chuyển hay xóa.

## Canon và ảnh thật

Mọi bản sửa tạo revision mới. Thay nguồn làm các bản chuyển thể/trang phụ thuộc cần cập nhật. Manga chỉ dùng edited prose mới nhất đã qua continuity audit. Canon, timeline, nhân vật, quan hệ và các hạt giống nằm trong hồ sơ; chương tiếp phải dựa trên chương trước đã chốt.

Ảnh dùng công cụ tạo/sửa ảnh **của phiên chat**, rồi lưu PNG thật và import. Trợ lý phải nhìn ảnh để kiểm tra diễn xuất, nhận dạng, bố cục, thoại và thứ tự đọc. Review ghi hash ảnh cùng thoại mong đợi/đọc được; schema hợp lệ không tự chứng minh chất lượng. Sửa tối đa hai lần/trang rồi hỏi về vấn đề còn lại. Chỉ trang hiện hành đã qua review mới xuất CBZ; ảnh đổi sau duyệt phải kiểm tra lại.

Codex chat có imagegen khi được cấp công cụ. Claude cần công cụ ảnh trong phiên của nó; không phải mọi phiên Claude đều vẽ được. Nếu không có công cụ hoặc không xuất được ảnh về file, trợ lý báo hạn chế cụ thể. Không tạo ảnh giả thay thế. Không tự chạy tiếp khi chat dừng.

## Lệnh nội bộ dành cho trợ lý

Python 3.11+, không cần thư viện ngoài. Người dùng không cần nhập các lệnh này:

```powershell
python -m story_studio                     # status, không mở giao diện
python -m story_studio start --seed 'gợi ý tùy chọn'
python -m story_studio offer <session> options.json
python -m story_studio choose <session> 0 <proposal-revision>
python -m story_studio resume <project> --chapter 1
python -m story_studio prompt <project> 1 draft task.json
python -m story_studio submit <project> 1 draft task.json output.md
python -m story_studio approve <project> <edit-id>
python -m story_studio image-task <project> 1 1 image-task.json
python -m story_studio page <project> 1 1 D:\output\page.png --packet image-task.json
python -m story_studio review-page <project> <page-id> review.json
python -m story_studio export <project>
python -m story_studio cbz <project> 1
```

`offer` nhận JSON array đúng ba đề xuất. Concept cần title/summary/tradeoff/genres; hướng truyện thêm length; hướng mỹ thuật thêm direction. Lệnh choose dùng index 0–2 và revision của bộ lựa chọn hiện hành. Submit từ chối packet có nguồn đã thay đổi. Progress cập nhật sau lưu, chốt hoặc import; resume luôn tính lại từ dữ liệu hiện tại.

## Skill và kiểm tra

Entry skill: [creator-studio](story_studio/skills/creator-studio/SKILL.md). Các vai: studio-director, story-architect, character-designer, art-director, prose-writer, series-memory, prose-to-manga, contextual-lettering, reference-curator, comic-reader-review.

Có entry skill trong `.agents/skills/` cho Codex và `.claude/skills/` cho Claude. Master bản trên máy được cài tại `C:\Users\Admin\.codex\skills\creator-studio\SKILL.md`. Các bản entry được kiểm tra đồng bộ.

```powershell
python -m unittest discover -s tests -v
```

Bản 0.4 giữ lõi canon/revision và xuất Markdown/CBZ. Chưa có EPUB/PDF hay truy hồi embedding cho hàng nghìn chương; context quá lớn cần biên tập hồ sơ. Framework trước nằm trong `legacy/`; các phiên bản UI/worker đã bỏ khỏi đường chạy hiện hành, vẫn có lịch sử Git.
