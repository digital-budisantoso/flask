from flask import Flask, jsonify, request
import os
import mongoservices
import mapservices
from flask_cors import cross_origin
from functools import wraps

AUTH0_DOMAIN = 'dev-s32eql6r5zsd0u3f.us.auth0.com'
API_AUDIENCE = 'https://santosoaris/api'
ALGORITHMS = ["RS256"]

app = Flask(__name__)
mongosvc = mongoservices.mongoservices()
mapsvc = mapservices.mapservices()

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False

@app.route('/')
def index():
    return jsonify({"Hallo": "Welcome to your Flask Application"})

@app.route('/api/menu')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def menu():
    return jsonify({"code": "1", "status": "OK", "menus":"menus"})

@app.route('/api/samples', methods=['POST'])
def save_sample():
    data = request.json
    return mongosvc.save_sample(data)	

@app.route('/api/findplace', methods=['GET'])
def find_place():
    args = request.args
    qry = args.get("qry")
    return mapsvc.findplace(qry)

@app.route('/api/route', methods=['POST'])
def find_route():
    data = request.json
    loc_1 = data.get('src')
    loc_2 = data.get('dst')
    return mapsvc.findroute(loc_1, loc_2)
	
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
