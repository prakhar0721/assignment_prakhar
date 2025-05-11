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
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {"name": name, "regNo": reg_no, "email": email}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["webhook"], response.json()["accessToken"]

# Function to fetch sql query basis on the even/odd last digit of the REG number.
def get_final_sql_query(reg_no):
    last_digit = int(reg_no.strip()[-1])
    
    # For even Registration number
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
    #  Condition for odd Registration number
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

# Function to submit query to the defined webhook with token
def submit_query(webhook_url, token, sql_query):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, headers=headers, json={"finalQuery": sql_query.strip()})
    return response.status_code, response.text
