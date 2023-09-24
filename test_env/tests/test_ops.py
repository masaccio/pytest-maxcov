from package import Add, Mul, Sub


def test_add():
    assert Add().add() == 30


def test_mul():
    assert Mul().mul() == 200


def test_sub():
    assert Sub().sub() == -10
