from src.video_streaming.video import parse_range, range_stream
import pytest
import aiofiles
import pytest_asyncio
from pathlib import Path


@pytest.mark.parametrize(
    "range_header, file_size, expected",
    [
        ('bytes=0-', 15342523, (0, 15342523 - 1)),
        ('bytes=', 15342523, (0, 15342523 - 1)),
        ('bytes=0-234623', 15342523, (0, 234623)),
        ('bytes=-234623', 15342523, (0, 234623)),
        ('242-234623', 15342523, (242, 234623)),
        ('242-', 15342523, (242, 15342523 - 1)),
        ('-234623', 15342523, (0, 234623)),
    ]
)
def test_error_parse_range(range_header, file_size, expected):
    assert parse_range(range_header, file_size) == expected


@pytest_asyncio.fixture(scope="function")
async def dummy_video_file(tmp_path: Path):
    """테스트용 더미 비디오 파일 생성 후 테스트 종료 시 삭제"""
    test_file = tmp_path / "test_video.mp4"
    test_content = b"0123456789" * 1000  # 10KB 더미 데이터

    # 파일 생성
    async with aiofiles.open(test_file, mode="wb") as f:
        await f.write(test_content)
    
    # 테스트에서 사용될 파일 경로와 데이터 반환
    yield str(test_file), test_content  

    # 정리 작업 (테스트 종료 후 실행됨). 파일 삭제
    test_file.unlink(missing_ok=True)

@pytest.mark.asyncio
async def test_range_stream(dummy_video_file):
    """range_stream이 올바르게 데이터를 스트리밍하는지 테스트"""
    test_file, test_content = dummy_video_file  # fixture에서 파일 경로와 내용 받기
    start, end = 0, 4095  # 4KB 읽기

    received_data = b""
    async for chunk in range_stream(test_file, start, end):
        received_data += chunk

    assert received_data == test_content[start:end + 1]  # 올바른 데이터인지 확인
    assert len(received_data) == (end - start + 1)  # 요청한 크기만큼 읽었는지 확인
