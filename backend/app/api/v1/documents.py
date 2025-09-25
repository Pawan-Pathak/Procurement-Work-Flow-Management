from flask import request as flask_request
from flask_restx import Namespace, Resource, fields
from ...extensions import db
from ...models import Document
from ...services.storage import save_file, is_allowed

api = Namespace('documents', description='Document upload and management')

upload_response = api.model('Document', {
    'id': fields.Integer,
    'filename': fields.String,
    'content_type': fields.String,
    'storage_key': fields.String,
    'category': fields.String,
})


@api.route('/upload')
class DocumentUploadResource(Resource):
    @api.marshal_with(upload_response, code=201)
    def post(self):
        if 'file' not in flask_request.files:
            return {'message': 'No file provided'}, 400
        file = flask_request.files['file']
        if not file or file.filename == '':
            return {'message': 'Empty file'}, 400
        if not is_allowed(file.filename):
            return {'message': 'File type not allowed'}, 400
        category = flask_request.form.get('category', 'attachment')
        request_id = flask_request.form.get('request_id')
        uploaded_by_id = flask_request.form.get('uploaded_by_id')
        uploaded_by_id = flask_request.form.get('uploaded_by_id')
        doc = Document(
            request_id=int(request_id) if request_id else None,
            uploaded_by_id=int(uploaded_by_id),
            filename=file.filename,
            content_type=file.mimetype or 'application/octet-stream',
            storage_key=storage_key,
            category=category,
        )
        db.session.add(doc)
        db.session.commit()
        return doc, 201