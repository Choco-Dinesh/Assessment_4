from InsuranceClaim import InsuranceClaimSystem

def run_tests():
    engine = InsuranceClaimSystem()

    # 1. Valid claim test
    res1 = engine.process_claim("POL123", "C01", "Auto", 5000.0, "2026-01-01", "2026-06-01", 0, 35, "Collision", "COMPLETE")
    print("Valid Claim Test Passed:", res1["status"] == "APPROVED" and res1["financials"]["insurance_payout"] == 3400.0)

    # 2. Claim before policy start test
    res2 = engine.process_claim("POL123", "C01", "Auto", 5000.0, "2026-06-01", "2026-01-01", 0, 35, "Collision", "COMPLETE")
    print("Claim Before Policy Start Test Passed:", res2["status"] == "REJECTED" and "before policy start" in res2["reason"])

    # 3. Excessive claim amount test
    res3 = engine.process_claim("POL124", "C02", "Auto", 40000.0, "2026-01-01", "2026-06-01", 1, 42, "Theft", "COMPLETE")
    print("Excessive Claim Amount Test Passed:", res3["status"] == "MANUAL REVIEW" and res3["fraud_risk_score"] == 30)

    # 4. Missing documents test
    res4 = engine.process_claim("POL125", "C03", "Health", 2000.0, "2026-01-01", "2026-05-01", 0, 28, "Illness", "MISSING")
    print("Missing Documents Test Passed:", res4["status"] == "REJECTED")

    # 5. Multiple previous claims test
    res5 = engine.process_claim("POL126", "C04", "Home", 10000.0, "2026-01-01", "2026-08-01", 4, 50, "Water", "COMPLETE")
    print("Multiple Previous Claims Test Passed:", res5["fraud_risk_score"] == 10)

    # 6. Fraud scenario test (Immediate incident + missing files + high history)
    res6 = engine.process_claim("POL127", "C05", "Health", 60000.0, "2026-08-10", "2026-08-12", 6, 61, "Injury", "INCOMPLETE")
    print("Fraud Scenario Test Passed:", res6["status"] == "FRAUD SUSPECTED" and res6["fraud_risk_score"] == 110)

    # 7. Boundary claim amount test (Claim exactly equal to deductible boundary)
    res7 = engine.process_claim("POL128", "C06", "Auto", 1000.0, "2026-01-01", "2026-04-01", 0, 22, "FenderBender", "COMPLETE")
    print("Boundary Claim Amount Test Passed:", res7["financials"]["insurance_payout"] == 0.0)

    # 8. Invalid policy number test
    res8 = engine.process_claim("", "C07", "Auto", 5000.0, "2026-01-01", "2026-04-01", 0, 30, "Collision", "COMPLETE")
    print("Invalid Policy Number Test Passed:", res8["status"] == "REJECTED" and "policy number" in res8["reason"])

    # 9. Invalid incident date test
    res9 = engine.process_claim("POL129", "C08", "Auto", 5000.0, "2026-01-01", "2026-INVALID-DATE", 0, 30, "Collision", "COMPLETE")
    print("Invalid Incident Date Test Passed:", res9["status"] == "REJECTED")

if __name__ == "__main__":
    run_tests()

