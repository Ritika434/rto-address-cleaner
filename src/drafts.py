import csv
from collections import Counter
from src.rules import normalise_state,normalise_name

TEMPLATES = {
    "en": "Hi {first}, thanks for your order {order_id}! To deliver it on time, please share your {asks}. Just reply to this message.",
    "hi": "नमस्ते {first}, आपके ऑर्डर {order_id} के लिए धन्यवाद! समय पर डिलीवरी के लिए कृपया {asks} भेजें। बस इसी मैसेज का जवाब दें।",
}

PHRASES = {
    "en": {"house_number": "house/flat number", "street": "street or area name",
           "landmark": "nearest landmark", "city": "correct city",
           "pincode": "correct 6-digit pincode"},
    "hi": {"house_number": "मकान/फ्लैट नंबर", "street": "गली या इलाके का नाम",
           "landmark": "पास का कोई लैंडमार्क", "city": "सही शहर का नाम",
           "pincode": "सही 6 अंकों का पिनकोड"},
}

JOINERS = {"en": "and", "hi": "और"}

HINDI_STATES=["Uttar Pradesh", "Bihar",
                  "Madhya Pradesh",
                  "Rajasthan",
                  "Haryana",
                  "Delhi",
                  "Jharkhand",
                  "Chhattisgarh",
                  "Uttarakhand",
                  "Himachal Pradesh"]

def build_drafts(in_path: str, out_draft_path: str, out_other_way_path:str) -> None:
    all_rows=[]
    with open(in_path,"r",encoding="utf-8") as f:
        rows=csv.DictReader(f)
        filtered=[]
        for row in rows:
            all_rows.append(row)
            if row["normalised_by"]=="llm":
                filtered.append(row)
    drafts=[]
    other_way=[]
    seen=set()
    for row in all_rows:
        asks=fields_to_ask(row)
        if "invalid_phone" in row["issues"].split(";"):
                hmap={
                    "order_id":row["order_id"],
                    "customer_phone":row["customer_phone"],
                    "asks":";".join(asks),
                    "reason":"invalid_phone"
                }
                seen.add(row["order_id"])
                other_way.append(hmap)
    for row in filtered:
        asks=fields_to_ask(row)
        if asks and row["order_id"] not in seen:
                lang=pick_language(row)
                message=draft_message(normalise_name(row["customer_name"]),row["order_id"],asks,lang)
                hmap={
                "order_id":row["order_id"],
                "phone":row["phone_clean"],
                "asks":";".join(asks),
                "lang":lang,
                "message":message
            }
                drafts.append(hmap)
    with open(out_draft_path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["order_id", "phone", "lang", "asks", "message"])
        w.writeheader()
        w.writerows(drafts)
    with open(out_other_way_path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["order_id", "customer_phone", "asks", "reason"])
        w.writeheader()
        w.writerows(other_way)
    print(len(drafts))
    print(len(other_way))
    print(Counter(d["lang"] for d in drafts))
    all_asks = Counter(a for d in drafts for a in d["asks"].split(";"))
    print("top asks:", all_asks.most_common(3))


def check_pincode_city_in_issues(issues):
    flags=issues.split(";")
    pincode=False
    city=False
    if "bad_pincode" in flags:
        pincode=True
    if "city_mismatch" in flags:
        city=True
    return city,pincode

def fields_to_ask(row:dict)->list[str]:
    result=[]
    ask_house_number = row["house_number"]=="" or row["house_number"]=="None"
    ask_street = row["street"]=="" or row["street"]=="None"
    ask_landmark= row["landmark"]=="" or row["landmark"]=="None"
    ask_city, ask_pincode= check_pincode_city_in_issues(row["issues"])
    if ask_house_number:
        result.append("house_number")
    if ask_street:
        result.append("street")
    if ask_landmark:
        result.append("landmark")
    if ask_city:
        result.append("city")
    if ask_pincode:
        result.append("pincode")
    return result

def join_items(items: list[str], word: str) -> str:
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f" {word} " + items[-1]

def draft_message(name: str, order_id: str, asks: list[str], lang: str) -> str:
    if not asks:
        return ""
    first = name.split()[0]
    phrases = [PHRASES[lang][a] for a in asks]
    return TEMPLATES[lang].format(first=first, order_id=order_id,
                                  asks=join_items(phrases, JOINERS[lang]))

def pick_language(row: dict) -> str:
    if normalise_state(row["state"]) in HINDI_STATES:
        return "hi"
    return "en"

def main():

    build_drafts("data/cleaned_orders_v0.csv",
                "data/drafts.csv","data/otherway.csv")
        
if __name__ == "__main__": main()
