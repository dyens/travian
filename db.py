#!/usr/bin/env python

from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

KIND_CHOICES = {
    'g': 'Глиняный карьер',
    'f': 'Лесопилка',
    'i': 'Железный рудник',
    'c': 'Ферма',
}


class Mine(Base):
    __tablename__ = 'mines'

    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    kind = Column(String)
    level = Column(Integer)

    # Требуемые ресурсы для улучшения
    r_g = Column(Integer)
    r_f = Column(Integer)
    r_i = Column(Integer)
    r_c = Column(Integer)
    r_g_c = Column(Integer)

    # Добыча
    output = Column(Integer)

    # Добыча на следующем уровне
    n_output = Column(Integer)

    #Cтроится
    constructed = Column(Boolean, default=False)



    def __init__(self, x, y, kind, level, output, n_output, r_g, r_f, r_i, r_c, r_g_c):
        self.x = x
        self.y = y
        self.kind = kind
        self.level = level
        self.output = output
        self.n_output = n_output
        self.r_g = r_g
        self.r_f = r_f
        self.r_i = r_i
        self.r_c = r_c
        self.r_g_c = r_g_c
        self.constructed = False
        
    
    def __repr__(self):
        return '<Mine (%s %s [%s])>' % (self.kind, self.level, self.output)

    def upgrade(self, r_g, r_f, r_i, r_c, r_g_c, n_output):
        self.level = self.level + 1
        self.output = n_output
        self.n_output = n_output
        self.r_g = r_g
        self.r_f = r_f
        self.r_i = r_i
        self.r_g_c = r_g_c
        session.add(self)
        session.commit()


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    work_type = Column(String)
    datetime = Column(DateTime)
    params = Column(String)

    def __init__(self, work_type, datetime, params):
        self.work_type = work_type
        self.datetime = datetime
        self.params = params
    
    def __repr__(self):
        return '<Job (%s [%s])>' % (self.datetime, self.params)

    def clear(self):
        for job in session.query(Job).all():
            session.delete(job)
        session.commit()



class Cell(Base):
    __tablename__ = 'cells'

    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    type_name = Column(String)
    f = Column(Integer)
    g = Column(Integer)
    i = Column(Integer)
    c = Column(Integer)
    culture = Column(String)
    allaince = Column(String)
    player_name = Column(String)
    population = Column(Integer)


    def __init__(self, x, y, type_name, f, g, i, c, culture, allaince,
                 player_name, population):
        self.x = x
        self.y = y
        self.type_name = type_name
        self.g = g
        self.f = f
        self.i = i
        self.c = c
        self.culture = culture
        self.allaince = allaince
        self.player_name = player_name
        self.population = population

    @staticmethod
    def create_or_update(x, y, type_name, f, g, i, c, culture, allaince,
                 player_name, population):
        cell = session.query(Cell).filter_by(x=x, y=y).first()
        if not cell:
            cell = Cell(x, y, type_name, f, g, i, c, culture, allaince,
                        player_name, population)
        
        cell.type_name = type_name
        cell.g = g
        cell.f = f
        cell.i = i
        cell.c = c
        cell.culture = culture
        cell.allaince = allaince
        cell.player_name = player_name
        cell.population = population
        session.add(cell)
        session.commit()


        
    
    def __repr__(self):
        return '<Cell (%s [%s, %s])>' % (self.id, self.x, self.y)




def create_all():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_all()
