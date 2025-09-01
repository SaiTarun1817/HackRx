import requests
import json
import time

url = "http://localhost:8000/hackrx/run"
headers = {
    "Authorization": "Bearer 31fc25012e9fc7527b7477d46c55f9fddbf1fe223cc61365879f50f1bb1dd574",
    "Content-Type": "application/json"
}
payload = {
    "documents": [
       r"C:\Users\bhara\OneDrive\Desktop\BAJAJ FINANCE HackRx 6.0 hackathon\docs\CHOTGDP23004V012223.pdf",
       r"C:\Users\bhara\OneDrive\Desktop\BAJAJ FINANCE HackRx 6.0 hackathon\docs\EDLHLGA23009V012223.pdf",
       r"C:\Users\bhara\OneDrive\Desktop\BAJAJ FINANCE HackRx 6.0 hackathon\docs\HDFHLIP23024V072223.pdf",
       r"C:\Users\bhara\OneDrive\Desktop\BAJAJ FINANCE HackRx 6.0 hackathon\docs\ICIHLIP22012V012223.pdf",
        r"C:\Users\bhara\OneDrive\Desktop\BAJAJ FINANCE HackRx 6.0 hackathon\docs\policy.pdf"
    ],
    "questions": [
     "Is knee replacement surgery covered?",
        "What is the policy’s coverage for a 45-year-old female with diabetes?", 
    ]
}

start_time = time.time()
response = requests.post(url, headers=headers, json=payload)
end_time = time.time()
elapsed = end_time - start_time

print("Status code:", response.status_code)
print(f"Total response time: {elapsed:.2f} seconds")

if response.status_code == 200:
    data = response.json()
    answers = data.get("answers", [])
    for i, ans in enumerate(answers):
        print(f"\n--- Question {i+1}: {payload['questions'][i]} ---")
        # Try to pretty-print the JSON answer if possible
        try:
            # Remove markdown code block if present
            ans_clean = ans.strip()
            if ans_clean.startswith("```json"):
                ans_clean = ans_clean[7:]
            if ans_clean.endswith("```"):
                ans_clean = ans_clean[:-3]
            ans_json = json.loads(ans_clean)
            print(json.dumps(ans_json, indent=2, ensure_ascii=False))
        except Exception:
            print(ans)
else:
    print("Error:", response.text)