import re

SYSTEM_PROMPT = """
You are ZENVY, an AI Payroll Copilot.

Rules:
- Use ONLY provided payroll, policy, and tax data.
- Never guess numbers.
- Redact PAN, Aadhaar, Bank Account details.
- Explain deductions legally and ethically.
- If information is missing, say:
  "I don’t have access to that information."
"""

ROLE_PROMPTS = {
    "employee": """
Tone: Simple and reassuring
Explain payroll clearly
Do NOT reveal internal HR or analytics data
""",
    "hr": """
Tone: Professional and compliance-focused
Include legal and policy references
Show only aggregated or anonymized data
"""
}

PAYROLL_DATA = {
    "employee_id": "EMP101",
    "gross_salary": 60000,
    "pf": 7200,
    "professional_tax": 200,
    "bonus": 10000,
    "net_salary": 52600
}

POLICIES = {
    "pf": "Provident Fund is mandatory under EPF Act.",
    "professional_tax": "State-mandated deduction.",
    "bonus": "Bonus is taxable as per Income Tax Act."
}

TAX_RULES = {
    "income_tax": "Calculated annually based on slabs.",
    "gratuity": "Applicable after 5 years of service."
}

def redact_sensitive_data(text):
    patterns = [
        r"[A-Z]{5}[0-9]{4}[A-Z]",
        r"\b\d{12}\b",
        r"\b\d{9,18}\b"
    ]
    for pattern in patterns:
        text = re.sub(pattern, "XXXX_REDACTED", text)
    return text

def verify_context(data):
    return bool(data)

def generate_response(role, question):
    if not verify_context(PAYROLL_DATA):
        return "I don’t have access to that information."

    q = question.lower()

    if role == "employee":
        if "net salary" in q or "less" in q:
            response = (
                "Your net salary is lower due to statutory deductions like "
                "Provident Fund and Professional Tax. These are legally required."
            )
        elif "pf" in q:
            response = (
                "Provident Fund is a mandatory retirement contribution under the EPF Act. "
                "Both you and your employer contribute."
            )
        elif "bonus" in q:
            response = (
                "Yes, bonuses are taxable and added to your gross income as per income tax laws."
            )
        else:
            response = "I don’t have access to that information."

    elif role == "hr":
        if "payroll cost" in q:
            response = (
                "Payroll costs increased due to bonus payouts and statutory tax recalculations."
            )
        elif "tax slab" in q:
            response = (
                "Several employees crossed tax slabs this quarter. "
                "Individual salary data is not disclosed."
            )
        elif "gratuity" in q:
            response = (
                "Gratuity applies after 5 years of continuous service "
                "as per the Payment of Gratuity Act."
            )
        else:
            response = "I don’t have access to that information."
    else:
        response = "Invalid role."

    return redact_sensitive_data(response)

def zenvy_chat(role, question):
    role = role.lower()
    if role not in ROLE_PROMPTS:
        return "Invalid role. Allowed roles: employee, hr."

    print("\n--- ZENVY AI PAYROLL COPILOT ---")
    print(SYSTEM_PROMPT)
    print(ROLE_PROMPTS[role])

    answer = generate_response(role, question)
    return f"\nQ: {question}\nA: {answer}"

if __name__ == "__main__":
    print(zenvy_chat("employee", "Why is my net salary less this month?"))
    print(zenvy_chat("employee", "Is my bonus taxable?"))
    print(zenvy_chat("hr", "Why did payroll cost increase this month?"))
