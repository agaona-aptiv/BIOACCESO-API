from flask import url_for
from flask_restx import Api

from .bioaccess import namespace as bioaccess_namespace

# TODO: temp fix for https://github.com/noirbizarre/flask-restplus/issues/223
class ApiSwaggerFix(Api):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=False)

api = ApiSwaggerFix(
    title='CIDEC Bioaccess API',
    version='1.54',
    description='API to provide support to BIOACCESS devices',
)

api.add_namespace(bioaccess_namespace)

#Final Updatable Version