from collections import Counter
import csv

WEIGHTS = {"bad_pincode": 0.30, "vague_address": 0.25,
           "invalid_phone": 0.25, "city_mismatch": 0.15}

def risk_score(row: dict, is_repeat: bool) -> float:
    score=0
    if row["payment_mode"]=="COD":
        score+=0.15
    else:
        score+=0.02
    issues=row["issues"].split(";")
    for issue in issues:
        score += WEIGHTS.get(issue, 0)
    if is_repeat:
        score+=0.35
    score=min(score,1.0)
    return score

def risk_band(score: float, high: float = 0.5, low: float = 0.2) -> str:
    if score>=high:
        return "high"
    elif score>=low:
        return "medium"
    else:
        return "low"

def evaluate(all_rows, threshold):
    phone_counts=Counter(r["phone_clean"] for r in all_rows if r["phone_clean"]!="")
    for row in all_rows:
        is_repeat=phone_counts[row["phone_clean"]]>1
        row["score"]=risk_score(row, is_repeat)
        row["band"]=risk_band(row["score"],high=threshold)
    print(Counter(r["band"] for r in all_rows))
    TP=0
    FP=0
    TN=0
    FN=0
    for row in all_rows:
        predicted=row["band"] == "high"
        actual=row["rto"] == "True"
        if actual and predicted==actual:
            TP+=1
        if not actual and predicted==actual:
            TN+=1
        if actual and predicted!=actual:
            FN+=1
        if not actual and predicted!=actual:
            FP+=1

    total = len(all_rows)
    print("TP", TP, "FP", FP, "FN", FN, "TN", TN)
    print("RTO base rate:", round((TP + FN) / total * 100, 1), "%")
    print("Precision:", round(TP / (TP + FP) * 100, 1) if TP + FP else "n/a", "%")
    print("Recall:", round(TP / (TP + FN) * 100, 1) if TP + FN else "n/a", "%")
    print("Accuracy:", round((TP + TN) / total * 100, 1), "%")

def main():
    all_rows=[]
    with open("data/cleaned_orders_v0.csv", "r", encoding="utf-8") as f:
        reader=csv.DictReader(f)
        for row in reader:
            all_rows.append(row)
    for high in [0.15, 0.2, 0.25, 0.3, 0.4, 0.5]:
        evaluate(all_rows,high)
        
if __name__=="__main__":
    main()
