
from log_analyzer import (
    count_failed_logins,
    count_failed_logins_by_ip,
    detect_suspicious_ips,
    read_logs,
)


def test_count_failed_logins():
    logs = [
        "Failed password for admin from 192.168.1.50 port 22 ssh2",
        "Accepted password for user from 192.168.1.20 port 22 ssh2",
        "Failed password for root from 10.0.0.15 port 22 ssh2",
    ]

    result = count_failed_logins(logs)

    assert result == 2


def test_count_failed_logins_by_ip():
    logs = [
        "Failed password for admin from 192.168.1.50 port 22 ssh2",
        "Failed password for root from 192.168.1.50 port 22 ssh2",
        "Failed password for user from 10.0.0.15 port 22 ssh2",
    ]

    result = count_failed_logins_by_ip(logs)

    assert result == {
        "192.168.1.50": 2,
        "10.0.0.15": 1,
    }


def test_detect_suspicious_ips():
    failed_logins_by_ip = {
        "192.168.1.50": 3,
        "10.0.0.15": 1,
    }

    result = detect_suspicious_ips(failed_logins_by_ip)

    assert result == ["192.168.1.50"]


def test_detect_suspicious_ips_custom_threshold():
    failed_logins_by_ip = {
        "192.168.1.50": 2,
        "10.0.0.15": 1,
    }

    result = detect_suspicious_ips(
        failed_logins_by_ip,
        threshold=2,
    )

    assert result == ["192.168.1.50"]


def test_read_logs(tmp_path):
    log_file = tmp_path / "auth.log"

    log_file.write_text(
        "Failed password for admin from 192.168.1.50 port 22 ssh2\n",
        encoding="utf-8",
    )

    result = read_logs(log_file)

    assert len(result) == 1
    assert "Failed password" in result[0]
