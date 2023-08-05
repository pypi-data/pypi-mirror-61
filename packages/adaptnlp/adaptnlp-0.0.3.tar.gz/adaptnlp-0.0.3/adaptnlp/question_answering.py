from typing import Tuple, List
from collections import OrderedDict

from adaptnlp.transformers import BertQuestionAnsweringModel


class EasyQuestionAnswering:
    """Question Answering Module
    """

    def __init__(self):
        self.bert_qa = None

    # Dynamic Loaders
    def _load_bert_qa(self) -> None:
        self.bert_qa = BertQuestionAnsweringModel()

    # QA Models
    def predict_bert_qa(self, query: str, context: str, n_best_size: int = 20) -> Tuple[str, List[OrderedDict]]:
        ''' Predicts top_n answer spans of query in regards to context


        :param query: The question
        :param context: The context of which the question is asking
        :param top_n: The top n answers returned

        :return: Either a list of string answers or a dict of the results
        '''

        self._load_bert_qa() if not self.bert_qa else None
        return self.bert_qa.predict(query=query, context=context, n_best_size=n_best_size)
