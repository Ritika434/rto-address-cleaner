import csv
from src.generate import VAGUE_ADDRESSES

def check_for_vague_address(in_path:str):
    all_rows=[]
    with open(in_path,"r",encoding="utf-8") as f:
        rows=csv.DictReader(f)
        for row in rows:
            all_rows.append(row)
    for row in all_rows:
        if "vague_address" in row["issues"].split(";") and row["address_line"] not in VAGUE_ADDRESSES:
            print(row["order_id"], row["address_line"], len(row["address_line"]))
            
def check_copied_pincodes(in_path:str):
    llm_rows=[]
    count=0
    with open(in_path,"r",encoding="utf-8") as f:
        rows=csv.DictReader(f)
        for row in rows:
            if row["normalised_by"]=="llm":
                llm_rows.append(row)
    for row in llm_rows:
        val=row["pincode_in_text"]
        address=row["address_line"] + " " + row["landmark"]
        if val and val not in address:
            count+=1
            print(row["order_id"], row["address_line"], row["landmark"], row["pincode"], row["pincode_in_text"])
    print(count)

def main():
    check_for_vague_address("data/cleaned_orders_v0.csv")
    check_copied_pincodes("data/cleaned_orders_v0.csv")

if __name__=="__main__":
    main()