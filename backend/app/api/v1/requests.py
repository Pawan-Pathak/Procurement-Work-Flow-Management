from flask import request as flask_request
from flask_restx import Namespace, Resource, fields
from ...extensions import db
from ...models import ProcurementRequest, RequestItem, RequestStatus

api = Namespace('requests', description='Procurement Requests')

request_item_model = api.model('RequestItem', {
    'description': fields.String(required=True),
    'quantity': fields.Integer(required=True, min=1),
    'unit_price': fields.Float(required=True, min=0),
})

request_create_model = api.model('RequestCreate', {
    'title': fields.String(required=True),
    'category': fields.String(required=True),
    'justification': fields.String(required=True),
    'amount': fields.Float(required=True),
    'items': fields.List(fields.Nested(request_item_model)),
    'created_by_id': fields.Integer(required=True),  # to be replaced by JWT identity later
})

request_response_model = api.model('Request', {
    'id': fields.Integer,
    'title': fields.String,
    'category': fields.String,
    'justification': fields.String,
    'amount': fields.Float,
    'status': fields.String,
})


@api.route('/')
class RequestListResource(Resource):
    @api.marshal_list_with(request_response_model)
    def get(self):
        qs = ProcurementRequest.query.order_by(ProcurementRequest.created_at.desc()).all()
        return qs

    @api.expect(request_create_model, validate=True)
    @api.marshal_with(request_response_model, code=201)
    def post(self):
        payload = flask_request.get_json()
        req = ProcurementRequest(
            title=payload['title'],
            category=payload['category'],
            justification=payload['justification'],
            amount=payload['amount'],
            status=RequestStatus.SUBMITTED,
            created_by_id=payload['created_by_id'],
        )
        items = [
            RequestItem(
                description=i['description'],
                quantity=i['quantity'],
                unit_price=i['unit_price'],
            ) for i in payload.get('items', [])
        ]
        req.items = items
        db.session.add(req)
        db.session.commit()
        return req, 201