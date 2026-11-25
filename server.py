"""Server TCP cơ bản, xử lý lần lượt từng client, chưa có TLS."""
import socket
from protocol import recv_message, send_message

HOST = "127.0.0.1"
PORT = 9000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Server đang lắng nghe tại {HOST}:{PORT}", flush=True)
        while True:
            conn, address = server.accept()
            print(f"Client kết nối: {address}", flush=True)
            with conn:
                try:
                    message = recv_message(conn)
                    # repr giúp phân biệt chuỗi rỗng và hiển thị ký tự điều khiển an toàn.
                    print(f"Đã nhận: {message!r}", flush=True)
                    send_message(conn, "Server đã nhận thông điệp")
                    print("Đã gửi phản hồi", flush=True)
                except TimeoutError:
                    print("Hết thời hạn gửi/nhận; đóng kết nối này", flush=True)
                except (OSError, ValueError) as error:
                    print(f"Lỗi phiên: {error!r}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng server")
    except OSError as error:
        print(f"Không thể khởi động hoặc tiếp tục phục vụ: {error}")
        raise SystemExit(1)
