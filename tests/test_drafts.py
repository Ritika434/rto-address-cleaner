from src.drafts import fields_to_ask, draft_message, join_items

def test_fields_to_ask_missing_house_and_landmark():
    r1 = {"house_number": "", "street": "MG Road", "landmark": "None", "issues": ""}
    assert fields_to_ask(r1) == ["house_number", "landmark"]

def test_fields_to_ask_city_mismatch():
    r = {"house_number": "123", "street": "MG Road", "landmark": "near St.Xaviers", "issues": ""}
    r2 = {**r, "issues": "city_mismatch;bad_pincode"}
    assert fields_to_ask(r2) == ["city", "pincode"]

def test_draft_message_empty_asks_returns_empty():
    assert draft_message("Priya Sharma", "ORD001", [], "en") == ""

def test_draft_message_hindi():
    assert draft_message("Anita Devi", "ORD003", ["house_number", "street", "landmark"], "hi") == \
  "नमस्ते Anita, आपके ऑर्डर ORD003 के लिए धन्यवाद! समय पर डिलीवरी के लिए कृपया मकान/फ्लैट नंबर, गली या इलाके का नाम और पास का कोई लैंडमार्क भेजें। बस इसी मैसेज का जवाब दें।"

def test_join_items_three():
    assert join_items(["a", "b", "c"], "और") == "a, b और c"