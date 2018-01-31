import os
from subprocess import check_call
from tempfile import NamedTemporaryFile

from tests.data import demo
from tests.data import demo_testsuite

expected_content = "tests.data.demo_testsuite:test_callDemo(F),"+ \
                demo_testsuite.__file__+";" \
                "tests.data.demo:callDemo(F),"+ \
                demo.__file__+"\n" \
                "tests.data.demo:callDemo(F),"+ \
                demo.__file__+";" \
                "tests.data.demo:Demo(C).__init__(F),"+ \
                demo.__file__+"\n" \
                "tests.data.demo:callDemo(F),"+ \
                demo.__file__+";" \
                "tests.data.demo:Demo(C).bar(F),"+ \
                demo.__file__+"\n" \
                "tests.data.demo:Demo(C).bar(F),"+ \
                demo.__file__+";" \
                "tests.data.demo:Demo(C).foo(F),"+ \
                demo.__file__


def test_nose_collection():
    with NamedTemporaryFile() as report, open(os.devnull, 'w') as devnull:
        check_call(
            ['nosetests',
             'tests/data/demo_testsuite.py',
             '--with-callgraph',
             '--callgraph-paths=%s' % os.path.dirname(demo.__file__),
             '--callgraph-output={}'.format(report.name)
             ],
            stdout=devnull,
            stderr=devnull)

        report.seek(0)
        contents = report.read().decode('utf8')
        assert contents == expected_content

def test_pytest_collection():
    with NamedTemporaryFile() as report, open(os.devnull, 'w') as devnull:
        check_call(
            ['py.test',
             'tests/data/demo_testsuite.py',
             '--callgraph-paths=%s' % os.path.dirname(demo.__file__),
             '--callgraph-output={}'.format(report.name)
             ],
            stdout=devnull,
            stderr=devnull)

        report.seek(0)
        contents = report.read().decode('utf8')
        assert contents == expected_content