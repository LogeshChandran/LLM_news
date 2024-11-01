import pandas as pd
from datasets import load_dataset
from transformers import BartForConditionalGeneration, BartTokenizer
from datetime import datetime

dataset = load_dataset("LogeshChandran/money_control_news")
df = pd.DataFrame(dataset['train'])

today_date = datetime.today().strftime('%Y-%m-%d')
filtered_df = df[df['article date'] == today_date]

model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def summarize_content(text):
    if not text or len(text) < 100:
        return []
    
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)

    try:
        summary_ids = model.generate(inputs, max_length=250, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        points = summary.split('\n')
        return [point for point in points if point.strip()][0]
    
    except Exception as e:
        return []

# Apply summarization to each news article
filtered_df['new summary'] = filtered_df['content'].apply(summarize_content)

# Combine summaries into one message
message = "\n\n".join([f"{i+1}. {point}" for i, point in enumerate(filtered_df['new summary'].tolist())])