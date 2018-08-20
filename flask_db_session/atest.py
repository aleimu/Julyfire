import threading


class Session():
    public_methods = (
        '__contains__', '__iter__', 'add', 'add_all', 'begin', 'begin_nested',
        'close', 'commit', 'connection', 'delete', 'execute', 'expire',
        'expire_all', 'expunge', 'expunge_all', 'flush', 'get_bind',
        'is_modified', 'bulk_save_objects', 'bulk_insert_mappings',
        'bulk_update_mappings',
        'merge', 'query', 'refresh', 'rollback',
        'scalar')

    def add(self):
        return 'add'

    def add_ll(self):
        return 'aa'

    def __call__(self, *args, **kwargs):
        self.add_ll()


class scoped_session():
    def __init__(self):
        options = None
        if options is None:
            options = {}
        scopefunc = options.pop('scopefunc', Session())
        options.setdefault('query_cls', "aa")
        print("options:", options)
        self.registry = ThreadLocalRegistry(scopefunc)


class ThreadLocalRegistry():
    def __init__(self, createfunc):
        self.createfunc = createfunc
        self.registry = threading.local()

    def __call__(self):
        try:
            print("call")
            print(self.registry.value)
            return self.registry.value
        except AttributeError:
            print("except")
            val = self.registry.value = self.createfunc()
            return val


def instrument(name):
    def do(self, *args, **kwargs):
        return getattr(self.registry(), name)(*args, **kwargs)

    return do


for meth in Session.public_methods:
    setattr(scoped_session, meth, instrument(meth))

print(vars(Session))
print(vars(scoped_session))
# print(vars(scoped_session()))
print scoped_session().add_all()
