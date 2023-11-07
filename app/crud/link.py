from sqlalchemy.orm import Session

from core.db.models import Link


def get_link_by_id(db: Session, id: int) -> Link:
    link_db: Link = db.query(Link) \
                      .filter(Link.id == id) \
                      .one_or_none() \
    
    return link_db


def create_link(db: Session, url: str) -> Link:
    link_db = Link(url=url)
    db.add(link_db)
    db.commit()

    return link_db