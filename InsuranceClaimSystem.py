from datetime import datetime

class InsuranceClaimSystem:
    def __init__(self):
        # Default configuration for policy parameters
        self.policy_rules = {
            "Health": {"max_coverage": 50000.0, "deductible": 500.0, "copay_pct": 0.10},
            "Auto": {"max_coverage": 30000.0, "deductible": 1000.0, "copay_pct": 0.15},
            "Home": {"max_coverage": 150000.0, "deductible": 2500.0, "copay_pct": 0.20}
        }

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None

    def process_claim(self, policy_num, customer_id, policy_type, claim_amount, policy_start_date, incident_date, prev_claim_count, customer_age, incident_type, document_status):
        # 1. Base Validations
        if not policy_num or len(policy_num) < 3:
            return {"status": "REJECTED", "reason": "Invalid policy number"}
        
        if policy_type not in self.policy_rules:
            return {"status": "REJECTED", "reason": "Invalid policy type"}

        if claim_amount <= 0:
            return {"status": "REJECTED", "reason": "Invalid claim amount"}

        start_dt = self._parse_date(policy_start_date)
        incident_dt = self._parse_date(incident_date)
        if not start_dt or not incident_dt:
            return {"status": "REJECTED", "reason": "Invalid date format"}

        if incident_dt < start_dt:
            return {"status": "REJECTED", "reason": "Incident date is before policy start date"}

        rules = self.policy_rules[policy_type]
        
        # 2. Fraud Risk Assessment Scoring
        fraud_score = 0
        
        # Indicator A: Incident immediately after policy activation (within 7 days)
        days_since_activation = (incident_dt - start_dt).days
        if days_since_activation <= 7:
            fraud_score += 35

        # Indicator B: Claim amount significantly higher than max policy coverage
        if claim_amount > rules["max_coverage"]:
            fraud_score += 30

        # Indicator C: Missing documentation
        if document_status.upper() != "COMPLETE":
            fraud_score += 25

        # Indicator D: Multiple previous claims
        if prev_claim_count >= 5:
            fraud_score += 20
        elif prev_claim_count >= 3:
            fraud_score += 10

        # 3. Eligibility and Financial Calculations
        max_payable = rules["max_coverage"]
        deductible = rules["deductible"]
        
        if claim_amount <= deductible:
            insurance_payout = 0.0
            cust_contribution = claim_amount
        else:
            assessable_amount = min(claim_amount, max_payable) - deductible
            copay_amount = assessable_amount * rules["copay_pct"]
            insurance_payout = assessable_amount - copay_amount
            cust_contribution = deductible + copay_amount + max(0.0, claim_amount - max_payable)

        # 4. Status Classification Logic
        if fraud_score >= 60:
            status = "FRAUD SUSPECTED"
        elif document_status.upper() == "MISSING":
            status = "REJECTED"
        elif fraud_score >= 30 or claim_amount > max_payable:
            status = "MANUAL REVIEW"
        else:
            status = "APPROVED"

        return {
            "status": status,
            "fraud_risk_score": fraud_score,
            "financials": {
                "claim_amount": round(claim_amount, 2),
                "max_payable": round(max_payable, 2),
                "deductible": round(deductible, 2),
                "customer_contribution": round(cust_contribution, 2),
                "insurance_payout": round(insurance_payout, 2)
            }
        }
