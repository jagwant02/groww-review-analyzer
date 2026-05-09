import os
import re
import pandas as pd

def scrub_pii(text: str) -> str:
    """
    Strips potential PII (Emails, Phone Numbers, common ID formats) from text.
    Ensures 100% compliance with privacy constraints.
    """
    if not isinstance(text, str):
        return ""
        
    # Regex for email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, '[EMAIL REDACTED]', text)
    
    # Regex for phone numbers (basic international/local patterns)
    phone_pattern = r'(\+?\d{1,3}[-\s]?)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}'
    text = re.sub(phone_pattern, '[PHONE REDACTED]', text)
    
    # Regex for generic IDs (like transaction IDs, alphanumeric strings of certain length)
    # Groww specific or general transaction IDs (e.g., matching length 10+ alphanumeric)
    id_pattern = r'\b[A-Z0-9]{10,}\b'
    text = re.sub(id_pattern, '[ID REDACTED]', text)
    
    return text

def sanitize_dataset(input_csv: str, output_csv: str):
    """
    Reads raw reviews, scrubs PII, drops username columns, and saves the cleaned dataset.
    """
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} does not exist. Run fetch_reviews.py first.")
        return
        
    print(f"Loading raw reviews from {input_csv}...")
    df = pd.read_csv(input_csv)
    
    # Drop username to ensure anonymity
    if 'userName' in df.columns:
        df = df.drop(columns=['userName'])
        print("Dropped 'userName' column for compliance.")
        
    # Apply PII scrubbing to the review text
    print("Scrubbing text for Emails, Phone Numbers, and IDs...")
    df['text'] = df['text'].apply(scrub_pii)
    
    # Save the sanitized dataset
    df.to_csv(output_csv, index=False)
    print(f"Successfully saved sanitized reviews to {output_csv}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    input_path = os.path.join(data_dir, 'raw_reviews.csv')
    output_path = os.path.join(data_dir, 'scrubbed_reviews.csv')
    sanitize_dataset(input_path, output_path)
