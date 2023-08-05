from typing import List, Dict, Union
from collections import defaultdict

from flair.data import Sentence
from flair.models import TextClassifier


class EasySequenceClassifier:
    """ Sequence level classification models"""

    def __init__(self):
        self.sequence_classifiers: Dict[TextClassifier] = defaultdict(bool)

    def tag_text(
            self,
            text: Union[List[Sentence], Sentence, List[str], str],
            model_name_or_path: str = "en-sentiment",
            mini_batch_size: int = 32,
    ) -> List[Sentence]:
        """ Tags a text sequence with labels the sequence classification models have been trained on

        :param text: Text input, it can be a string or any of Flair's `Sentence` input formats
        :param model_name_or_path: The hosted model name key or model path
        :param mini_batch_size: The mini batch size for running inference
        :return: A list of Flair's `Sentence`s
        """
        # Load Text Classifier Model and Pytorch Module into tagger dict
        if not self.sequence_classifiers[model_name_or_path]:
            self.sequence_classifiers[model_name_or_path] = TextClassifier.load(model_name_or_path)

        classifier = self.sequence_classifiers[model_name_or_path]
        return classifier.predict(sentences=text, mini_batch_size=mini_batch_size, use_tokenizer=True)

    def tag_all(
            self,
            text: Union[List[Sentence], Sentence, List[str], str],
            mini_batch_size: int = 32,
    ) -> List[Sentence]:
        """ Tags text with all labels from all sequence classification models

        :param text: Text input, it can be a string or any of Flair's `Sentence` input formats
        :param mini_batch_size: The mini batch size for running inference
        :return: A list of Flair's `Sentence`s
        """
        sentences = text
        for tagger_name in self.sequence_classifiers.keys():
            sentences = self.tag_text(sentences, model_name_or_path=tagger_name, mini_batch_size=mini_batch_size)
        return sentences
