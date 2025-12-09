def calculate_risk(age, bmi, family_history, symptoms_count):
    risk_score = 0

    if age >= 45:
        risk_score += 1
    if bmi >= 25:
        risk_score += 1
    if family_history.lower() in ["parent", "sibling"]:
        risk_score += 1
    if symptoms_count >= 2:
        risk_score += 2
    
    if risk_score <= 1:
        return "Low Risk"
    elif risk_score == 2:
        return "Moderate Risk"
    else:
        return "High Risk — please take a glucose test"

if __name__ == "__main__":
    print("Here are the list of the symptoms:")
    print("- Feeling very thristy (polydipsia)")
    print("- Feeling very hungry (polyphagia)")
    print("- Urinating often, especially at night (polyuria)")
    print("- Extreme fatigue") 
    print("- Blurred vision")
    print("- Frequent infections")
    print("- Unexplained weight loss")
    print("- Slow-healing sores or cuts")
    print("- Numbness or tingling in the hands or feet")
    print("- Very dry skin")
    symptoms_count = int(input("Out of all the symptoms listed above, write the number of symptoms you have experienced: "))
    print(calculate_risk(45, 30, "Parent", symptoms_count))