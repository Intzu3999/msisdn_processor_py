import os
from datetime import datetime, timedelta

VALID_EXTENSIONS = (".xlsx", ".csv", ".html")

def collect_recent_reports(result_folder="result", hours=1):
    collected = []
    cutoff = datetime.now() - timedelta(hours=hours)

    for fname in os.listdir(result_folder):
        if fname.endswith(VALID_EXTENSIONS):
            full_path = os.path.join(result_folder, fname)
            mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
            if mtime > cutoff:
                collected.append(full_path)
    return collected
