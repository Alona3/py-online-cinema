from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: int
    __name__: str

    # Автоматично задає ім'я таблиці за ім'ям класу в нижньому регістрі
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"  # додає "s", щоб було множина, напр. users
