# scripts/load_to_postgres.py
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
import os
from dotenv import load_dotenv 

# .env dosyasını yükle
load_dotenv() 

def load_data_to_db():
    DB_USER = 'postgres'
    DB_PASS = os.getenv('DB_PASS') 
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'olist_db'

    # Şifreyi URL formatına uygun şekilde encode ediyoruz
    encoded_pass = urllib.parse.quote_plus(DB_PASS)

    # SQLAlchemy Engine oluşturma
    connection_string = f"postgresql+psycopg2://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)
    
    processed_path = "data/processed/"
    
    print("PostgreSQL bağlantısı kuruldu. Veriler yükleniyor...")

    # 1. Customers Tablosu
    df_customers = pd.read_csv(os.path.join(processed_path, 'cleaned_customers.csv'))
    df_customers.to_sql('raw_customers', engine, if_exists='replace', index=False)
    print(" raw_customers tablosu yüklendi.")

    # 2. Products Tablosu (İngilizce kategoriler dahil)
    df_products = pd.read_csv(os.path.join(processed_path, 'cleaned_products.csv'))
    df_products.to_sql('raw_products', engine, if_exists='replace', index=False)
    print(" raw_products tablosu yüklendi.")

    # 3. Orders Tablosu (Gecikme ve Süre metrikleri dahil)
    df_orders = pd.read_csv(os.path.join(processed_path, 'cleaned_orders.csv'))
    df_orders.to_sql('raw_orders', engine, if_exists='replace', index=False)
    print("raw_orders tablosu yüklendi.")

    # 4. Payments Tablosu
    df_payments = pd.read_csv(os.path.join(processed_path, 'cleaned_payments.csv'))
    df_payments.to_sql('raw_payments', engine, if_exists='replace', index=False)
    print("raw_payments tablosu yüklendi.")

    # 5. Order Items Tablosu (YENİ EKLENEN TABLO)
    df_items = pd.read_csv(os.path.join(processed_path, 'cleaned_order_items.csv'))
    df_items.to_sql('raw_order_items', engine, if_exists='replace', index=False)
    print("raw_order_items tablosu yüklendi.")

    print("Bütün veriler PostgreSQL'e başarıyla aktarıldı")

if __name__ == "__main__":
    load_data_to_db()