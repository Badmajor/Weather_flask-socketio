from . import db


def get_or_create(model, session=db.session, **kwargs):
    """Метод возвращает объект, если его нет в базе, создает."""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance, True
