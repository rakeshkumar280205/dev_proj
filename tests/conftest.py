import sys
import types


class _FakeScalar(float):
    def item(self):
        return float(self)


class _FakeSentenceTransformer:
    def __init__(self, _model_name):
        pass

    def encode(self, data, convert_to_tensor=True):
        return data


def _fake_cos_sim(_left, right):
    count = len(right) if hasattr(right, "__len__") else 1
    return [[_FakeScalar(0.0) for _ in range(count)]]


class _FakeDoc:
    noun_chunks = ()


class _FakeNLP:
    def __call__(self, _text):
        return _FakeDoc()


def _install_test_stubs():
    # Avoid model downloads and heavy NLP startup during tests.
    if "sentence_transformers" not in sys.modules:
        fake_sentence_transformers = types.ModuleType("sentence_transformers")
        fake_sentence_transformers.SentenceTransformer = _FakeSentenceTransformer
        fake_sentence_transformers.util = types.SimpleNamespace(cos_sim=_fake_cos_sim)
        sys.modules["sentence_transformers"] = fake_sentence_transformers

    if "spacy" not in sys.modules:
        fake_spacy = types.ModuleType("spacy")
        fake_spacy.load = lambda _name: _FakeNLP()
        sys.modules["spacy"] = fake_spacy


_install_test_stubs()
