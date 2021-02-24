# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: BSD-2-Clause

import requests
import subprocess
from subprocess import check_output
from flask import Flask, request, render_template
from flask_restx import fields, Api, Resource, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix

AVAILABLE_FORMATS=['default', 'spdxtagvalue', 'spdxjson', 'json', 'yaml', 'html']
DEFAULT_FORMAT='default'

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='0.1', title='Tern API',
    description='API for tern tool'
)

ns = api.namespace('tern', description='Tern command operations')

tern_request = ns.model(
    'tern_request', 
    {
        'image': fields.String(required=True, description='Image name for inspection',
            example='debian:buster'),
        'format': fields.String(description='Format of the report',
            example='default', default='default'),
    },
)
parser = reqparse.RequestParser()
parser.add_argument('image', type=str, required=True)
parser.add_argument('format', type=str)

tern_response = tern_request.inherit(
    'tern_response',
    {
        'report': fields.Raw(description='Report of inspection'),
    }
)

def exec_tern(image, report_format):
    cmd = ['tern', '--driver', 'fuse', 'report', '-f', report_format, '-i', image]
    return check_output(cmd).decode('utf-8')

@ns.route('/inspect')
@ns.doc('execute_tern')
class Tern(Resource):
    @ns.expect(tern_request, validate=True)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error')
    @ns.marshal_with(tern_response)
    def post(self):
        args = parser.parse_args()
        report_format = args['format'] if args['format'] in AVAILABLE_FORMATS else DEFAULT_FORMAT
        return {
                'image': args['image'],
                'format': report_format,
                'report': exec_tern(args['image'], report_format),
        }

@app.route('/webui',methods = ['GET'])
def webui():
    return render_template("/index.html")

@app.route('/show',methods = ['POST'])
def show():
    url = request.url_root + '/tern/inspect'
    image = str(request.form.get('image'))
    report_format = str(request.form.get('format'))
    data = {
        'image': image,
        'format': report_format,
    }
    r = requests.post(url, json=data)
    result = r.json()
    return '<html><pre>' + result['report'] + '</pre></html>'

if __name__ == "__main__":
    app.run()
