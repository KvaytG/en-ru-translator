import logging
import warnings
from typing import Optional
import torch
from transformers import MarianMTModel, MarianTokenizer
from transformers import logging as hf_logging
from .internal import TranslationCache, has_english_letters, Sentencizer

hf_logging.set_verbosity_error()
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning)


class Translator:
    def __init__(self, model_name: str = "KvaytG/marian-mt-en-ru-high-precision"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name).to(self.device)
        self.model.eval()
        self.cache = TranslationCache()
        self.sentencizer = Sentencizer()

    def translate_batch(self, texts: list[Optional[str]]) -> list[Optional[str]]:
        if not texts:
            return []
        results: list[Optional[str]] = [None] * len(texts)
        all_to_translate = []
        mapping = []
        sentences_per_text = []
        for idx, text in enumerate(texts):
            if text is None:
                sentences_per_text.append([])
                continue
            sentences = self.sentencizer.split(text)
            sentences_per_text.append(sentences)
            for pos, sent in enumerate(sentences):
                if has_english_letters(sent):
                    cached = self.cache.get(sent)
                    if cached is not None:
                        sentences[pos] = cached
                    else:
                        all_to_translate.append(sent)
                        mapping.append((idx, pos))
        if all_to_translate:
            inputs = self.tokenizer(
                all_to_translate,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128
            ).to(self.device)
            with torch.no_grad():
                generated_ids = self.model.generate(**inputs)
            translated_texts = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
            for (idx, pos), tr_text in zip(mapping, translated_texts):
                self.cache.set([(all_to_translate.pop(0), tr_text)])
                sentences_per_text[idx][pos] = tr_text
        for idx, sentences in enumerate(sentences_per_text):
            if sentences:
                results[idx] = " ".join(sentences)
            else:
                results[idx] = texts[idx]
        self.cache.save()
        return results

    def translate(self, text: Optional[str]) -> Optional[str]:
        return self.translate_batch([text])[0]
