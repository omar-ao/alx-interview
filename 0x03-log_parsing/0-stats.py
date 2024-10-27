#!/usr/bin/python3
""" This is the stats module
"""

import sys
import re
import signal
from collections import defaultdict
from typing import Dict

# Global variables to store metrics
total_size: int = 0
status_counts: Dict[str, int] = defaultdict(int)
line_count: int = 0

def signal_handler(sig: int, frame) -> None:
    """Handle the SIGINT signal for graceful termination."""
    print_metrics()
    sys.exit(0)

def main() -> None:
    global total_size, status_counts, line_count

    # Register the signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    # Regular expression to match the log line format
    log_pattern: re.Pattern = re.compile(
        r'^(?P<ip>[\d\.]+) - \[(?P<date>[^\]]+)\] '
        r'"(?P<method>GET) (?P<url>\/projects\/\d+) HTTP\/1\.1" '
        r'(?P<status>\d{3}) (?P<size>\d+)$'
    )

    try:
        for line in sys.stdin:
            line = line.strip()
            match = log_pattern.match(line)

            if match:
                status_code: str = match.group('status')
                file_size: int = int(match.group('size'))

                # Update metrics
                total_size += file_size
                status_counts[status_code] += 1
                line_count += 1

                # Print metrics after every 10 lines
                if line_count % 10 == 0:
                    print_metrics()

        # Print final metrics if EOF is reached
        if line_count > 0:
            print_metrics()

    except Exception as e:
        print(f"An error occurred: {e}")

def print_metrics() -> None:
    """Print the current metrics."""
    print(f"File size: {total_size}")

    # Sort and print status codes
    for status in sorted(status_counts.keys()):
        print(f"{status}: {status_counts[status]}")

if __name__ == "__main__":
    main()

