"""
Animation Calculator - Flask Backend
A simple calculator API with animated frontend
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for API requests


@app.route('/')
def index():
    """Serve the main calculator page"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"ok": True}), 200


@app.route('/calculate', methods=['POST'])
def calculate():
    """
    POST endpoint to perform calculations
    Accepts JSON: {"num1": number, "num2": number, "operator": "+|-|*|/|pow"}
    Returns: {"result": number}
    """
    try:
        data = request.get_json()
        
        # Validate request data
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        num1 = data.get('num1')
        num2 = data.get('num2')
        operator = data.get('operator')
        
        # Validate all required fields
        if num1 is None or num2 is None or operator is None:
            return jsonify({"error": "Missing required fields: num1, num2, operator"}), 400
        
        # Convert to floats for calculation
        try:
            num1 = float(num1)
            num2 = float(num2)
        except (ValueError, TypeError):
            return jsonify({"error": "num1 and num2 must be valid numbers"}), 400
        
        # Validate operator
        valid_operators = ['+', '-', '*', '/', 'pow']
        if operator not in valid_operators:
            return jsonify({"error": f"Invalid operator. Must be one of: {', '.join(valid_operators)}"}), 400
        
        # Perform calculation
        result = 0
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return jsonify({"error": "Division by zero is not allowed"}), 400
            result = num1 / num2
        elif operator == 'pow':
            result = num1 ** num2
        
        # Return result
        return jsonify({"result": result}), 200
    
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


def print_banner():
    """Print startup banner"""
    banner = """
    ╔════════════════════════════════════════════╗
    ║   Animation Calculator - Flask Backend     ║
    ║   Server starting on http://127.0.0.1:5000 ║
    ╚════════════════════════════════════════════╝
    """
    print(banner)


if __name__ == '__main__':
    print_banner()
    # Run development server
    app.run(debug=True, host='0.0.0.0', port=5000)
