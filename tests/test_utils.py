# tests/test_utils.py
import string
from utils import generate_short_code

def test_generate_short_code_length():
    code = generate_short_code(size=8)
    assert isinstance(code, str)
    assert len(code) == 8

def test_generate_short_code_characters():
    code = generate_short_code(size=10)
    allowed_chars = set(string.ascii_letters + string.digits)
    # Проверяем, что все символы входят в разрешённый набор
    assert set(code).issubset(allowed_chars)