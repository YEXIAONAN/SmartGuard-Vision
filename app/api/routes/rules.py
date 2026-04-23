from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.schemas.response import ApiResponse
from app.schemas.rule import RuleConfigRead, RuleConfigUpdate
from app.services.audit_service import log_audit_event
from app.services.rule_service import list_rules, set_rule
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[list[RuleConfigRead]], summary="规则配置列表")
def get_rules(
    db: Session = Depends(get_db),
    _: object = Depends(require_roles("admin", "operator")),
):
    return success_response(data=list_rules(db))


@router.put("/{rule_key}", response_model=ApiResponse[RuleConfigRead], summary="更新规则配置")
def put_rule(
    payload: RuleConfigUpdate,
    rule_key: str = Path(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _: object = Depends(require_roles("admin")),
):
    rule = set_rule(
        db,
        rule_key=rule_key,
        rule_value=payload.rule_value,
        description=payload.description,
        updated_by=current_user.username,
    )
    log_audit_event(
        db,
        username=current_user.username,
        role=current_user.role,
        action="rule.update",
        target_type="rule",
        target_id=rule_key,
        detail=f"更新规则为 {payload.rule_value}",
    )
    return success_response(data=rule, message="rule updated")
