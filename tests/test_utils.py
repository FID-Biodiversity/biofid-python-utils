from tests.base import NoDatabaseTestCase
import utils


class TestBIOfidUtilities(NoDatabaseTestCase):
    def test_merge_list(self):
        test_lists = (
            (['not', 'nested', 'at', 'all'], ['not', 'nested', 'at', 'all']),
            (['only', ['one', 'element'], 'is', 'nested'], ['only', 'one', 'element', 'is', 'nested']),
            ([['everything', 'is'], ['in', 'a', 'list'], ['somehow']],
             ['everything', 'is', 'in', 'a', 'list', 'somehow'])
        )

        for test_list, expected_list in test_lists:
            with self.subTest(msg=f'List: {test_list}'):
                self.assertListEqual(list(utils.traverse(test_list)), expected_list)
