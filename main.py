import requests

def generate_webhook(name, reg_no, email):
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {"name": name, "regNo": reg_no, "email": email}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["webhook"], response.json()["accessToken"]

def get_final_sql_query(reg_no):
    last_digit = int(reg_no.strip()[-1])
    
    if last_digit % 2 == 0:
        # Acropolis-Q2: Count of younger employees in the same department
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
        # Acropolis-Q1: Highest salary not on 1st of the month
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


def submit_query(webhook_url, token, sql_query):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, headers=headers, json={"finalQuery": sql_query.strip()})
    return response.status_code, response.text
