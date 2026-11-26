import pandas as pd
from datetime import date, timedelta
from faker import Faker
import random
import string
import csv

COLUMNS=[
        "order_id", "order_date", "customer_name", "customer_phone",
        "address_line", "landmark", "city", "state", "pincode",
        "payment_mode", "order_value", "rto", "rto_reason"
    ]

VAGUE_ADDRESSES = [
        "opp school",
        "near grocery shop",
        "beside hanuman temple",
        "beside block post banyan tree",
        "college block",
        "in front of hospital"
    ]

LANDMARKS = [
    "Near Central Railway Station",
    "Opposite City Bus Stand",
    "Near Main Post Office",
    "Behind District Court",
    "Near Government General Hospital",
    "Opposite Police Station",
    "Near Town Hall",
    "Near Clock Tower",
    "Near Gandhi Statue",
    "Opposite Municipal Corporation Office",
    "Near SBI Main Branch",
    "Near Hanuman Temple",
    "Near Shiva Temple",
    "Near Ganesh Temple",
    "Near Durga Temple",
    "Near Iskcon Temple",
    "Near Jama Masjid",
    "Near St. Mary's Church",
    "Near Gurudwara Sahib",
    "Near Jain Temple",
    "Near Apollo Hospital",
    "Near Fortis Hospital",
    "Near Manipal Hospital",
    "Near Metro Station Gate 1",
    "Near Metro Station Gate 2",
    "Near Railway Overbridge",
    "Near Bus Depot",
    "Opposite Petrol Pump",
    "Near Indian Oil Petrol Bunk",
    "Near HP Petrol Pump",
    "Near Bharat Petroleum Bunk",
    "Near Sub-Registrar Office",
    "Near RTO Office",
    "Near Electricity Board Office",
    "Near Water Tank",
    "Near Over Head Water Tank",
    "Near Fire Station",
    "Near Public Library",
    "Near Stadium Gate",
    "Near Cricket Stadium",
    "Near Indoor Stadium",
    "Near Central Mall",
    "Near Orion Mall",
    "Near Phoenix Marketcity",
    "Near Lulu Mall",
    "Near Forum Mall",
    "Near D-Mart",
    "Near Reliance Fresh",
    "Near More Supermarket",
    "Near Big Bazaar",
    "Near Vegetable Market",
    "Near Main Market",
    "Near Flower Market",
    "Near Fish Market",
    "Near Sabzi Mandi",
    "Near Grain Market",
    "Near Kendriya Vidyalaya",
    "Near Delhi Public School",
    "Near St. Joseph's School",
    "Near National Public School",
    "Near Government High School",
    "Near Engineering College",
    "Near Medical College",
    "Near University Main Gate",
    "Near Polytechnic College",
    "Near Industrial Estate",
    "Near IT Park",
    "Near Tech Park Main Gate",
    "Near Software Technology Park",
    "Near Airport Road Junction",
    "Near Highway Toll Plaza",
    "Near Ring Road Junction",
    "Near Bypass Junction",
    "Near Outer Ring Road",
    "Near MG Road Junction",
    "Near Station Road",
    "Near Temple Street",
    "Near Church Street",
    "Near Market Road",
    "Near Civil Lines",
    "Near Cantonment Area",
    "Near Circuit House",
    "Near Dak Bungalow",
    "Near PWD Guest House",
    "Near Youth Hostel",
    "Near Cinema Hall",
    "Near Multiplex",
    "Near Community Hall",
    "Near Marriage Hall",
    "Near Convention Centre",
    "Near Ambedkar Circle",
    "Near Subhash Chowk",
    "Near Nehru Chowk",
    "Near Patel Chowk",
    "Near Bhagat Singh Chowk",
    "Near Shivaji Circle",
    "Near Rajaji Nagar Circle",
    "Near Botanical Garden",
    "Near Children's Park",
    "Near Lake View Point"
]

