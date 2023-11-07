from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db

import crud.link as crud
from schemas.link import Link, LinkInDB


router = APIRouter(prefix="/links")


@router.get('/', response_model=LinkInDB)
def get_link(id: int, db=Depends(get_db)):
    result = crud.get_link_by_id(db=db, id=id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    link_db = LinkInDB(id=result.id, url=result.url)

    return link_db


@router.post("/", response_model=LinkInDB)
async def create_link(link: Link, db=Depends(get_db)):
    result = crud.create_link(db=db, url=link.url)
    link_db = LinkInDB(id=result.id, url=result.url)

    return link_db
