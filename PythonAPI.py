from flask import Flask, jsonify, request

app=Flask(__name__)

#In a real application

data = [        {"id": 1, "name": "Apple"},
        {"id": 2, "name": "Banana"},
        {"id": 3, "name": "Orange"},
    ]

    # GET all items
@app.route('/items', methods=['GET'])
def get_items():
        return jsonify(data)

    # GET a single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
        item = next((item for item in data if item["id"] == item_id), None)
        if item:
            return jsonify(item)
        return jsonify({"message": "Item not found"}), 404

    # POST (create) a new item
@app.route('/items', methods=['POST'])
def create_item():
        new_item = request.get_json()
        if new_item and "name" in new_item:
            new_item["id"] = len(data) + 1  # Simple ID generation
            data.append(new_item)
            return jsonify(new_item), 201  # 201 Created
        return jsonify({"message": "Invalid item data"}), 400

    # PUT (update) an item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
        updated_data = request.get_json()
        item_index = next((i for i, item in enumerate(data) if item["id"] == item_id), None)
        if item_index is not None and updated_data and "name" in updated_data:
            data[item_index]["name"] = updated_data["name"]
            return jsonify(data[item_index])
        return jsonify({"message": "Item not found or invalid data"}), 404

    # DELETE an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
        global data # Declare data as global to modify it
        initial_len = len(data)
        data = [item for item in data if item["id"] != item_id]
        if len(data) < initial_len:
            return jsonify({"message": "Item deleted"}), 200
        return jsonify({"message": "Item not found"}), 404

if __name__ == '__main__':
        app.run(debug=True) 