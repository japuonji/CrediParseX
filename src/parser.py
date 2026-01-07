import re
from typing import Optional, Dict, List


def parse_mpesa_sms(line: str) -> Optional[Dict]:
    """
    Parse an MPESA-style bank SMS alert.
    Returns structured data or None if parsing fails.
    """

    pattern = (
        r"received a credit of KES\s+([\d,]+(?:\.\d{2})?)\s+"
        r"from\s+(.+?)\s+"
        r"for account\s+([A-Z0-9\-]+)\s+"
        r"at\s+(.+?)\.\s*MPESA Ref\s+([A-Z0-9]+)"
    )

    match = re.search(pattern, line)

    if not match:
        return None

    amount_raw, payer, account, date, mpesa_ref = match.groups()

    return {
        "payer": payer.strip(),
        "amount": int(float(amount_raw.replace(",", ""))),
        "account": account.strip(),
        "date": date.strip(),
        "mpesa_ref": mpesa_ref.strip(),
        "raw_message": line.strip()
    }


def parse_sms_file(path: str) -> List[Dict]:
    """
    Parse all SMS alerts from a file.
    """

    parsed = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            data = parse_mpesa_sms(line)
            if data:
                parsed.append(data)
            else:
                print(f"[WARN] Failed to parse line:\n{line}\n")

    return parsed


if __name__ == "__main__":
    sms_data = parse_sms_file("../data/sms_alerts.txt")

    print("\n--- PARSED PAYMENTS ---")
    for item in sms_data:
        print(item)
