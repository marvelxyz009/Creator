"""Bounded PNG structural validation; does not edit artwork."""
import struct
import zlib

def validate_png(raw):
    if len(raw) > 12_000_000 or raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 33:
        raise ValueError("Upload a real PNG under 12MB")
    offset, seen, compressed = 8, [], bytearray()
    while offset < len(raw):
        if offset + 12 > len(raw):
            raise ValueError("Truncated PNG")
        size = struct.unpack(">I", raw[offset:offset+4])[0]
        end = offset + size + 12
        if end > len(raw):
            raise ValueError("Truncated PNG chunk")
        kind, data = raw[offset+4:offset+8], raw[offset+8:offset+8+size]
        crc = struct.unpack(">I", raw[end-4:end])[0]
        if zlib.crc32(kind + data) & 0xffffffff != crc:
            raise ValueError("PNG CRC mismatch")
        seen.append(kind)
        if kind == b"IHDR":
            if len(seen) != 1 or size != 13:
                raise ValueError("Invalid PNG header")
            width, height = struct.unpack(">II", data[:8])
            if not 0 < width <= 10000 or not 0 < height <= 20000:
                raise ValueError("Invalid image dimensions")
        if kind == b"IDAT":
            compressed.extend(data)
        if kind == b"IEND":
            if size or end != len(raw):
                raise ValueError("Invalid PNG ending")
            break
        offset = end
    if not seen or seen[0] != b"IHDR" or seen[-1] != b"IEND" or not compressed:
        raise ValueError("Incomplete PNG")
    try:
        decoder = zlib.decompressobj()
        decoder.decompress(bytes(compressed), 64_000_001)
        if not decoder.eof or decoder.unused_data:
            raise ValueError("Invalid or oversized PNG image data")
    except zlib.error as exc:
        raise ValueError("Invalid PNG compression") from exc
    return width, height
