from flask import request, make_response
import json
from application_configuration.app_config import app, db

from models.dog import Dog

# error_dict is used when requests don't contain correct information, or point towards non-existing paths
error_dict = {"error": "not found"}


@app.route('/animals/api/v1.2/dogs', methods=['GET'])
def api_get_dogs_root():
    """
    Request handler for GET /animals/api/v1.2/dogs
    :return: HTTP STATUS 200 & json containing all the available URIs from this route
    """
    available_routes = {
        "GET /animals/api/v1.2/dogs/": {"description": "Return JSON representation of all Dogs in Dog table"},
        "GET /animals/api/v1.2/dogs/[id]": {"description": "Return JSON representation of Dog with specific id"},
        "PUT /animals/api/v1.2/dogs/[id]": {"accepts": "JSON",
                                            "description": "Update Dog at id with information included in supplied JSON"},
        "POST /animals/api/v1.2/dogs/": {"accepts": "JSON",
                                         "description": "Creates a new Dog with information included in supplied JSON"},
        "DELETE /animals/api/v1.2/dogs/[id]": {"description": "Deletes dog at id"}
    }
    return make_response(json.dumps(available_routes), 200)

@app.route('/animals/api/v1.2/dogs/', methods=['GET'])
def api_get_dogs():
    """
    Request handler for GET /animals/api/v1.2/dogs

    :return: HTTP STATUS 200 & json containing all the dogs found in the dogs table of the animals DB
    """
    dogs_dict = {"dogs": []}
    dogs = Dog.query.all()
    for dog in dogs:
        dogs_dict["dogs"].append({"id": dog.id, "name": dog.name, "age": dog.age})
    return make_response(json.dumps(dogs_dict), 200)


@app.route('/animals/api/v1.2/dogs/<int:dog_id>', methods=['GET'])
def api_get_dog_by_id(dog_id):
    """
    Request handler for GET /animals/api/v1.2/dogs/<id>

    :param dog_id: UID for requested dog resource
    :return: HTTP STATUS 200 & json containing the requested dog OR
    HTTP STATUS 404 & json containing that resource was not found
    """
    requested_dog = Dog.query.filter_by(id=dog_id).first()
    if requested_dog is None:
        return make_response(json.dumps(error_dict), 404)
    else:
        return make_response(json.dumps(
            {'id': requested_dog.id,
             'name': requested_dog.name,
             'age': requested_dog.age}),
            200)


@app.route('/animals/api/v1.2/dogs/', methods=["POST"])
def api_post_new_dog():
    """
    Request handler for POST /animals/api/v1.2/dogs ---
    REQUEST must contain json {"name": "<dog_name>", "age": "<dog_age>"}

    :return: HTTP STATUS 201 & json containing id of new dog resource that was create
    OR HTTP STATUS 400 & json informing of error
    """
    if request.json is not None:
        if "age" in request.json.keys() and "name" in request.json.keys():
            new_dog = Dog(name=request.json["name"], age=request.json["age"])
            db.session.add(new_dog)
            db.session.commit()
            return make_response(json.dumps({"action": "created", "resource": "dog", "id": new_dog.id}), 201)
    return make_response(json.dumps(error_dict), 400)


@app.route('/animals/api/v1.2/dogs/<int:dog_id>', methods=['PUT'])
def update_dog(dog_id):
    """
    Request handler for PUT /animals/api/v1.2/dogs/<id> --- REQUEST must contain json updating either dog name, or age

    :param dog_id: UID for dog resource to be updated
    :return: HTTP STATUS 200 & json containing successful update info
    OR HTTP STATUS 400 & json containing error message
    """
    if request.json is not None:
        dog = Dog.query.filter_by(id=str(dog_id)).first()
        if "name" in request.json.keys():
            dog.name = request.json["name"]
        if "age" in request.json.keys():
            dog.age = request.json["age"]
        db.session.add(dog)
        db.session.commit()
        return make_response(json.dumps({"action": "updated", "resource": "dog", "id": dog.id}), 200)
    return make_response(json.dumps(error_dict), 400)


@app.route('/animals/api/v1.2/dogs/<int:dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    """
    Request handler for DELETE /animals/api/v1.2/dogs/<id>

    :param dog_id: UID for dog resource to be deleted
    :return: HTTP STATUS 200 & json containing successful delete info
    """
    dog = Dog.query.filter_by(id=str(dog_id)).first()
    db.session.delete(dog)
    db.session.commit()
    return make_response(json.dumps({"action": "deleted", "resource": "dog", "id": dog.id}), 200)


if __name__ == "__main__":
    # app.debug = True
    from util.seed_db import drop_create
    drop_create()
    app.run(port=8080)
