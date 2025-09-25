from datetime import datetime
from flask import request as flask_request
from flask_restx import Namespace, Resource, fields
from ...extensions import db
from ...models import ProcurementRequest, Approval, ApprovalDecision, RequestStatus
from ...services.approval_matrix import get_approval_steps

api = Namespace('workflow', description='Workflow actions')

approve_action_model = api.model('ApproveAction', {
    'action': fields.String(enum=['approve', 'reject', 'clarify'], required=True),
    'comment': fields.String,
    'approver_id': fields.Integer(required=True),  # replace with JWT later
    'role': fields.String(required=True),
})

approval_needed_model = api.model('ApprovalNeeded', {
    'roles': fields.List(fields.String),
})


@api.route('/<int:request_id>/needed')
class NeededApprovalsResource(Resource):
    @api.marshal_list_with(approval_needed_model)
    def get(self, request_id: int):
        req = ProcurementRequest.query.get_or_404(request_id)
        steps = get_approval_steps(float(req.amount))
        return [{'roles': s.roles} for s in steps]


@api.route('/<int:request_id>/action')
class WorkflowActionResource(Resource):
    @api.expect(approve_action_model, validate=True)
    def post(self, request_id: int):
        payload = flask_request.get_json()
        req = ProcurementRequest.query.get_or_404(request_id)
        action = payload['action']
        comment = payload.get('comment')
        role = payload['role']
        approver_id = payload['approver_id']

        if action == 'approve':
            decision = ApprovalDecision.APPROVED
        elif action == 'reject':
            decision = ApprovalDecision.REJECTED
        elif action == 'clarify':
            decision = ApprovalDecision.CLARIFY
        else:
            return {'message': 'Invalid action'}, 400

        approval = Approval(
            request_id=req.id,
            approver_id=approver_id,
            role=role,
            decision=decision,
            comment=comment,
            decided_at=datetime.utcnow(),
        )
        db.session.add(approval)

        # Update request status
        if decision == ApprovalDecision.REJECTED:
            req.status = RequestStatus.REJECTED
        elif decision == ApprovalDecision.CLARIFY:
            req.status = RequestStatus.CLARIFICATION
        else:
            # Simplified progression; detailed step tracking can be added later
            req.status = RequestStatus.UNDER_REVIEW

        db.session.commit()
        return {'message': 'Action recorded', 'status': req.status}, 200