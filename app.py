from flask import Flask, jsonify, abort, make_response, request
from models import routes


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/routes/", methods=["GET"])
def routes_list_api_v1():
    return jsonify(routes.all())


@app.route("/api/v1/routes/<int:route_id>", methods=["GET"])
def get_route(route_id):
    route = routes.get(route_id)
    if not route:
        abort(404)
    return jsonify({"route": route})


@app.route("/api/v1/routes/", methods=["POST"])
def add_route():
    if not request.json or not 'title' in request.json or not 'place' in request.json or not 'grade' in request.json:
        abort(400)
    route = {
        'id': routes.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'location': request.json.get('location', ""),
        'place': request.json['place'],
        'grade': request.json['grade'],
        'done': request.json.get('location', False)
    }
    routes.add(route)
    return jsonify({'route': route}), 201


@app.route("/api/v1/routes/<int:route_id>", methods=['DELETE'])
def delete_route(route_id):
    result = routes.delete(route_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/routes/<int:route_id>", methods=["PUT"])
def update_route(route_id):
    route = routes.get(route_id)
    if not route:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'location' in data and not isinstance(data.get('location'), str),
        'place' in data and not isinstance(data.get('place'), str),
        'grade' in data and not isinstance(data.get('grade'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    route = {
        'id': data.get('id', route['id']),
        'title': data.get('title', route['title']),
        'location': data.get('location', route['location']),
        'place': data.get('place', route['place']),
        'grade': data.get('grade', route['grade']),
        'done': data.get('done', route['done'])
    }
    routes.update(route_id, route)
    return jsonify({'route': route})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)
