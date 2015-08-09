# coding=utf8

# представьте, что следующий словарь - база данных
# в дальнейших комментах под базой будет подразумеваться этот список


db = [
    {'id': 1, 'name': 'Chuck Norris', 'rate': 2},
    {'id': 2, 'name': 'Bruce Lee', 'rate': 1},
    {'id': 3, 'name': 'Jackie Chan', 'rate': 3},
]


class Entity:
    pass


class TextField:
    pass


class IntegerField:
    pass


# Делаем мини-модель ORM, нужно заставить работать следующий кусок кода.
# Для этого реализуйте объявленные выше классы, а также, если необходимо,
# базовые и метаклассы.


class User(Entity):
    __tablename__ = 'user'
    name = TextField()
    rate = IntegerField()
    # если угодно, можно заменить TextField на Field(Text), Field.Text и т.п.

u = User.get(2)                 # u должен присвоиться объект типа User
                                # с аттрибутами id=2, name='Bruce Lee', rate=1

u.name                          # вернет строку 'Bruce Lee'

u2 = User(name='Arni', rate=4)  # В "базу" должен записаться новый dict
                                # {'id': 4, 'name': 'Arni', 'rate': 4},
                                # переменной u2 должен присвоиться объект
                                # типа User c аттрибутами  name='Arni', rate=4

u2.rate                         # Должно вернуть 4 (int(4))

User.name == 'Duncan MacLeod'   # Выражение должно вернуть SQL statement
                                # (просто строку):
                                # "user"."name" = 'Duncan MacLeod'
