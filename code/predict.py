import json

import keras
import numpy as np
from keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences


class Translator():
    def __init__(self, model_path, input_tokenizer_json, target_tokenizer_json, maxlen):
        self.model_path = model_path
        self.input_tokenizer_json = input_tokenizer_json
        self.target_tokenizer_json = target_tokenizer_json
        self.maxlen = maxlen
        self.start_mark = '<start>'
        self.end_mark = '<end>'

        self._load_model()
        self._load_tokenizer()

    def _load_model(self):
        self.model = keras.models.load_model(self.model_path, compile=True)

    def _load_tokenizer(self):
        with open(self.input_tokenizer_json) as f:
            input_json = json.load(f)
            self.input_tokenizer = tokenizer_from_json(input_json)

        with open(self.target_tokenizer_json) as f:
            target_json = json.load(f)
            self.target_tokenizer = tokenizer_from_json(target_json)

    def _normalize_and_preprocess(self, text):
        punctuation = '!"#$%&()*+,-./:;=?@[\\]^_`{|}~\t\n'

        text = text.lower().strip()
        text = ''.join((filter(lambda x: x not in punctuation, text)))

        return text

    def lang_detector(self, sentence):
        return detect(sentence)

    def __call__(self, sentence):
        index_prediction = list()

        normalize_sentence = self._normalize_and_preprocess(sentence)
        sequences = self.input_tokenizer.texts_to_sequences(
            [normalize_sentence])
        sequences = pad_sequences(
            sequences, maxlen=self.maxlen, padding='post', truncating='post')

        predictions = self.model(sequences)

        for i in predictions[0]:
            index_prediction.append(np.argmax(i))

        marks = [self.start_mark, self.end_mark]
        result = self.target_tokenizer.sequences_to_texts([index_prediction])[
            0]

        result = ' '.join(
            [word for word in result.split(' ') if word not in marks])

        return result


if __name__ == '__main__':
    saved_model_path = 'code/translation/resources/saved_model'
    input_tokenizer_dir = 'code/translation/resources/input_tokenizer.json'
    target_tokenizer_dir = 'code/translation/resources/target_tokenizer.json'

    translator = Translator(
        saved_model_path,
        input_tokenizer_dir,
        target_tokenizer_dir,
        20
    )

    text_input = 'i like apple'
    translate = translator(text_input)

    print(translate)
