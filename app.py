from flask import Flask, request, jsonify
from function import late_checkins, on_leave, non_checked_in, leave_trends
from summary import generate_leave_summary, generate_late_checkin_summary,generate_non_checked_in_summary,generate_leave_trend_summary
app = Flask(__name__)



@app.route('/late_checkins', methods=['POST'])
def analyze_late_checkins():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        analysis_result = late_checkins(data)
        final_summary = generate_late_checkin_summary(analysis_result)

        return jsonify(final_summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@app.route('/on_leave', methods=['POST'])
def analyze_on_leave():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        analysis_result = on_leave(data)
        final_summary = generate_leave_summary(analysis_result)

        return jsonify(final_summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500    


@app.route('/non_checked_in', methods=['POST'])
def analyze_non_checked_in():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        analysis_result = non_checked_in(data)
        final_summary = generate_non_checked_in_summary(analysis_result)
        return jsonify(final_summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route('/leave_trends', methods=['POST'])
def analyze_leave_trends():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        analysis_result = leave_trends(data)
        final_summary = generate_leave_trend_summary(analysis_result)
        return jsonify(final_summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500 
if __name__ == '__main__':
    app.run(debug=True,port=3000)
