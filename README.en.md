
# en-ru-translator

![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![MIT License](https://img.shields.io/badge/License-MIT-green)

A simple tool for translating text from English to Russian using a MarianMT-based model.

## 📚 Usage
```python
from en_ru_translator import Translator

translator = Translator()

# Translating multiple lines
texts = [
    "Hello world! This is a test.",
    "I love you."
]
translations = translator.translate_batch(texts)
print(translations)

# Translating a single line
translation = translator.translate("This is a single sentence.")
print(translation)
```

## ⚙️ Installation
```bash
pip install git+https://github.com/KvaytG/en-ru-translator.git
```

## 📜 License
Licensed under the **[MIT](LICENSE.txt)** license.

This project uses open-source components. For license details see **[pyproject.toml](pyproject.toml)** and dependencies' official websites.
