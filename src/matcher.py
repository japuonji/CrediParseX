import csv
from typing import List, Dict

def load_tenants(csv_path: str) -> List[Dict]:
    tenants = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["expected_rent"] = float(row["expected_rent"])
            tenants.append(row)
    return tenants


def match_payment_to_tenant(payment: Dict, tenants: List[Dict]) -> Dict:
    """
    Match a payment to a tenant.
    Returns a dictionary with match info.
    """

    # First, try matching by reference/account
    for tenant in tenants:
        if payment.get("account") and payment["account"].upper() == tenant["reference"].upper():
            return {
                **payment,
                "tenant_id": tenant["tenant_id"],
                "tenant_name": tenant["name"],
                "house": tenant["house"],
                "expected_rent": tenant["expected_rent"],
                "status": "MATCHED"
            }

    # Second, try matching by payer name (case-insensitive, partial)
    payer = payment.get("payer", "").upper()
    for tenant in tenants:
        if tenant["name"].upper() in payer:
            return {
                **payment,
                "tenant_id": tenant["tenant_id"],
                "tenant_name": tenant["name"],
                "house": tenant["house"],
                "expected_rent": tenant["expected_rent"],
                "status": "MATCHED"
            }

    # If no match, mark unknown
    return {
        **payment,
        "tenant_id": None,
        "tenant_name": None,
        "house": None,
        "expected_rent": None,
        "status": "UNKNOWN"
    }


def reconcile_payments(payments: List[Dict], tenants: List[Dict]) -> List[Dict]:
    """
    Reconcile a list of payments against tenants.
    Also detects partial/full payments.
    """

    results = []
    for payment in payments:
        matched = match_payment_to_tenant(payment, tenants)
        expected = matched.get("expected_rent")

        # Detect partial or full payment
        if matched["status"] == "MATCHED":
            if payment["amount"] >= expected:
                matched["payment_type"] = "FULL"
            else:
                matched["payment_type"] = "PARTIAL"
        else:
            matched["payment_type"] = "UNKNOWN"

        results.append(matched)

    return results
