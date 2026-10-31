"""Check which TLS versions a server actually negotiates.

Usage: python3 main.py example.com 443
Tries TLS 1.3, 1.2, 1.1 and 1.0 in turn with a context locked to that
version. Grade: A (TLS 1.3), B (1.2 only), C (older versions accepted),
F (nothing negotiated).
"""
import argparse
import socket
import ssl
import sys

VERSIONS = []
for name, value in (("TLSv1.3", ssl.TLSVersion.TLSv1_3), ("TLSv1.2", ssl.TLSVersion.TLSv1_2),
                    ("TLSv1.1", ssl.TLSVersion.TLSv1_1), ("TLSv1", ssl.TLSVersion.TLSv1)):
    VERSIONS.append((name, value))


def probe(host, port, timeout=5.0):
    results = {}
    for name, version in VERSIONS:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.minimum_version = version
            context.maximum_version = version
            with socket.create_connection((host, port), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host):
                    results[name] = "supported"
        except ssl.SSLError:
            results[name] = "rejected"
        except (OSError, ValueError):
            results[name] = "error"
    return results


def grade(results):
    supported = [name for name, state in results.items() if state == "supported"]
    if "TLSv1.3" in supported:
        return "A"
    if supported == ["TLSv1.2"]:
        return "B"
    if supported:
        return "C"
    return "F"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    args = parser.parse_args(argv)
    results = probe(args.host, args.port)
    for name, _ in VERSIONS:
        print(f"{name}: {results[name]}")
    print(f"Grade: {grade(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
