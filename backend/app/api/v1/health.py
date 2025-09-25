from flask_restx import Namespace, Resource

api = Namespace('health', description='Healthcheck endpoints')


@api.route('/healthz')
class HealthzResource(Resource):
    def get(self):
        return {'status': 'ok'}