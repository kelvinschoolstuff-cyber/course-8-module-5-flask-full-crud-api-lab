from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required."}), 400

    event_id = max((event.id for event in events), default=0) + 1
    event = Event(event_id, title.strip())
    events.append(event)
    return jsonify(event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = next((item for item in events if item.id == event_id), None)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} was not found."}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required."}), 400

    event.title = title.strip()
    return jsonify(event.to_dict()), 200

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = next((item for item in events if item.id == event_id), None)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} was not found."}), 404

    events.remove(event)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
