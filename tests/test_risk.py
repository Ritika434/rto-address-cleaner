from src.risk import risk_score, risk_band
import pytest

def test_risk_score():
    assert risk_score({"payment_mode": "Prepaid", "issues": ""}, False) == pytest.approx(0.02)
    assert risk_score({"payment_mode": "COD", "issues": "bad_pincode;vague_address"}, False) == pytest.approx(0.70)
    assert risk_score({"payment_mode": "COD", "issues": "bad_pincode;vague_address;invalid_phone;city_mismatch"}, True) == pytest.approx(1.0)

def test_risk_band():
    assert risk_band(0.02) == "low"
    assert risk_band(0.2) == "medium"
    assert risk_band(0.49) == "medium"
    assert risk_band(0.5) == "high"
    assert risk_band(0.9, high=0.95) == "medium"
