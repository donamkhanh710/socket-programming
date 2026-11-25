"""Nhập và kiểm tra thông điệp trước khi mở kết nối TCP."""
import socket
from protocol import encode_message, recv_message, send_message

HOST = "127.0.0.1"
PORT = 9000


def main():
    while True:
        try:
            message = input("Nhập thông điệp gửi tới server: ")
            encode_message(message)  # Kiểm tra độ dài và UTF-8 trước khi kết nối.
            break
        except ValueError as error:
            print(f"Dữ liệu chưa hợp lệ: {error}. Hãy nhập lại.")
        except (EOFError, KeyboardInterrupt):
            print("\nĐã hủy nhập; chưa mở kết nối")
            return
    try:
        with socket.create_connection((HOST, PORT), timeout=10) as client:
            print("Đã kết nối tới server")
            send_message(client, message)
            print("Đã gửi thông điệp")
            response = recv_message(client)
            print(f"Phản hồi: {response}")
    except ConnectionRefusedError:
        print("Kết nối bị từ chối. Kiểm tra server đã chạy và HOST/PORT có đúng không.")
        return 1
    except TimeoutError:
        print("Hết thời gian kết nối hoặc trao đổi. Kiểm tra cửa sổ server.")
        return 1
    except (OSError, ValueError) as error:
        print(f"Trao đổi không hoàn tất: {error}. Kiểm tra cửa sổ server.")
        return 1
    except KeyboardInterrupt:
        print("\nĐã hủy kết nối")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
