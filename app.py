from flask import Flask, jsonify
import csv
from collections import defaultdict

app = Flask(__name__)

def read_csv_and_convert_to_json():
    organization = defaultdict(list)

    with open('data.csv', mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            department = {
                "name": row["name"],
                "department": row["department"],
                "salary": int(row["salary"]),
                "office": row["office"],
                "isManager": row["isManager"] == "TRUE",
                "skills": [row["skill1"], row["skill2"], row["skill3"]]
            }
            organization[row["department"]].append(department)

    final_organization = {"organization": {"departments": []}}
    for department, employees in organization.items():
        manager = next((emp for emp in employees if emp["isManager"]), None)
        manager_name = manager["name"] if manager else ""
        department_object = {"name": department, "managerName": manager_name, "employees": employees}
        final_organization["organization"]["departments"].append(department_object)
        
    return final_organization

@app.route('/organization-chart', methods=['GET'])
def organization_chart():
    organization_chart_data = read_csv_and_convert_to_json()
    return jsonify(organization_chart_data)

@app.route('/me', methods=['GET'])
def about_me():
    me = {
        "name": "Yugam Goyal",
        "homepage": "https://www.linkedin.com/in/yugam-goyal/",
        "githubURL": "https://github.com/yugamgoyal",
        "interestingFact": "I love cooking different cuisines!",
        "skills": ["Python", "Java", "C++", "C", "JavaScript", "SQL", "HTML", "CSS", "...."]
    }
    return jsonify(me)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
