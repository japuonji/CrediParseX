from .parser import parse_sms_file
from .matcher import load_tenants, reconcile_payments

# Load parsed payments
payments = parse_sms_file("data/sms_alerts.txt")

# Load tenants
tenants = load_tenants("data/tenants.csv")

# Reconcile
reconciled = reconcile_payments(payments, tenants)

# Print report
print("\n--- RECONCILIATION REPORT ---")
for r in reconciled:
    print(f"{r.get('house') or 'UNKNOWN'} - {r.get('tenant_name') or 'UNKNOWN'} : "
          f"{r['payment_type']} - KES {r['amount']} - MPESA Ref: {r.get('mpesa_ref')}")
