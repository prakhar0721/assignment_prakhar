from main import generate_webhook, get_final_sql_query, submit_query

test_cases = [
    {"name": "Prakhar", "regNo": "0827AL221100", "email": "prakharnamdev221037@acropolis.in"},
    {"name": "Jane Odd", "regNo": "REG12347", "email": "jane2@example.com"}
]

for case in test_cases:
    print(f"Running test for {case['regNo']}...")
    try:
        webhook_url, token = generate_webhook(case["name"], case["regNo"], case["email"])
        sql_query = get_final_sql_query(case["regNo"])
        status, response = submit_query(webhook_url, token, sql_query)
        print(f"Submitted for {case['regNo']} → Status: {status}, Response: {response}\n")
    except Exception as e:
        print(f"Test failed for {case['regNo']} → Error: {e}\n")


