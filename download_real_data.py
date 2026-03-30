import pandas as pd
import urllib.request
import os

def download_real_dataset():
    print("=========================================================")
    print("Initiating Download: Official UCI Online Retail Dataset")
    print("=========================================================")
    print("This is the industry-standard 'Real World' dataset for E-commerce RFM/CLV model testing before production.")
    print("It contains over 540,000 real rows from a registered non-store online retail company based in the UK.\n")
    
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    file_path = "Online_Retail.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Downloading 23MB Excel file from {url}...")
        urllib.request.urlretrieve(url, file_path)
        print("Download complete.")
    else:
        print("File already found locally. Skipping download.")
        
    print("Reading real data into Pandas Engine (this takes ~10 seconds)...")
    df = pd.read_excel(file_path)
    
    print("Mapping real-world headers safely to Consumer360 Schema...")
    # The actual UCI dataset natively maps exactly to our schema concept
    df.rename(columns={
        'InvoiceNo': 'invoice_no',
        'StockCode': 'stock_code',
        'Description': 'description',
        'Quantity': 'quantity',
        'InvoiceDate': 'invoice_date',
        'UnitPrice': 'unit_price',
        'CustomerID': 'customer_id',
        'Country': 'country'
    }, inplace=True)
    
    output_path = "raw_transaction_logs.csv"
    print(f"Exporting to '{output_path}'...")
    df.to_csv(output_path, index=False)
    
    # Optional cleanup of the large excel file to save space
    if os.path.exists(file_path):
        os.remove(file_path)
        
    print("\n✅ Success!")
    print(f"Completely replaced the synthetic mock data with {len(df):,} absolutely authentic real-world transactions.")
    print("The system is now completely staging a Production environment.")

if __name__ == "__main__":
    download_real_dataset()
