from flask_restplus import fields

success_schema = {
    'status': fields.String(required=True),
    'msg': fields.String(required=True),
    # 'data': fields.Nested(),
}


error_schema = {
    'status': fields.String(required=True),
    'msg': fields.String(required=True),
    'errorCode': fields.String()
}
