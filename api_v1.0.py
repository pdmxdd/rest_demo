from flask import request
import json
from application_configuration.app_config import app, db

from models.dog import Dog

# error_dict is used when requests don't contain correct information, or point towards non-existing paths
error_dict = {"error": "not found"}


@app.route('/animals/api/v1.0/dogs/', methods=['GET'])
def api_get_dogs():
    """
    Request handler for GET /animals/api/v1.0/dogs

    :return: json containing all the dogs found in the dogs table of the animals DB
    """
    dogs_dict = {"dogs": []}
    dogs = Dog.query.all()
    for dog in dogs:
        dogs_dict["dogs"].append({"id": dog.id, "name": dog.name, "age": dog.age})
    return json.dumps(dogs_dict)


@app.route('/animals/api/v1.0/dogs/<int:dog_id>', methods=['GET'])
def api_get_dog_by_id(dog_id):
    """
    Request handler for GET /animals/api/v1.0/dogs/<id>

    :param dog_id: UID for requested dog resource
    :return: json containing the requested dog OR json containing that resource was not found
    """
    requested_dog = Dog.query.filter_by(id=dog_id).first()
    if requested_dog is None:
        return json.dumps(error_dict)
    else:
        return json.dumps({'id': requested_dog.id, 'name': requested_dog.name, 'age': requested_dog.age})


@app.route('/animals/api/v1.0/dogs/', methods=["POST"])
def api_post_new_dog():
    """
    Request handler for POST /animals/api/v1.0/dogs ---
    REQUEST must contain json {"name": "<dog_name>", "age": "<dog_age>"}

    :return: json containing id of new dog resource that was create OR json informing of error
    """
    if request.json is not None:
        if "age" in request.json.keys() and "name" in request.json.keys():
            new_dog = Dog(name=request.json["name"], age=request.json["age"])
            db.session.add(new_dog)
            db.session.commit()
            return json.dumps({"action": "created", "resource": "dog", "id": new_dog.id})
    return json.dumps(error_dict)


@app.route('/animals/api/v1.0/dogs/<int:dog_id>', methods=['PUT'])
def update_dog(dog_id):
    """
    Request handler for PUT /animals/api/v1.0/dogs/<id> --- REQUEST must contain json updating either dog name, or age

    :param dog_id: UID for dog resource to be updated
    :return: json containing successful update info OR json containing error message
    """
    if request.json is not None:
        dog = Dog.query.filter_by(id=str(dog_id)).first()
        if "name" in request.json.keys():
            dog.name = request.json["name"]
        if "age" in request.json.keys():
            dog.age = request.json["age"]
        db.session.add(dog)
        db.session.commit()
        return json.dumps({"action": "updated", "resource": "dog", "id": dog.id})
    return json.dumps(error_dict)


@app.route('/animals/api/v1.0/dogs/<int:dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    """
    Request handler for DELETE /animals/api/v1.0/dogs/<id>

    :param dog_id: UID for dog resource to be deleted
    :return: json containing successful delete info
    """
    dog = Dog.query.filter_by(id=str(dog_id)).first()
    db.session.delete(dog)
    db.session.commit()
    return json.dumps({"action": "deleted", "resource": "dog", "id": dog.id})


if __name__ == "__main__":
    from util.seed_db import drop_create
    drop_create()
    app.run(port=8080)
