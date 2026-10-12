import re
from datetime import datetime

def clean_transactions(records):
    cleaned_records = []
    for record in records:
        if record['user_id'] and record['user_id'].strip():
            amount = re.sub(r'[^\d.]', '', record['amount'])
            record['amount'] = float(amount)
            date = record['date']
            if '/' in date:
                date = datetime.strptime(date, '%Y/%m/%d').strftime('%Y-%m-%d')
            elif '-' in date:
                date = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
            record['date'] = date
            cleaned_records.append(record)
    return cleaned_records