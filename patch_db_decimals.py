import os
import re

def sanitize_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # We will inject a helper function at the top
    helper = """
import decimal

def _sanitize_decimals(data):
    if isinstance(data, list):
        return [_sanitize_decimals(item) for item in data]
    elif isinstance(data, dict):
        return {k: _sanitize_decimals(v) for k, v in data.items()}
    elif isinstance(data, decimal.Decimal):
        return float(data)
    else:
        return data
"""

    if "_sanitize_decimals" not in content:
        content = content.replace("import mysql.connector", "import mysql.connector\n" + helper)
    
    # Now replace occurrences of `return data` with `return _sanitize_decimals(data)` where it's the result of fetchall or fetchone.
    # Actually it's easier to just do it wherever fetchall() or fetchone() is called!
    # Wait, in db.py:
    # data = cursor.fetchall() -> data = _sanitize_decimals(cursor.fetchall())
    # data = cursor.fetchone() -> data = _sanitize_decimals(cursor.fetchone())

    content = content.replace("data = cursor.fetchall()", "data = _sanitize_decimals(cursor.fetchall())")
    content = content.replace("data = cursor.fetchone()", "data = _sanitize_decimals(cursor.fetchone())")
    content = content.replace("user = cursor.fetchone()", "user = _sanitize_decimals(cursor.fetchone())")
    content = content.replace("stats = cursor.fetchone()", "stats = _sanitize_decimals(cursor.fetchone())")
    
    with open(filepath, "w") as f:
        f.write(content)
    
if __name__ == "__main__":
    sanitize_file("db.py")
    print("Patched db.py with _sanitize_decimals")
