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

    def test_convert_all_container_recursively_to_tuple(self):
        inputs = [
            ['a', 'b', ['c', 'd', ['e']], 'f'],
            [1, 2, 3, (4, 5, 6), (7, 8, 9)]
        ]

        expected = [
            ('a', 'b', ('c', 'd', ('e',)), 'f'),
            (1, 2, 3, (4, 5, 6), (7, 8, 9))
        ]

        for input, expectation in zip(inputs, expected):
            with self.subTest(input):
                self.assertEquals(container.convert_all_container_recursively(input, tuple), expectation)

    def test_group_elements(self):
        inputs = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ]

        expected = [
            ((1, 2, 3), (4, 5, 6), (7, 8, 9)),
            ((1, 2), (3, 4), (5, 6), (7, 8), (9, 10))
        ]

        number_of_elements_per_loop = [
            3, 2
        ]

        for input, expectation, elements_per_loop in zip(inputs, expected, number_of_elements_per_loop):
            with self.subTest(input):
                for elements, expected_elements in zip(container.group_elements(input, elements_per_loop), expectation):
                    self.assertEquals(elements, expected_elements)