AREAS = {
    "Mumbai": ["Andheri West", "Bandra East", "Powai", "Malad West", "Chembur"],
    "Bengaluru": ["Koramangala", "Indiranagar", "Whitefield", "HSR Layout", "Jayanagar"],
    "New Delhi": ["Connaught Place", "Hauz Khas", "Saket", "Dwarka", "Lajpat Nagar"],
    "Chennai": ["T. Nagar", "Adyar", "Anna Nagar", "Velachery", "OMR"],
    "Hyderabad": ["Banjara Hills", "Jubilee Hills", "Gachibowli", "HITEC City", "Madhapur"],
    "Kolkata": ["Salt Lake", "Park Street", "New Town", "Ballygunge", "Behala"],
    "Pune": ["Koregaon Park", "Hinjewadi", "Viman Nagar", "Kothrud", "Baner"],
    "Tiruppur": ["Avinashi Road", "Palladam Road", "Kumaran Road", "Kangeyam Road", "Perumanallur"]
}

CITY_MESSY = {
    "Bengaluru": ["blr", "bangalore", "BANGALORE", "Bengaluru "],
    "Mumbai": ["bombay", "MUMBAI", "mumbai "],
    "New Delhi": ["delhi", "New delhi", "new delhi"],
    "Chennai": ["madras", "chennai", "CHENNAI"],
    "Hyderabad": ["hyd", "HYDERABAD", "hyderabad"],
    "Kolkata": ["calcutta", "kolkata"],
    "Pune": ["pune ", "PUNE"],
    "Tiruppur": ["tirupur", "TIRUPPUR"],
}
STATE_MESSY = {
    "Karnataka": ["KA", "karnataka"],
    "Maharashtra": ["MH", "maharashtra"],
    "Delhi": ["DL", "delhi"],
    "Tamil Nadu": ["TN", "tamilnadu"],
    "Telangana": ["TS", "telangana"],
    "West Bengal": ["WB", "west bengal"],
}

VAGUE_ADDRESSES = [
        "opp school",
        "near grocery shop",
        "beside hanuman temple",
        "beside block post banyan tree",
        "college block",
        "in front of hospital"
    ]

def make_order_id(index: int):
    # unique 6 digit number
    return 100000 + index

def make_order_date():
    # random date in the last 2 months
    start_date=date(2026,9,14)
    end_date=date(2026,11,14)

    days_between= (end_date-start_date).days

    random_int = random.randint(0, days_between)
    random_date = start_date + timedelta(days=random_int)

    return random_date

def make_customer_name():
    # random customer name
    return fake.name()

def make_customer_phone(bad_phone, rand):
    # random customer phone number
    first_digit = random.choice(['6','7','8','9'])
    wrong_digit = random.choice(range(6))
    remaining_digits = ''.join(random.choices(string.digits, k=9))
    phone_number = first_digit+remaining_digits
    if bad_phone:
        phone_number = str(wrong_digit)+remaining_digits
    elif rand<0.10:
        phone_number = f"+91{phone_number}"
    elif rand<0.15:
        phone_number = f"0{phone_number}"
    elif rand<0.25:
        phone_number = f"{phone_number[:5]} {phone_number[5:]}"
    elif rand<0.30:
        phone_number = f"{phone_number[:5]}-{phone_number[5:]}"
    return phone_number

def make_address_line(vague):
    # random address line
    if not vague:
        return " ".join([fake.building_number(),fake.street_name()])
    else:
        return fake.random_element(elements=VAGUE_ADDRESSES)

def make_landmark(empty_landmark):
    # random landmark
    if not empty_landmark:
        return fake.random_element(elements=LANDMARKS)
    else:
        return ""

def random_row():
    i = random.randrange(len(df))
    return [str(df.iloc[i]["pincode"]), df.iloc[i]["city"], df.iloc[i]["state"]]

