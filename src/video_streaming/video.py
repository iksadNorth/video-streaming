import aiofiles

async def range_stream(file_path: str, start: int, end: int):
    async with aiofiles.open(file_path, mode="rb") as f:
        await f.seek(start)
        remaining_bytes = end - start + 1
        while remaining_bytes > 0:
            chunk_size = min(1024 * 1024, remaining_bytes)
            data = await f.read(chunk_size)
            if not data:
                break
            yield data
            remaining_bytes -= len(data)

def parse_range(range_header, file_size):
    if not range_header:
        return 0, file_size - 1
    range_str = range_header.replace("bytes=", "").strip()
    start, end = range_str.split("-")[:2] if "-" in range_str else (int(range_str or 0), file_size - 1)
    start   = int(start)    if start    else 0
    end     = int(end)      if end      else file_size - 1
    return start, end
