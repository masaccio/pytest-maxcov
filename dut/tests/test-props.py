from package import Add, Mul, Sub


def test_add_a():
    assert Add().a == 10


def test_add_b():
    assert Add().b == 20


def test_mul_a():
    assert Mul().a == 10


def test_mul_b():
    assert Mul().b == 20


def test_sub_a():
    assert Sub().a == 10


def test_sub_b():
    assert Sub().b == 20
