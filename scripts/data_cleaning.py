# scripts/data_cleaning.py
import pandas as pd
import os

def clean_data():
    raw_path = "data/raw/"
    processed_path = "data/processed/"
    
    # Processed klasörü yoksa oluştur
    if not os.path.exists(processed_path):
        os.makedirs(processed_path)
        
    print("Veri temizleme işlemi başlıyor...")

    # 1. ORDERS TEMİZLİĞİ
    df_orders = pd.read_csv(os.path.join(raw_path, 'olist_orders_dataset.csv'))
    
    # Tarih kolonlarını string'den datetime formatına çevirme
    date_columns = ['order_purchase_timestamp', 'order_approved_at', 
                    'order_delivered_carrier_date', 'order_delivered_customer_date', 
                    'order_estimated_delivery_date']
    
    for col in date_columns:
        df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')
        
    df_orders.to_csv(os.path.join(processed_path, 'cleaned_orders.csv'), index=False)
    print("✓ Orders tablosu temizlendi (Tarih formatları düzeltildi).")

    # 2. PRODUCTS TEMİZLİĞİ
    df_products = pd.read_csv(os.path.join(raw_path, 'olist_products_dataset.csv'))
    
    # Eksik kategorileri 'Unknown' ile doldurma
    df_products['product_category_name'] = df_products['product_category_name'].fillna('Unknown')
    
    # Kalan sayısal eksiklikleri (2 satır) 0 ile doldurma
    numeric_cols = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 
                    'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
    for col in numeric_cols:
        df_products[col] = df_products[col].fillna(0)
        
    df_products.to_csv(os.path.join(processed_path, 'cleaned_products.csv'), index=False)
    print("✓ Products tablosu temizlendi (Eksik kategoriler dolduruldu).")

    # 3. CUSTOMERS ve PAYMENTS (Temiz oldukları için doğrudan kopyalıyoruz)
    df_customers = pd.read_csv(os.path.join(raw_path, 'olist_customers_dataset.csv'))
    df_customers.to_csv(os.path.join(processed_path, 'cleaned_customers.csv'), index=False)
    print("✓ Customers tablosu aktarıldı.")

    df_payments = pd.read_csv(os.path.join(raw_path, 'olist_order_payments_dataset.csv'))
    df_payments.to_csv(os.path.join(processed_path, 'cleaned_payments.csv'), index=False)
    print("✓ Payments tablosu aktarıldı.")
    
    print("Tüm temizleme işlemleri bitti. Dosyalar 'data/processed/' klasöründe hazır!")

if __name__ == "__main__":
    clean_data()