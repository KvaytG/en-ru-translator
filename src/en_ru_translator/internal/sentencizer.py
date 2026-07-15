import spacy
import spacy.cli

class Sentencizer:
    """ INTERNAL CLASS! """
    def __init__(self):
        model_name = "en_core_web_sm"
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            spacy.cli.download(model_name)
            self.nlp = spacy.load(model_name)

    def split(self, text: str) -> list[str]:
        if not text.strip():
            return []
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents]
