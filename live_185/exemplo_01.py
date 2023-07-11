from typing import Optional

import strawberry
from sqlmodel import (
    SQLModel,
    Field,
    create_engine,
    select,
    Session
)


engine = create_engine('sqlite:///database.db')


class ModelPessoa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: int


SQLModel.metadata.create_all(engine)


def cria_pessoa(idade: int, nome: str):
    pessoa = ModelPessoa(nome=nome, idade=idade)

    with Session(engine) as session:
        session.add(pessoa)
        session.commit()
        session.refresh(pessoa)

    return pessoa


@strawberry.type
class Pessoa:
    id: Optional[int]
    nome: str
    idade: int


@strawberry.type
class Query:

    @strawberry.field
    def all_pessoa() -> list[Pessoa]:
        query = select(ModelPessoa)
        with Session(engine) as session:
            result = session.execute(query).scalars().all()

        return result
    

@strawberry.type
class Mutation:
    create_pessoa: Pessoa = strawberry.field(resolver=cria_pessoa)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
