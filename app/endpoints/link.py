import json

from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db

from core.broker import session
from crud.link import get_link_by_id, create_link, update_status_by_id
from schemas.link import Link, LinkInDB, LinkUpdate


router = APIRouter(prefix="/links")


@router.get('/', response_model=LinkInDB)
def get_link(id: int, db=Depends(get_db)):
    result = get_link_by_id(db=db, id=id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    link_db = LinkInDB(id=result.id, url=result.url, status=result.status)

    return link_db


@router.post("/", response_model=LinkInDB)
async def post_link(link: Link, db=Depends(get_db)):
    result = create_link(db=db, url=link.url)
    link_db = LinkInDB(id=result.id, url=result.url, status=result.status)

    session.publish_task(json.dumps(result.as_dict()))

    return link_db


@router.put('/', response_model=LinkInDB)
def update_link(link: LinkUpdate, db=Depends(get_db)):
    result = update_status_by_id(db=db, id=link.id, status=link.status)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return LinkInDB(id=result.id, url=result.url, status=result.status)
