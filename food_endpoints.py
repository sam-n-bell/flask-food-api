from __main__ import db, app
import cursor_utils
from flask import jsonify, abort, Response, request
from bson.objectid import ObjectId
from bson.errors import InvalidId
from bson.json_util import dumps, loads
from marshmallow_models import CreateFoodInputSchema, return_errors_str

create_food_schema = CreateFoodInputSchema()

foods_collection = db['foods']

@app.route('/foods', methods=['GET'])
def get_foods():
    try:
        category = request.args.get('category')
        name = request.args.get('name')
        results = None
        if name:
            results = foods_collection.find({'name': {'$regex': name}})
        elif category:
            results = foods_collection.find({'category': category})
        else:
            results = foods_collection.find()

        foods = list()
        for q in results:
            foods.append({'_id': str(q['_id']), 'name': q['name'], 'calories': q['calories']})

        return jsonify(foods=foods)
    except Exception as e:
        abort(500, description=str(e))
        

@app.route('/foods/<id>', methods=['GET'])
def get_food_by_id(id):
    try:
        q = foods_collection.find_one({'_id': ObjectId(id)})
        food = cursor_utils.convert_single_cursor_to_dict(q, ['_id', 'name', 'calories'])
        if food is None:
            abort(404, description='Resource not found')
        return jsonify(food)
    except InvalidId:
        abort(500, description="Invalid ObjectID")

@app.route('/foods', methods=['POST'])
def create_food():
    food = request.json
    errors = create_food_schema.validate(food)
    errors_str = return_errors_str(errors)
    if errors:
        abort(400, description=errors_str)
    foods_collection.insert_one(food)
    return Response(None, 201)

@app.route('/foods/<_id>', methods=['PATCH'])
def update_food(_id):
    try:
        food = request.json
        result = foods_collection.replace_one({"_id": ObjectId(_id)}, food)
        updated_count = result.matched_count
        if updated_count == 0:
            abort(404, description='Resource not found')
        else:
            return Response(None, 200)
    except InvalidId:
        abort(500, description="Invalid ObjectID")

@app.route('/foods/<_id>', methods=['DELETE'])
def delete_food(_id):
    try:
        result = foods_collection.delete_one({'_id': ObjectId(_id)})
        deleted_count = result.deleted_count
        if deleted_count == 0:
            abort(404, description='Resource not found')
        else:
            return Response(None, 200)
    except InvalidId:
        abort(500, description="Invalid ObjectID")