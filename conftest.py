import re
try:
    import json
except ImportError:
    import simplejson as json

import pytest

import docopt


def pytest_collect_file(file_path, parent):
    if file_path.suffix == ".docopt" and file_path.name.startswith("test"):
        return DocoptTestFile.from_parent(path=file_path, parent=parent)


def parse_test(raw):
    raw = re.compile('#.*$', re.M).sub('', raw).strip()
    if raw.startswith('"""'):
        raw = raw[3:]

    for fixture in raw.split('r"""'):
        name = ''
        doc, _, body = fixture.partition('"""')
        cases = []
        for case in body.split('$')[1:]:
            argv, _, expect = case.strip().partition('\n')
            expect = json.loads(expect)
            prog, _, argv = argv.strip().partition(' ')
            cases.append((prog, argv, expect))

        yield name, doc, cases


class DocoptTestFile(pytest.File):

    def collect(self):
        raw = self.path.read_text()
        index = 1

        for name, doc, cases in parse_test(raw):
            name = self.path.stem
            for case in cases:
                yield DocoptTestItem.from_parent(self, name="%s(%d)" % (name, index), doc=doc, case=case)
                index += 1


class DocoptTestItem(pytest.Item):

    @classmethod
    def from_parent(cls, parent, name, doc, case):
        self = super().from_parent(parent, name=name)
        self.doc = doc
        self.prog, self.argv, self.expect = case
        return self

    def runtest(self):
        try:
            result = docopt.docopt(self.doc, argv=self.argv)
        except docopt.DocoptExit:
            result = 'user-error'

        if self.expect != result:
            raise DocoptTestException(self, result)

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, DocoptTestException):
            return "\n".join((
                "usecase execution failed:",
                self.doc.rstrip(),
                "$ %s %s" % (self.prog, self.argv),
                "result> %s" % json.dumps(excinfo.value.args[1]),
                "expect> %s" % json.dumps(self.expect),
            ))

    def reportinfo(self):
        return self.fspath, 0, "usecase: %s" % self.name


class DocoptTestException(Exception):
    pass
