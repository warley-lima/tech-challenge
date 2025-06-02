import pytest
from app.utils.utils import Utils

@pytest.mark.parametrize("input_value,expected", [
    ("producao", "prod"),
    ("processamento", "process"),
    ("comercializacao", "commer"),
    ("importacao", "import"),
    ("exportacao", "export"),
])
def test_normalize_option_offline(input_value, expected):
    if input_value is None:
        with pytest.raises(TypeError):
            Utils.normalize_option_offline(input_value)
    else:
        assert Utils.normalize_option_offline(input_value) == expected

@pytest.mark.parametrize("input_value,expected", [
    ("producao", "opt_02"),
    ("processamento", "opt_03"),
    ("comercializacao", "opt_04"),
    ("importacao", "opt_05"),
    ("exportacao", "opt_06"),
    ("publicacao", "opt_07"),
    ("unknown", "opt_02"),
    ("", "opt_02"),
])
def test_normalize_option(input_value, expected):
    if input_value is None:
        with pytest.raises(TypeError):
            Utils.normalize_option(input_value)
    else:
        assert Utils.normalize_option(input_value) == expected

@pytest.mark.parametrize("input_value,expected", [
    ("uvas", "subopt_03"),
    ("espumantes", "subopt_02"),
    ("americanas", "subopt_02"),
    ("vinhos", "subopt_01"),
    ("viniferas", "subopt_01"),
    ("passas", "subopt_04"),
    ("unclass", "subopt_04"),
    ("unknown", None),
    ("", None),
    (None, None),
])
def test_normalize_suboption(input_value, expected):
    if input_value is None:
        assert Utils.normalize_suboption(input_value) is None
    else:
        assert Utils.normalize_suboption(input_value) == expected