#####
## look at crontab . it run 


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ast
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime, timezone

# ====== HTTP Ayarları ======
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HASH_URL = "https://gmit-repo.gm.com/sa-tools/scripts/output/patch/current_schedule/schedule_hash"  # senin URL
PROXIES = {
    "http": "",
    "https": "",
}
HTTP_TIMEOUT = 30  # saniye

# ====== DB Settings ======
DB_CONFIG = {
    "host": "localhost",
    "database": "mydb",
    "user": "admin",
    "password": "Deneme123!",
    "port": 5532,
}

# ====== Functions ======
def normalize_ts(utc_str: str) -> str:
    """
    '2026-01-01 08:00:00 UTC' -> '2026-01-01 08:00:00+00:00'
    """
    if utc_str is None:
        return None
    s = utc_str.strip()
    if s.endswith(" UTC"):
        return s.replace(" UTC", "+00:00")
    # Zaten timezone varsa dokunma (ör: +00:00)
    return s

def parse_ruby_hash(raw_text: str) -> dict:
    """
    Converts a Ruby-style hash string to a Python dict. 
    Captures both '=>' and HTML escape '=">' variants.
    """
    cleaned = raw_text.replace("=&gt;", ":").replace("=>", ":")
    try:
        data = ast.literal_eval(cleaned)
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Parse failed: {e}\nIncoming text start: {raw_text[:200]!r}")
    if not isinstance(data, dict):
        raise ValueError("he expected top-level structure should be a dict.")
    return data

def to_rows(data: dict):
    """
    Dict -> DB'ye uygun satırlar (parametre dict)
    Senin kolon mapping’in:
      server_name = dict key
      start_time  = arr[0]
      end_time    = arr[1]
      dry_run_status     = arr[2]
      patch_apply_status = arr[3]
      patch_window       = arr[4]
      ingested_time      = NOW() (DB side)
    """
    for server, arr in data.items():
        if not isinstance(arr, (list, tuple)) or len(arr) < 5:
            # Skip or raise missing/broken lines
            # I'm logging and skipping this part.
            print(f"[WARNING] {server} Unexpected data: {arr!r} — skipped")
            continue
        yield {
            "server_name": server,
            "start_time": normalize_ts(arr[0]),
            "end_time": normalize_ts(arr[1]),
            "dry_run_status": arr[2],
            "patch_apply_status": arr[3],
            "patch_window": arr[4],
        }

def insert_rows(rows):
    """
    Bulk insert into the schedule_hash table. 
    Since the table schema has no defaults/constraints, it's a direct INSERT.
    """
    sql_truncate = "TRUNCATE TABLE iaasinvp_p.schedule_hash;"
    sql_insert = """
    INSERT INTO iaasinvp_p.schedule_hash (
        server_name, start_time, end_time, dry_run_status, patch_apply_status, patch_window, ingested_time
    ) VALUES (
        %(server_name)s, %(start_time)s, %(end_time)s, %(dry_run_status)s, %(patch_apply_status)s, %(patch_window)s, NOW()
    )
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql_truncate)
                execute_batch(cur, sql_insert, list(rows), page_size=1000)
        print("[OK] TRUNCATE + reload completed.")
    finally:
        if conn is not None:
            conn.close()

def main():
    # 1) HTTP GET
    try:
        # verify=False: self-signed vb. durumlar için uyarı devre dışı
        resp = requests.get(HASH_URL, proxies=PROXIES, verify=False, timeout=HTTP_TIMEOUT)
    except requests.RequestException as e:
        print(f"[ERROR] HTTP request failer: {e}")
        return

    print(f"[INFO] HTTP status: {resp.status_code}")
    if resp.status_code != 200:
        print("[INFO] Not Response 200 , Don't import to DB.")
        return

    raw_text = resp.text.strip()
    if not raw_text:
        print("[INFO] Response body empty, Don't import to DB.")
        return

    # 2) Parse
    try:
        data = parse_ruby_hash(raw_text)
    except ValueError as e:
        print(f"[ERROR] Parsing error: {e}")
        return

    # 3) convert rows
    rows_iter = to_rows(data)
    rows_list = list(rows_iter)
    if not rows_list:
        print("[INFO] There are no any line ")
        return

    # 4) DB'ye yaz
    try:
        insert_rows(rows_list)
    except Exception as e:
        print(f"[ERROR] Error during the insert : {e}")

if __name__ == "__main__":
    main()
