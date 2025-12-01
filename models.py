from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Professor(Base):
    __tablename__ = 'professores'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    disciplina = Column(String, nullable=True)

    turmas = relationship('Turma', back_populates='professor', cascade='all, delete-orphan')


class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sala = Column(String, nullable=True)
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=True)

    professor = relationship('Professor', back_populates='turmas')
    alunos = relationship('Aluno', back_populates='turma', cascade='all, delete-orphan')


class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=True)
    turma_id = Column(Integer, ForeignKey('turmas.id'), nullable=True)

    turma = relationship('Turma', back_populates='alunos')
