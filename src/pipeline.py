from collections import Counter
import csv
from src.rules import clean_row, clean_house_number
from src.llm import call_llm, make_batches, batch_to_payload, load_cache, save_cache, route, TOKENS
import time
import json


def main():
    with open("data/orders_synthetic.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open("data/pincodes.csv", encoding="utf-8") as f:
        pincodes = {r["pincode"]: r for r in csv.DictReader(f)}
    cleaned = [clean_row(r, pincodes) for r in rows]

    assert len(cleaned) == 1000
    print(Counter(i for c in cleaned for i in c["issues"]))
    print(sum(1 for c in cleaned if not c["issues"]), "rows fully clean by rules")

    for c in cleaned:
        c["route"] = route(c)

    llm_rows = [c for c in cleaned if c["route"] == "llm"]
    rule_rows = [c for c in cleaned if c["route"] == "rules"]

    assert len(llm_rows) + len(rule_rows) == 1000
    assert all({"vague_address", "bad_pincode"} & set(c["issues"]) for c in llm_rows)
    assert not any({"vague_address", "bad_pincode"} & set(c["issues"]) for c in rule_rows)

    print(f"Rules alone handled {len(rule_rows) / 10:.1f}% of orders")
    print(len(llm_rows), "rows need the LLM")
    cache = load_cache("data/llm_cache.json")
    batched_rows=make_batches(llm_rows)
    for batch in batched_rows:
        todo=[]
        for row in batch:
            if row["order_id"] not in cache:
                todo.append(row)
        if not todo:
            continue
        results = call_llm(batch_to_payload(todo))
        sent=set(r["order_id"] for r in todo)
        got=set(g.order_id for g in results)
        missing=set(sent-got)
        print(missing)
        for result in results:
            if result.order_id in sent:
                cache[result.order_id]=result.model_dump()
        save_cache(cache, "data/llm_cache.json")
        time.sleep(6)

    print(len(cache), "cached")
    print(TOKENS)
    with open("data/tokens.json", "w") as f:
        json.dump(TOKENS, f)
    print(json.dumps(list(cache.values())[:3], indent=2))

    COLUMNS = [
        # the 13 originals
        "order_id", "order_date", "customer_name", "customer_phone",
        "address_line", "landmark", "city", "state", "pincode",
        "payment_mode", "order_value", "rto", "rto_reason",
        # the rules pass
        "phone_clean", "city_clean", "state_clean", "pincode_clean",
        "issues", "normalised_by",
        # the LLM pass (empty for rules rows)
        "house_number", "building", "street", "area",
        "llm_landmark", "pincode_in_text", "address_complete", "missing",
    ]

    with open("data/cleaned_orders_v0.csv","w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for row in cleaned:
            new_row=row.copy()
            new_row["issues"]=";".join(new_row["issues"])
            new_row["normalised_by"] = row["route"]
            new_row.pop("route")
            if new_row["normalised_by"] == "llm":
                llm = cache[new_row["order_id"]]
                new_row["llm_landmark"]=llm["landmark"]
                new_row["address_complete"]=llm["complete"]
                new_row["missing"]=";".join(llm["missing"])
                new_row["house_number"]=clean_house_number(llm["house_number"])
                new_row["building"]=llm["building"]
                new_row["street"]=llm["street"]
                new_row["area"]=llm["area"]
                new_row["pincode_in_text"]=llm["pincode_in_text"]
            else:
                new_row["llm_landmark"]=""
                new_row["address_complete"]=True
                new_row["missing"]=""
                new_row["house_number"]=""
                new_row["building"]=""
                new_row["street"]=""
                new_row["area"]=""
                new_row["pincode_in_text"]=""
            w.writerow(new_row)

if __name__ == "__main__":
    main()