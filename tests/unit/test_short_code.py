from app.services.link import generate_short_code


def test_generate_short_code_default_length() -> None:
    code = generate_short_code()

    assert len(code) == 7


def test_generate_short_code_custom_length() -> None:
    code = generate_short_code(10)

    assert len(code) == 10


def test_generate_short_code_contains_valid_characters() -> None:
    code = generate_short_code()

    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
    )

    assert all(
        character in allowed
        for character in code
    )


def test_generate_short_codes_are_not_identical() -> None:
    first = generate_short_code()
    second = generate_short_code()

    assert first != second