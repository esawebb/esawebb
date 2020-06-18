from django.test import TestCase


# TODO: remove and add real tests
class TestInitial(TestCase):
    def test_of_tests1(self):
        self.assertEquals(1, 1)

    def test_of_tests2(self):
        self.assertEquals(2, 6 / 3)

    def test_of_tests3(self):
        self.assertEquals(3, 4 * 2 - 5)
