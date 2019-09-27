from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import kamailio as schema
from wazo_router_confd.services import kamailio as service


router = APIRouter()


@router.post("/kamailio/routing")
def kamailio(request: schema.RoutingRequest, db: Session = Depends(get_db)):
    response = service.routing(db, request=request)
    return {
        "success": bool(response['routes']),
        "rtjson": response if response['routes'] else None,
    }
