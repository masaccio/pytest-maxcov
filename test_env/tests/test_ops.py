from package import Add, Mul, Sub


def test_add():
    assert Add().add() == 30


def test_mul():
    assert Mul().mul() == 200


def test_sub():
    assert Sub().sub() == -10


def test_add_2():
    assert Add().add(double=True) == 60


def test_mul_2():
    assert Mul().mul(double=True) == 400


def test_sub_2():
    assert Sub().sub(double=True) == -20
