
from pathlib import Path


# Define the path to the log file.
LOG_FILE = Path(__file__).resolve().parent / "sample_logs" / "auth.log"


def read_logs(file_path: Path) -> list[str]:
    """Read the log file and return its lines."""

    with file_path.open("r", encoding="utf-8") as file:
        logs = file.readlines()

    return logs


def count_failed_logins(logs: list[str]) -> int:
    """Count failed login attempts in the log entries."""

    failed_attempts = 0

    for log in logs:
        if "Failed password" in log:
            failed_attempts += 1

    return failed_attempts


def count_failed_logins_by_ip(logs: list[str]) -> dict[str, int]:
    """Count failed login attempts grouped by source IP."""

    failed_logins_by_ip = {}

    for log in logs:
        # Process only failed authentication events.
        if "Failed password" in log:
            parts = log.split()

            # Find the source IP after the word "from".
            if "from" in parts:
                from_index = parts.index("from")
                ip_address = parts[from_index + 1]

                # Add the IP to the dictionary or increment its count.
                if ip_address in failed_logins_by_ip:
                    failed_logins_by_ip[ip_address] += 1
                else:
                    failed_logins_by_ip[ip_address] = 1

    return failed_logins_by_ip

def detect_suspicious_ips(
        failed_logins_by_ip: dict[str, int],
        threshold: int = 3
) -> list[str]:
    """Identify IP addresses that exceed the failed login threshold"""

    suspicious_ips = []

    for ip_address, attempts in failed_logins_by_ip.items():
        if attempts >= threshold:
            suspicious_ips.append(ip_address)

    return suspicious_ips

def main() -> None:
    """Run the log analyzer."""

    logs = read_logs(LOG_FILE)

    failed_attempts = count_failed_logins(logs)

    # Store the result using a different name from the function.
    failed_logins_by_ip = count_failed_logins_by_ip(logs)

    suspicious_ips = detect_suspicious_ips(failed_logins_by_ip)

    print("=== ANALISADOR DE LOGS ===")
    print(f"Total de linhas analisadas: {len(logs)}")
    print(f"Tentativas de login malsucedidas: {failed_attempts}")

    print("\nFalhas de autenticação por IP:")

    for ip_address, attempts in failed_logins_by_ip.items():
        print(f"IP: {ip_address} | Tentativas: {attempts}")

    print("\nIPs suspeitos:")

    if suspicious_ips:
        for ip_address in suspicious_ips:
            print(f"ALERTA: {ip_address} atingiu o limite de tentativas.")
    else:
        print("Nenhum IP suspeito encontrado.")


# Run the main function when the script is executed directly.
if __name__ == "__main__":
    main()
