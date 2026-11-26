import pytest
from src.rules import normalise_phone, is_vague, clean_row, clean_house_number

def test_phone_strips_plus91():
    assert normalise_phone("+919876543210") == "9876543210"

def test_phone_strips_leading_zero():
    assert normalise_phone("09876543210") == "9876543210"

def test_phone_removes_spaces_and_dashes():
    assert normalise_phone("98765 43210") == "9876543210"
    assert normalise_phone("98765-43210") == "9876543210"

# One test function, run once per value in the list
@pytest.mark.parametrize("address", [
    "opp school", "near grocery shop", "beside hanuman temple",
    "beside block post banyan tree", "college block", "in front of hospital",
])
def test_planted_vague_addresses_are_flagged(address):
    assert is_vague(address)

# Regression test for the 25 Nov fix: short real addresses are NOT vague
@pytest.mark.parametrize("address", ["418 Ben, Saket", "52 Babu, Powai"])
def test_short_real_addresses_are_not_vague(address):
    assert not is_vague(address)

def test_clean_row_flags_bad_pincode():
    row = {"customer_phone": "9876543210", "city": "Mumbai", "state": "MH",
           "pincode": "4000", "address_line": "12 MG Road, Powai"}
    pincodes = {"400076": {"city": "Mumbai"}}
    assert "bad_pincode" in clean_row(row, pincodes)["issues"]
    
@pytest.mark.parametrize("raw, expected", [
    ("H.No. 932", "932"),
    ("House No. 12B", "12B"),
    ("h no 45", "45"),
    ("#17/3", "17/3"),
    ("070", "070"),
    ("74/161", "74/161"),
])
def test_clean_house_number(raw, expected):
    assert clean_house_number(raw) == expected