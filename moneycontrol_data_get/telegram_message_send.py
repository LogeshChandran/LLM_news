import requests
from datetime import datetime
import pytz
import logging
import os

def split_message(text, limit=4096):
    parts = text.split('\n\n')  # Split by double newline (or adjust to your split logic)
    chunks = []
    current_chunk = ""

    for part in parts:
        if len(current_chunk) + len(part) + 2 <= limit:  # 2 extra for newline between parts
            current_chunk += part + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = part + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
    
def send_message_with_documents(message="", document_paths=[],captions=[]):
    bot_token = '6511501073:AAHbWvFY_dKcUQfKNGFODOeYK8PEUJ4vXPI'
    chat_id = -1002340142576
    print("telegram message")
    # bot_token = os.environ["BOT_TOKEN"]
    # chat_id = os.environ["CHAT_ID"]
    messages = split_message(message)
    for msg in messages:
        if msg :
        # if message:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            params = {
                'chat_id': chat_id,
                # 'text': message
                'text' : msg
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                # logging.info(f'Message sent successfully! - {message}')
                logging.info(f'Message sent successfully! - {msg}')
            else:
                logging.info(f'Failed to send message: - { response.text }')

    document_url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    for path,caption in zip(document_paths,captions):
        document_params = {
            'chat_id': chat_id,
            'caption' : caption
        }
        document_file = {'document': open(path, 'rb')}
        document_response = requests.post(document_url, params=document_params, files=document_file)
        if document_response.status_code == 200:
            logging.info(f'Message sent successfully! - {message}')
        else:
            logging.info(f'Failed to send message: - { response.text }')

if __name__=="__main__":
    message = 'Hello from Python! Here are the documents.'
    document_paths = ['line_pattern_pdf_report.pdf', 'line_pattern_pdf_report.pdf']
    send_message_with_documents(message=message, document_paths=document_paths,captions=["Line pattern","Line pattern"])
