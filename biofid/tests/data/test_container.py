from biofid.tests.base import NoDatabaseTestCase
from biofid.data import container


class TestContainer(NoDatabaseTestCase):
    def test_iterate_recursively(self):
        inputs = [
            ['ab', 'bc', 'cd'],
            ('ab', ('bc', 'cd'), 'de'),
            [(1, 2), (3, 4), 5, (6, 7)]
        ]

        expected = [
            ['ab', 'bc', 'cd'],
            ['ab', 'bc', 'cd', 'de'],
            [1, 2, 3, 4, 5, 6, 7]
        ]

        for inputs, expected_outcome in zip(inputs, expected):
            with self.subTest(input):
                self.assertEquals(list(container.iterate_recursively(inputs)), expected_outcome)
