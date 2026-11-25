"""Giao thức bài 1: 4 byte độ dài + nội dung UTF-8, tối đa 4096 byte."""
import struct
import time

MAX_MESSAGE_SIZE = 4096
IO_TIMEOUT = 10.0


def encode_message(message):
    """Kiểm tra trước khi kết nối; độ dài tính theo byte UTF-8."""
    payload = message.encode("utf-8")
    if len(payload) > MAX_MESSAGE_SIZE:
        raise ValueError(f"Thông điệp có {len(payload)} byte, tối đa {MAX_MESSAGE_SIZE}")
    return payload


def _remaining(deadline):
    seconds = deadline - time.monotonic()
    if seconds <= 0:
        raise TimeoutError("Hết thời hạn trao đổi một thông điệp")
    return seconds


def _recv_exact(sock, size, deadline):
    data = bytearray()
    while len(data) < size:
        # Cùng một deadline cho cả header và nội dung, không gia hạn mỗi lần đọc.
        sock.settimeout(_remaining(deadline))
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError(
                f"Đối tác đóng kết nối: mới nhận {len(data)}/{size} byte của phần đang đọc"
            )
        data.extend(chunk)
    return bytes(data)


def send_message(sock, message, timeout=IO_TIMEOUT):
    payload = encode_message(message)
    sock.settimeout(timeout)
    sock.sendall(struct.pack("!I", len(payload)) + payload)


def recv_message(sock, timeout=IO_TIMEOUT):
    deadline = time.monotonic() + timeout
    header = _recv_exact(sock, 4, deadline)
    size = struct.unpack("!I", header)[0]
    if size > MAX_MESSAGE_SIZE:
        raise ValueError(f"Độ dài khai báo {size} vượt giới hạn {MAX_MESSAGE_SIZE}")
    # size=0 hợp lệ: thông điệp rỗng.
    return _recv_exact(sock, size, deadline).decode("utf-8")
