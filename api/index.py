from flask import Flask, jsonify
from flask_cors import CORS
from api.routes import user_bp, auth_bp
from pymongo import MongoClient
from api.config import Config

app = Flask(__name__) 
CORS(app, origins=["https://flask-api-weld-ten.vercel.app", "http://localhost:5000"])

try:
    client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)  
    db = client[Config.MONGO_DB_NAME]
    app.config['MONGO_URI'] = client  
    print("Kết nối MongoDB thành công!")
except Exception as e:
    print(f"Lỗi kết nối MongoDB: {e}")
    exit(1) 

app.register_blueprint(user_bp, prefix='/api/user')
app.register_blueprint(auth_bp, prefix='/api/auth')

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Test endpoint is working!'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)

