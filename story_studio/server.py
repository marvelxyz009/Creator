"""Loopback-only local UI, a durable worker and a small JSON API."""
from __future__ import annotations
import argparse
import base64
import json
import mimetypes
import secrets
import struct
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from .core import PACKAGE_ROOT, DEFAULT_DATA, GENRES, STAGES, Studio, encode

class Server(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address, studio):
        super().__init__(address, Handler)
        self.studio = studio
        self.token = secrets.token_urlsafe(32)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def send(self, value, status=200, content_type="application/json; charset=utf-8"):
        body = value if isinstance(value, bytes) else encode(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def guard(self, write=False):
        host = self.headers.get("Host", "")
        valid = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        if host not in valid:
            raise ValueError("Invalid local host")
        origin = self.headers.get("Origin")
        if origin and origin not in {"http://" + h for h in valid}:
            raise ValueError("Cross-origin request rejected")
        if write and not secrets.compare_digest(self.headers.get("X-Studio-Token", ""), self.server.token):
            raise ValueError("Invalid request token")

    def do_GET(self):
        try:
            self.guard()
            u = urllib.parse.urlparse(self.path)
            q = urllib.parse.parse_qs(u.query)
            studio = self.server.studio
            if u.path == "/":
                page = (PACKAGE_ROOT / "web" / "index.html").read_text(encoding="utf-8").replace("__TOKEN__", self.server.token)
                self.send(page.encode(), content_type="text/html; charset=utf-8")
            elif u.path == "/api/state":
                self.send({"projects": studio.projects(), "jobs": studio.jobs(), "references": studio.references(), "genres": GENRES, "stages": STAGES, "provider": {"mode": getattr(studio.provider, "mode", "test"), "model": getattr(studio.provider, "model", "")}, "skills": sorted(p.name for p in (PACKAGE_ROOT / "skills").iterdir() if p.is_dir())})
            elif u.path == "/api/project":
                id = q["id"][0]
                self.send({"project": studio.project(id), "artifacts": studio.artifacts(id), "jobs": studio.jobs(id)})
            elif u.path == "/api/export":
                file = studio.export(q["id"][0])
                self.send(file.read_bytes(), content_type="application/zip")
            elif u.path == "/api/cbz":
                file = studio.export_cbz(q["id"][0], int(q["chapter"][0]))
                self.send(file.read_bytes(), content_type="application/vnd.comicbook+zip")
            elif u.path == "/api/page":
                project, artifact = q["project"][0], q["id"][0]
                row = next((r for r in studio.artifacts(project) if r["id"] == artifact and r["kind"] == "page"), None)
                if not row:
                    raise ValueError("Page not found")
                file = studio.root / "projects" / project / "pages" / (artifact + ".png")
                self.send(file.read_bytes(), content_type="image/png")
            else:
                self.send({"error": "Not found"}, 404)
        except (ValueError, KeyError, OSError) as exc:
            self.send({"error": str(exc)}, 400)

    def do_POST(self):
        try:
            self.guard(write=True)
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 16_000_000:
                raise ValueError("Request size invalid")
            data = json.loads(self.rfile.read(size))
            studio = self.server.studio
            if self.path == "/api/projects":
                result = studio.create(data)
            elif self.path == "/api/enqueue":
                result = studio.enqueue(data["project"], int(data.get("chapter", 1)), data.get("stage", "bible"))
            elif self.path == "/api/retry":
                result = studio.retry(data["id"])
            elif self.path == "/api/provider":
                result = studio.select_provider(data["mode"])
            elif self.path == "/api/pause":
                result = studio.pause(data["project"], data["paused"])
            elif self.path == "/api/approve-page":
                result = studio.approve_page(data["project"], data["id"], str(data["notes"]))
            elif self.path == "/api/continue":
                result = studio.continue_job(data["id"])
            elif self.path == "/api/revise":
                old = next(r for r in studio.artifacts(data["project"]) if r["id"] == data["id"])
                if old["kind"] == "page":
                    raise ValueError("Use page upload for images")
                result = studio.save(data["project"], old["chapter"], old["kind"], str(data["body"]), old["parents"])
            elif self.path == "/api/references":
                result = studio.add_reference(data)
            elif self.path == "/api/page":
                raw = base64.b64decode(data["png"], validate=True)
                result = studio.import_page(data["project"], int(data["chapter"]), int(data["number"]), raw)
            else:
                raise ValueError("Unknown operation")
            self.send({"ok": True, "result": result})
        except (ValueError, KeyError, TypeError, StopIteration, OSError) as exc:
            self.send({"error": str(exc) or "Artifact not found"}, 400)

def main():
    parser = argparse.ArgumentParser(description="Creator Story Studio local server")
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    studio = Studio(args.data)
    # Hold an OS lock so a second process cannot recover another worker's jobs.
    lock = (studio.root / "server.lock").open("a+b")
    lock.seek(0)
    if __import__("os").name == "nt":
        import msvcrt
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            raise SystemExit("Studio data directory is already in use")
    else:
        import fcntl
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise SystemExit("Studio data directory is already in use")
    server = Server(("127.0.0.1", args.port), studio)
    studio.recover()
    stop = threading.Event()
    def worker():
        while not stop.is_set():
            if not studio.run_one():
                stop.wait(1)
    threading.Thread(target=worker, daemon=True).start()
    print(f"Creator Story Studio: http://127.0.0.1:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()
        lock.close()

if __name__ == "__main__":
    main()