def make_bad_pin(pin):
    kind = random.choice(["empty", "short", "letter"])
    if kind == "empty":
        return ""
    if kind == "short":
        return pin[:5]                      # 5 digits
    return pin[:3] + "O" + pin[4:]          # letter O in place of a digit

def make_pin_city_state_combo(bad_pin, bad_city, mismatch):
    pin, city, state = random_row()

    if mismatch:
        while True:
            _, other_city, other_state = random_row()
            if other_city != city:
                break
        city, state = other_city, other_state

    area = pick_area(city)

    if bad_pin:
        pin = make_bad_pin(pin)

    if bad_city:
        city = random.choice(CITY_MESSY.get(city, [city.lower()]))
        state = random.choice(STATE_MESSY.get(state, [state.lower()]))

    return pin, city, state, area

def make_order_value():
    # choose a random value
    return fake.random_int(min=299, max=3499)

RISK_FLAGS= [
    ("repeat", "refused", 0.55),
    ("bad_pin", "address", 0.45),
    ("vague", "address", 0.35),
    ("bad_phone", "unreachable", 0.35),
    ("mismatch", "address", 0.25)
]

def pick_area(city: str)->str:
    if city in AREAS:
        return random.choice(AREAS[city])
    else:
        return ""

def check_for_rto(flags, payment_mode):
    score=0
    p=0
    for flag, reason, chance in RISK_FLAGS:
        if flag in flags:
            score+=chance
    if payment_mode=="COD":
        p=0.15 + score
    else:
        p=0.02 + 0.1 * score
    p = min(0.9,p)
    rand=random.random()
    if rand>p:
        return (False,"none")
    for flag, reason, chance in RISK_FLAGS:
        if flag in flags:
            return (True,reason)
    return (True,"refused")

def main():

    global df,fake
    df = pd.read_csv("data/pincodes.csv")
    Faker.seed(4321)
    fake = Faker('en_IN')
    random.seed(42)

    REPEAT_PHONES=[make_customer_phone(False, 0.9) for _ in range(0,10)]
    rows=[]

    for i in range(1000):
        hmap={}
        cod=True if random.random()<0.60 else False
        vague=True if random.random()<0.15 else False
        bad_pin=True if random.random()<0.10 else False
        mismatch=True if random.random()<0.06 else False
        bad_phone=True if random.random()<0.05 else False
        bad_city=True if random.random()<0.40 else False
        has_landmark=True if random.random()<0.70 else False
        repeat=True if random.random()<0.03 else False
        flags=set()
        for name, value in [("vague", vague), ("bad_pin", bad_pin), ("mismatch", mismatch),
                        ("bad_phone", bad_phone), ("repeat", repeat)]:
            if value:
                flags.add(name)
        phone= random.choice(REPEAT_PHONES) if repeat else make_customer_phone(bad_phone, random.random())
        pincode, city, state, area = make_pin_city_state_combo(bad_pin, bad_city, mismatch)
        payment_mode = "COD" if cod else "Prepaid"
        rto, rto_reason = check_for_rto(flags, payment_mode)
        order_id = make_order_id(i)
        order_date = make_order_date()
        customer_name=make_customer_name()
        if not vague:
            address_line=", ".join([make_address_line(vague),area])
        else:
            address_line=make_address_line(vague)
        landmark=make_landmark(not has_landmark)
        order_value=make_order_value()
        hmap["order_id"]=order_id
        hmap["order_date"]=order_date
        hmap["customer_name"]=customer_name
        hmap["address_line"]=address_line
        hmap["landmark"]=landmark
        hmap["customer_phone"]=phone
        hmap["pincode"]=pincode
        hmap["city"]=city
        hmap["state"]=state
        hmap["payment_mode"]=payment_mode
        hmap["rto"]=rto
        hmap["rto_reason"]=rto_reason
        hmap["order_value"]=order_value
        rows.append(hmap)

    with open("data/orders_synthetic.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f,fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
        
if __name__ == "__main__":
    main()