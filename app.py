from flask import Flask, request, jsonify

from src.minerals import search_minerals, sync_minerals

app = Flask(__name__)

@app.route('/search_minerals', methods=['POST'])
def post_search_minerals():
    data = request.json
    search_filters = data.get('filters', {})
    search_text = data.get('search_text', '')

    try:
        minerals = search_minerals(search_filters, search_text)
        return jsonify({"success": True, "payload": minerals}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

        
@app.route('/sync_minerals', methods=['GET'])
def route_sync_minerals():
    # get text from params
    max = int(request.args.get('max', 10))
    # retrieve api to get data
    payload = sync_minerals(max)
    # convert and return data
    return jsonify({"payload": payload}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)