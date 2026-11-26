def normalise_name(name: str) -> str:
    return " ".join(name.split()).title()

def normalise_phone(s):
       # digits only; drop leading 91 (12 digits) or 0 (11 digits)
      cleaned = "".join(c for c in s if c.isdigit())
      if len(cleaned)==11 and cleaned.startswith("0"):
        return cleaned[1:]
      elif len(cleaned)==12 and cleaned.startswith("91"):
        return cleaned[2:]
      else:
        return cleaned

def normalise_city(s):
           # map bangalore/blr/bombay/delhi/madras/hyd/calcutta/tirupur
        city={"blr":"Bengaluru", "bangalore":"Bengaluru", "delhi": "New Delhi", "madras": "Chennai", "hyd": "Hyderabad"
, "tirupur": "Tiruppur", "calcutta": "Kolkata", "bombay": "Mumbai"}
        key = s.strip().lower()
        return city.get(key, key.title())

def normalise_state(s):
           # KA, MH, TN, TS, DL, WB → full names
        states={"ka":"Karnataka", "mh":"Maharashtra", "tn":"Tamil Nadu", "ts":"Telangana", "dl":"Delhi", "wb":"West Bengal",
                "tamilnadu": "Tamil Nadu"}
        return states.get(s.strip().lower(), s.title())


def is_valid_phone(p):
           # 10 digits, starts with 6–9
    return len(p)==10 and p[0] in "6789"

def is_vague(address):
    return not any(c.isdigit() for c in address)

def clean_row(row,pincodes)-> dict:
    cleaned_dict=row.copy()
    phone_clean = normalise_phone(row["customer_phone"])
    city_clean = normalise_city(row["city"])
    state_clean = normalise_state(row["state"])
    pincode_clean = "".join(ch for ch in row["pincode"] if ch.isalnum())
    cleaned_dict["phone_clean"]=phone_clean
    cleaned_dict["city_clean"]=city_clean
    cleaned_dict["state_clean"]=state_clean
    cleaned_dict["pincode_clean"]=pincode_clean
    issues=[]
    if not is_valid_phone(phone_clean):
        issues.append("invalid_phone")
    if len(cleaned_dict["pincode_clean"])!=6 or pincode_clean not in pincodes:
        issues.append("bad_pincode")
    elif pincodes[pincode_clean]["city"] != city_clean:
        issues.append("city_mismatch")
    if is_vague(row["address_line"]):
        issues.append("vague_address")
    cleaned_dict["issues"]=issues
    return cleaned_dict

def clean_house_number(s: str) -> str:
    s = s.strip()
    prefixes = ["house no.", "house no", "h.no.", "h.no", "h no", "#"]
    lower = s.lower()
    for pre in prefixes:
        if lower.startswith(pre):
            return s[len(pre):].strip()
    return s
    