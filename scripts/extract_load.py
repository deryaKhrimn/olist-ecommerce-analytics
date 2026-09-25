# scripts/extract_load.py
import kaggle

def download_olist_data():
    dataset = "olistbr/brazilian-ecommerce"
    download_path = "data/raw"
    
    print(f"Kaggle'dan {dataset} veri seti indiriliyor...")
    kaggle.api.dataset_download_files(dataset, path=download_path, unzip=True)
    print("Veri indirme ve zipten çıkarma işlemi tamamlandı!")

if __name__ == "__main__":
    download_olist_data()