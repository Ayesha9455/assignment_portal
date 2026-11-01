import os, json, datetime, urllib.request
import xml.etree.ElementTree as ET

def parse_tests(path="results.xml"):
    tests = []
    for tc in ET.parse(path).getroot().iter("testcase"):
        bad = tc.find("failure")
        if bad is None:
            bad = tc.find("error")
        tests.append({
            "name": tc.get("name"),
            "result": "failed" if bad is not None else "passed",
            "failure_message": bad.get("message") if bad is not None else None,
        })
    return tests

tests = parse_tests()
passed = sum(t["result"] == "passed" for t in tests)
failed = len(tests) - passed

report = {
    "repository": os.getenv("GITHUB_REPOSITORY"),
    "branch": os.getenv("GITHUB_REF_NAME"),
    "commit_sha": os.getenv("GITHUB_SHA"),
    "pipeline_run_id": os.getenv("GITHUB_RUN_ID"),
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "tests": tests,
    "summary": {"total": len(tests), "passed": passed, "failed": failed},
    "overall_status": "PASSED" if failed == 0 and tests else "FAILED",
}

with open("report.json", "w") as f:
    json.dump(report, f, indent=2)
with open("email_body.txt", "w") as f:
    f.write("Commit: %s\nResult: %s\nTotal: %d  Passed: %d  Failed: %d\n\n" %
            (report["commit_sha"], report["overall_status"], len(tests), passed, failed))
    for t in tests:
        f.write("- %s: %s %s\n" % (t["name"], t["result"], t["failure_message"] or ""))

url = os.environ["REPORT_URL"]
req = urllib.request.Request(url, data=json.dumps(report).encode(),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=30) as resp:
    print("Receiver responded:", resp.status)
