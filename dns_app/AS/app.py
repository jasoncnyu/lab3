# Jaesung Choi (jc13152)
import socket

AS_HOST = "0.0.0.0"
AS_PORT = 53533
DNS_RECORDS_FILE = "dns_records.txt"  # DNS 정보를 저장할 파일 경로

def save_record_to_file(record):
    """
    DNS 레코드를 파일에 저장
    """
    with open(DNS_RECORDS_FILE, "a") as file:
        file.write(record + "\n")
    print(f"Record saved: {record}")

def load_records_from_file():
    """
    파일에서 DNS 레코드를 로드
    """
    records = {}
    try:
        with open(DNS_RECORDS_FILE, "r") as file:
            for line in file:
                record = line.strip().split(',')
                if len(record) == 4:  # NAME, VALUE, TYPE, TTL
                    name, value, _type, ttl = record
                    records[name] = (value, _type, ttl)
    except FileNotFoundError:
        pass  # 파일이 없을 경우 빈 딕셔너리 반환
    return records

def handle_registration(data):
    """
    FS 서버에서 받은 등록 요청을 처리하고 파일에 기록
    """
    lines = data.split("\n")
    record_type = lines[0].split("=")[1]  # TYPE=A
    name = lines[1].split("=")[1]  # NAME=fibonacci.com
    value = lines[2].split("=")[1]  # VALUE=IP_ADDRESS
    ttl = lines[3].split("=")[1]  # TTL=10

    record = f"{name},{value},{record_type},{ttl}"
    save_record_to_file(record)
    return "Registration successful"

def handle_dns_query(data, records):
    """
    DNS 쿼리 요청을 처리
    """
    lines = data.split("\n")
    record_type = lines[0].split("=")[1]  # TYPE=A
    name = lines[1].split("=")[1]  # NAME=fibonacci.com

    # 파일에서 로드한 레코드에서 해당 이름의 IP 조회
    if name in records:
        value, _type, ttl = records[name]
        response = f"TYPE={_type}\nNAME={name}\nVALUE={value}\nTTL={ttl}\n"
        return response
    else:
        return "Record not found"

def start_as_server():
    """
    AS 서버 시작
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((AS_HOST, AS_PORT))

    print(f"Authoritative Server running on {AS_HOST}:{AS_PORT}")
    
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()

        # 파일에서 기존 DNS 레코드 로드
        records = load_records_from_file()

        if "VALUE" in message:
            # 등록 요청 처리
            response = handle_registration(message)
        else:
            # DNS 쿼리 요청 처리
            response = handle_dns_query(message, records)

        # 응답 전송
        sock.sendto(response.encode(), addr)

if __name__ == "__main__":
    start_as_server()