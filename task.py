# coding=utf8

# представьте, что следующий словарь - база данных
# в дальнейших комментах под базой будет подразумеваться этот список


db = [
    {'id': 1, 'name': 'Chuck Norris', 'rate': 2},
    {'id': 2, 'name': 'Bruce Lee', 'rate': 1},
    {'id': 3, 'name': 'Jackie Chan', 'rate': 3},
]


class Field:
    _eq_fmt = '{}.{} = {}'

    def __init__(self, *args, **kwargs):
        pass

    def __eq__(self, other):
        return self._eq_fmt.format(self._tbname, self._name, other)

    def __get__(self, instance, owner):
        if isinstance(instance, (Entity)):
            self._cached_value = instance._reflection[self._name]
            return self._cached_value
        return self

    def __set__(self, instance, value):
        if isinstance(instance, Entity):
            self._cached_value = value
            instance._reflection[self._name] = value
        else:
            raise TypeError("instance %s is not Entity" % instance)

    def __getattribute__(self, name):
        if name == 'value':
            name = '_cached_value'
        return super().__getattribute__(name)

    def __setattribute__(self, name, value):
        if name == 'value':
            raise AttributeError("access denied")
        return super().__getattribute__(name)


class TextField(Field):
    _eq_fmt = '"{}"."{}" = \'{}\''
    pass


class IntegerField(Field):
    _eq_fmt = '"{}"."{}" = {}'
    pass


class EntityMeta(type):

    def __new__(meta_cls, name, bases, attrs):
        if attrs.get('__tablename__', None) is None:
            attrs['__tablename__'] = name.lower()
        attrs['id'] = IntegerField()
        for key, value in attrs.items():
            if isinstance(value, Field):
                setattr(value, '_name', key)
                setattr(value, '_tbname', attrs['__tablename__'])
        clazz = super(EntityMeta, meta_cls).__new__(
            meta_cls,
            name,
            bases,
            attrs
        )
        return clazz


class Entity(object, metaclass=EntityMeta):
    _reflection = None

    @staticmethod
    def _get_new_id():
        return (max(db, key=lambda item: item['id'])['id'] + 1)

    def __init__(self, **kwargs):
        self._reflection = kwargs.get('reflection', None)
        if self._reflection is None:
            self._reflection = {'id': Entity._get_new_id()}
            db.append(self._reflection)
            for (key, value) in kwargs.items():
                self.__setattr__(key, value)

    @classmethod
    def get(clazz, id):
        gen = (entry for entry in db if entry['id'] == id)
        reflection = next(gen)
        gen.close()
        instance = clazz(reflection=reflection)
        return instance


# Делаем мини-модель ORM, нужно заставить работать следующий кусок кода.
# Для этого реализуйте объявленные выше классы, а также, если необходимо,
# базовые и метаклассы.


class User(Entity):
    __tablename__ = 'user'
    name = TextField()
    rate = IntegerField()


u = User.get(2)
# u должен присвоиться объект типа User
assert (isinstance(u, User))
# с аттрибутами id=2, name='Bruce Lee', rate=1
assert ((u.id, u.name, u.rate) == (2, 'Bruce Lee', 1))

# вернет строку 'Bruce Lee'
assert (u.name == 'Bruce Lee')

u2 = User(name='Arni', rate=4)
# В "базу" должен записаться новый dict
# {'id': 4, 'name': 'Arni', 'rate': 4},
# переменной u2 должен присвоиться объект
# типа User c аттрибутами  name='Arni', rate=4
assert ({'id': 4, 'name': 'Arni', 'rate': 4} in db)

# Должно вернуть 4 (int(4))
assert (u2.rate == int(4))

statement = User.name == 'Duncan MacLeod'
# Выражение должно вернуть SQL statement
# (просто строку):
# "user"."name" = 'Duncan MacLeod'
assert (statement == '"user"."name" = \'Duncan MacLeod\'')
