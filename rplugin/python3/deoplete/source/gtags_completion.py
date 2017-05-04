import os
import sys

sys.path.insert(1, os.path.dirname(__file__))
from deoplete_gtags import GtagsBase # pylint: disable=locally-disabled, wrong-import-position

class Source(GtagsBase):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'gtags'
        self.mark = '[gtags]'

    @classmethod
    def get_search_flags(cls):
        return ['-c']

    @classmethod
    def get_search_word(cls, context):
        return '"{}"'.format(context['input'])

    def gather_candidates(self, context):
        word = self.get_search_word(context)
        tags = self.exec_global(self.get_search_flags() + [word], context)
        candidates = self._convert_to_candidates(tags)
        return candidates

    @classmethod
    def _convert_to_candidates(cls, tags):
        return [{'word': t} for t in tags]
