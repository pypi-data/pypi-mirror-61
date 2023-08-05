import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .dependencies import get_db, get_current_playlist
from escarpolette.login import get_current_user, User
from escarpolette.models import Item, Playlist
from escarpolette.player import get_player, Player
from escarpolette.schemas.item import ItemSchemaIn, ItemSchemaOut
from escarpolette.schemas.playlist import PlaylistSchemaOut
from escarpolette.tools import get_content_metadata
from escarpolette.rules import rules


logger = logging.getLogger(__name__)
router = APIRouter()

ERROR_CONFLICT_MSG = "This item is already waiting to be played"


@router.get("/", response_model=PlaylistSchemaOut)
def get(
    current_playlist: Playlist = Depends(get_current_playlist),
) -> PlaylistSchemaOut:
    playlist = PlaylistSchemaOut()

    for item in current_playlist.items:
        playlist.items.append(
            ItemSchemaOut(
                artist=item.artist,
                duration=item.duration,
                title=item.title,
                url=item.url,
            )
        )
        if item.played:
            playlist.idx += 1

    return playlist


@router.post(
    "/",
    status_code=201,
    response_model=ItemSchemaOut,
    responses={409: {"description": ERROR_CONFLICT_MSG}},
)
async def post(
    data: ItemSchemaIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    playlist: Playlist = Depends(get_current_playlist),
    player: Player = Depends(get_player),
) -> Item:
    metadata = get_content_metadata(data.url)
    item = Item(user_id=current_user.id, **metadata)

    if not rules.can_add_item(current_user, item, db):
        raise TooManyRequests

    playlist.items.append(item)
    db.add(playlist)

    try:
        db.flush()
    except IntegrityError as e:
        logger.debug("Integrity error while trying to add a new item: %s", e)
        raise HTTPException(status_code=409, detail=ERROR_CONFLICT_MSG)

    await player.add_item(item.url)
    db.commit()

    return item
