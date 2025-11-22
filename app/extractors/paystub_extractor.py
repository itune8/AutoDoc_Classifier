import re
from typing import Any, Dict


def extract_pay_stub_fields(text: str) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    employer_match = re.search(r"EMPLOYER NAME/ADDRESS:\s*(.+)", text, re.IGNORECASE)
    if employer_match:
        fields["employer"] = employer_match.group(1).strip()

    employee_match = re.search(r"EMPLOYEE NAME/ADDRESS:\s*([\w\s,]+)", text, re.IGNORECASE)
    if employee_match:
        fields["employee"] = employee_match.group(1).strip()

    payroll_id_match = re.search(r"Payroll ID:\s*([0-9A-Za-z-]+)", text, re.IGNORECASE)
    if payroll_id_match:
        fields["payroll_id"] = payroll_id_match.group(1).strip()

    cycle_match = re.search(r"Cycle:\s*([0-9\-]+\s*-\s*[0-9\-]+)", text, re.IGNORECASE)
    if cycle_match:
        fields["cycle"] = cycle_match.group(1).strip()

    pay_rate_match = re.search(r"Pay Rate:\s*([$0-9,./yr]+)", text, re.IGNORECASE)
    if pay_rate_match:
        fields["pay_rate"] = pay_rate_match.group(1).strip()

    pay_date_match = re.search(r"Pay Date:\s*([0-9\-]+)", text, re.IGNORECASE)
    if pay_date_match:
        fields["pay_date"] = pay_date_match.group(1).strip()

    gross_pay_match = re.search(r"GROSS PAY\s*\n\s*([0-9.,$]+)", text, re.IGNORECASE)
    if gross_pay_match:
        fields["gross_pay"] = gross_pay_match.group(1).strip()

    net_pay_match = re.search(r"NET PAY\s*\n\s*([0-9.,$]+)", text, re.IGNORECASE)
    if net_pay_match:
        fields["net_pay"] = net_pay_match.group(1).strip()

    return fields
