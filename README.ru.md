
# en-ru-translator

[![US](https://kvaytg.ru/common/flags/us-21x16.svg) English](README.md) | ![RU](https://kvaytg.ru/common/flags/ru-21x16.svg) **Русский**

![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![PolyForm License](https://img.shields.io/badge/License-PolyForm-blue)

Простой инструмент для перевода текста с английского на русский с использованием модели на основе MarianMT.

## 📚 Использование
```python
from en_ru_translator import Translator

translator = Translator()

# Перевод нескольких строк
texts = [
    "Hello world! This is a test.",
    "I love you."
]
translations = translator.translate_batch(texts)
print(translations)

# Перевод одной строки
translation = translator.translate("This is a single sentence.")
print(translation)
```

## ⚙️ Установка
```bash
pip install git+https://github.com/KvaytG/en-ru-translator.git
```

## 📜 Лицензия
Распространяется по лицензии **[PolyForm Noncommercial](LICENSE.md)**.

Проект использует компоненты с открытым исходным кодом. Сведения о лицензиях см. в **[pyproject.toml](pyproject.toml)** и на официальных ресурсах зависимостей.
