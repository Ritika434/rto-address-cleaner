from src.llm import make_batches, batch_to_payload

def test_make_batches_45_rows():
    rows = [{"order_id": str(i)} for i in range(45)]
    assert len(make_batches(rows))==3
    assert [len(b) for b in make_batches(rows)] == [20, 20, 5]

def test_payload_is_wrapped_in_orders_tags():
    row=[{
        "order_id":1,
        "address_line":"123 Malviya marg",
        "landmark":"Near Kalyani Temple",
        "city_clean":"Mumbai",
        "pincode_clean":"400001"
    }]
    payload = batch_to_payload(row)

    assert payload.startswith("<orders>")
    assert payload.endswith("</orders>")
    assert "Mumbai" in payload            
    assert "city_clean" not in payload 
    