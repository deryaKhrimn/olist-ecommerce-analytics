# scripts/data_cleaning.py
import pandas as pd
import os

def clean_data():
    raw_path = "data/raw/"
    processed_path = "data/processed/"
    
    if not os.path.exists(processed_path):
        os.makedirs(processed_path)
        
    print("Veri temizleme ve Feature Engineering işlemi başlıyor...")

    # 1. ORDERS: Tarih düzeltmeleri ve Yeni Metrikler (Feature Engineering)
    df_orders = pd.read_csv(os.path.join(raw_path, 'olist_orders_dataset.csv'))
    
    date_columns = ['order_purchase_timestamp', 'order_approved_at', 
                    'order_delivered_carrier_date', 'order_delivered_customer_date', 
                    'order_estimated_delivery_date']
    
    for col in date_columns:
        df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')
        
    # Teslimat süresi (Gün) ve Gecikme durumu (True/False)
    df_orders['delivery_duration_days'] = (df_orders['order_delivered_customer_date'] - df_orders['order_purchase_timestamp']).dt.days
    df_orders['is_delayed'] = (df_orders['order_delivered_customer_date'] > df_orders['order_estimated_delivery_date']) & (df_orders['order_delivered_customer_date'].notnull())
    
    df_orders.to_csv(os.path.join(processed_path, 'cleaned_orders.csv'), index=False)
    print("✓ Orders tablosu temizlendi (Süre ve Gecikme metrikleri eklendi).")

   # 2. PRODUCTS: Eksik Veri Doldurma ve İNGİLİZCE KATEGORİ EKLEME (Merge)
    df_products = pd.read_csv(os.path.join(raw_path, 'olist_products_dataset.csv'))
    
    # Kategori çeviri tablosunu okuyoruz
    df_translation = pd.read_csv(os.path.join(raw_path, 'product_category_name_translation.csv'))
    
    # Pandas ile Left Join yaparak İngilizce isimleri ana tabloya ekliyoruz
    df_products = pd.merge(df_products, df_translation, on='product_category_name', how='left')
    
    # Eksik kategorileri 'Unknown' ile doldurma (Hem Portekizce hem İngilizce kolon için)
    df_products['product_category_name'] = df_products['product_category_name'].fillna('Unknown')
    df_products['product_category_name_english'] = df_products['product_category_name_english'].fillna('Unknown')
    
    numeric_cols = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 
                    'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
    for col in numeric_cols:
        df_products[col] = df_products[col].fillna(0)
        
    df_products.to_csv(os.path.join(processed_path, 'cleaned_products.csv'), index=False)
    print("✓ Products tablosu temizlendi (İngilizce kategori isimleri eklendi).")

    # 3. CUSTOMERS: Metin Standardizasyonu (Çok önemli!)
    df_customers = pd.read_csv(os.path.join(raw_path, 'olist_customers_dataset.csv'))
    df_customers['customer_city'] = df_customers['customer_city'].str.lower().str.strip()
    df_customers.to_csv(os.path.join(processed_path, 'cleaned_customers.csv'), index=False)
    print("✓ Customers tablosu temizlendi (Şehir isimleri standardize edildi).")

    # 4. PAYMENTS
    df_payments = pd.read_csv(os.path.join(raw_path, 'olist_order_payments_dataset.csv'))
    df_payments.to_csv(os.path.join(processed_path, 'cleaned_payments.csv'), index=False)
    print("✓ Payments tablosu aktarıldı.")

    # 5. ORDER ITEMS (YENİ EKLENDİ)
    df_items = pd.read_csv(os.path.join(raw_path, 'olist_order_items_dataset.csv'))
    # Tarih kolonunu düzeltelim
    df_items['shipping_limit_date'] = pd.to_datetime(df_items['shipping_limit_date'], errors='coerce')
    df_items.to_csv(os.path.join(processed_path, 'cleaned_order_items.csv'), index=False)
    print("✓ Order Items tablosu aktarıldı.")
    
    print("Tüm işlemler bitti. Yeni veriler 'data/processed/' klasöründe!")

if __name__ == "__main__":
    clean_data()