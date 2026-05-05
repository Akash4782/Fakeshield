import re
try:
    content = open('app/models/text_classifier_ensemble.py', 'r', encoding='utf-8').read()
    print(f"Triple quotes count: {len(re.findall('\"\"\"', content))}")
except Exception as e:
    print(f"Error: {e}")
