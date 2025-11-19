import os
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pract3Belova.settings')

import django
django.setup()

def create_template_files():
    templates = {
        # ... все шаблоны из кода выше ...
    }
    
    for filepath, content in templates.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Создан: {filepath}")

if __name__ == "__main__":
    create_template_files()