








class Option(object):
    def __init__(self, source):
        source = source.strip().split('  ')[0]
        self.argument_count = 1 if '=' in source else 0
        source = source.replace('=', ' ')
        self.short = None
        self.full = None
        for s in source.split():
            if s.startswith('--'):
                self.full = s
                continue
            if s.startswith('-'):
                self.short = s
        self.name = (self.full or self.short).lstrip('-')
        self.default = None
