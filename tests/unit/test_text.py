from api.services.text import build_input


def test_star_title_is_masked():
    assert build_input("Five Stars", "Great") == " . Great"
    assert build_input("Five Stars", "Great") == build_input("", "Great")
    assert build_input("4.0 out of 5 stars", "Great") == build_input("", "Great")


def test_real_title_is_kept():
    assert build_input("Broke", "bad") == "Broke . bad"
