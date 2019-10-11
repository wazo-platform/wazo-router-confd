from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import kamailio as schema, cdr as cdr_schema
from wazo_router_confd.services import kamailio as service, cdr as cdr_service


router = APIRouter()


@router.post("/kamailio/routing")
def kamailio_routing(request: schema.RoutingRequest, db: Session = Depends(get_db)):
    response = service.routing(db, request=request)
    return {
        "success": bool(response['routes']),
        "rtjson": response if response['routes'] else None,
    }


@router.post("/kamailio/cdr")
def kamailio_cdr(request: schema.CDRRequest, db: Session = Depends(get_db)):
    cdr = cdr_schema.CDRCreate(
        tenant_id=1,
        source_ip=request.source_ip,
        source_port=request.source_port,
        from_uri=request.from_uri,
        to_uri=request.to_uri,
        call_id=request.call_id,
        call_start=request.call_start,
        duration=request.duration,
    )
    response = cdr_service.create_cdr(db, cdr=cdr)
    return {"success": bool(response)}
