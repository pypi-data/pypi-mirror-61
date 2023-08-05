import re
from parglare import Grammar, Parser


def test_pass_to_action():
    """
    Testing passing additional information from recognizer to action.
    """

    grammar = r'''
    S: a;
    terminals
    a: ;
    '''

    called = [False]
    passed = [None]

    def a_rec(input, pos):
        m = re.compile(r'(\d+)')
        result = m.match(input[pos:])
        passed[0] = result
        return result.group(), result

    def a_act(context, value, match):
        """
        Action will get the additional returned information from the a_rec
        recognizer. In this case a regex match object.
        """
        called[0] = True
        assert value == '42'
        assert passed[0] is match

    g = Grammar.from_string(grammar,
                            recognizers={
                                'a': a_rec
                            })
    Parser(g,
           actions={
               'a': a_act
           }).parse('42')

    assert called[0]
