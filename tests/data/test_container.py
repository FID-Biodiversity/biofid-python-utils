from biofid.tests.base import NoDatabaseTestCase
from biofid.data import container


class TestContainer(NoDatabaseTestCase):
    def test_iterate_recursively(self):
        inputs = [
            ['ab', 'bc', 'cd'],
            ('ab', ('bc', 'cd'), 'de'),
            [(1, 2), (3, 4), 5, (6, 7)],

        ]

        expected = [
            ['ab', 'bc', 'cd'],
            ['ab', 'bc', 'cd', 'de'],
            [1, 2, 3, 4, 5, 6, 7],

        ]

        for inputs, expected_outcome in zip(inputs, expected):
            with self.subTest(input):
                self.assertEqual(list(container.iterate_recursively(inputs)), expected_outcome)

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
                self.assertEqual(container.convert_all_container_recursively(input, tuple), expectation)

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
                    self.assertEqual(elements, expected_elements)

    def test_escape_keys_and_values_of_dict(self):
        inputs = [
            {'$foo': 'bar&'},
            {'$foo': ['bar&', 'bu//']},
            {'$foo': {'bar&': 'bu//'}},
            {'$foo': {'bar&': ['bu//']}},
        ]

        expected = [
            {'\\$foo': 'bar\\&'},
            {'\\$foo': ['bar\\&', 'bu\\/\\/']},
            {'\\$foo': {'bar\\&': 'bu\\/\\/'}},
            {'\\$foo': {'bar\\&': ['bu\\/\\/']}},
        ]

        def dummy_escaping_function(text: str) -> str:
            return text.replace('$', '\\$').replace('&', '\\&').replace('/', '\\/')

        for input, expectation in zip(inputs, expected):
            with self.subTest(input):
                result = container.escape_keys_and_values_of_dict(input, dummy_escaping_function)
                self.assertDictEqual(expectation, result)
