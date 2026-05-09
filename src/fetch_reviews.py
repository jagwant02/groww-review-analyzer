import os
import pandas as pd
from google_play_scraper import Sort, reviews

# Groww app package name on Google Play Store
APP_PACKAGE = 'com.nextbillion.groww'

def fetch_app_reviews(app_package: str, count: int = 500):
    """
    Fetches the most recent public reviews for the specified app.
    Does NOT require login/scraping behind authentication.
    """
    print(f"Fetching up to {count} recent reviews for {app_package}...")
    
    result, continuation_token = reviews(
        app_package,
        lang='en', # Language
        country='in', # Country (Groww is primarily India)
        sort=Sort.NEWEST, # Get the latest reviews (last 8-12 weeks)
        count=count
    )
    
    # Extract relevant fields
    extracted_reviews = []
    for r in result:
        extracted_reviews.append({
            'date': r['at'],
            'rating': r['score'],
            'userName': r['userName'],
            'text': r['content']
        })
        
    df = pd.DataFrame(extracted_reviews)
    return df

if __name__ == "__main__":
    # Ensure data directory exists (relative to project root)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Fetch reviews
    df_reviews = fetch_app_reviews(APP_PACKAGE, count=200)
    
    # Save to CSV
    output_path = os.path.join(data_dir, 'raw_reviews.csv')
    df_reviews.to_csv(output_path, index=False)
    print(f"Successfully saved {len(df_reviews)} reviews to {output_path}")
