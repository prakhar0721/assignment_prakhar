import requests

"""
main.py

Automatically:
1. Sends a POST request to generate a webhook and auth token.
2. Solves a SQL problem based on employee age and department.
3. Submits the final SQL query using the received webhook and token.

Runs on startup without user input.
"""

# Function to generate webhook
def generate_webhook(name, reg_no, email):
    try:
        url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
        payload = {"name": name, "regNo": reg_no, "email": email}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["webhook"], data["accessToken"]
    except requests.exceptions.RequestException as e:
        print("Error generating webhook:", e)
        raise
    except KeyError:
        print("Invalid response structure while generating webhook.")
        raise

# Function to fetch SQL query based on last digit of reg_no
def get_final_sql_query(reg_no):
    try:
        last_digit = int(reg_no.strip()[-1])
        if last_digit % 2 == 0:
            return """
            SELECT 
              e1.EMP_ID,
              e1.FIRST_NAME,
              e1.LAST_NAME,
              d.DEPARTMENT_NAME,
              COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
            FROM EMPLOYEE e1
            JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID
            LEFT JOIN EMPLOYEE e2 
              ON e1.DEPARTMENT = e2.DEPARTMENT 
             AND DATEDIFF(CURDATE(), e2.DOB) > DATEDIFF(CURDATE(), e1.DOB)
            GROUP BY e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME
            ORDER BY e1.EMP_ID DESC;
            """
        else:
            return """
            SELECT 
              p.AMOUNT AS SALARY,
              CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
              FLOOR(DATEDIFF(CURDATE(), e.DOB) / 365.25) AS AGE,
              d.DEPARTMENT_NAME
            FROM PAYMENTS p
            JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
            JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
            WHERE DAY(p.PAYMENT_TIME) != 1
            ORDER BY p.AMOUNT DESC
            LIMIT 1;
            """
    except (ValueError, IndexError):
        print("Invalid registration number format.")
        raise

# Function to submit query
def submit_query(webhook_url, token, sql_query):
    try:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        response = requests.post(webhook_url, headers=headers, json={"finalQuery": sql_query.strip()})
        response.raise_for_status()
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        print("Error submitting query:", e)
        raise
