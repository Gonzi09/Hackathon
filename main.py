import pandas as pd
from flask import Flask, request, jsonify, send_file
from io import BytesIO
from flask_cors import CORS

app = Flask('app')
CORS(app)  

tickets = [
    {"id": 1, "name": "Alicia Johnson", "issue": "Can't access mentorship portal"},
    {"id": 2, "name": "Fatima Ahmed", "issue": "Need resources for coding interview prep"},
]

@app.route("/api/tickets", methods=["GET"])
def get_tickets():
    """Return the list of tickets as a JSON response."""
    return jsonify(tickets)

@app.route("/api/submit_ticket", methods=["POST"])
def submit_ticket():
    """Submit a new ticket from the React frontend."""
    data = request.get_json()
    name = data.get("name")
    issue = data.get("issue")
    
    ticket_id = len(tickets) + 1
    tickets.append({"id": ticket_id, "name": name, "issue": issue})
    
    return jsonify({"message": "Ticket submitted successfully!"}), 200

@app.route("/api/delete_ticket/<int:id>", methods=["DELETE"])
def delete_ticket(id):
    """Delete a ticket by its ID."""
    global tickets
    tickets = [ticket for ticket in tickets if ticket["id"] != id]
    return jsonify({"message": "Ticket deleted successfully!"}), 200

@app.route("/download")
def download_tickets():
    """Generate and download the ticket list as an Excel file."""
    df = pd.DataFrame(tickets)
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Tickets")
    
    output.seek(0)  
    return send_file(output, as_attachment=True, download_name="tickets.xlsx", mimetype="application/vnd.ms-excel")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
