import requests

URL = "https://api.jebray.com/tools/cekban"
KEY = "JEBRAY_KEY_396baac9c584e592278ad4bbafc8ddd9"
HEADERS = {"X-API-Key": KEY, "Content-Type": "application/json"}

def req(path, method="POST", data=None):
    try:
        fn = requests.post if method == "POST" else requests.get
        res = fn(f"{URL}{path}", json=data, headers=HEADERS, timeout=30)
        return res.json(), res.status_code
    except Exception as e:
        return {"success": False, "error": str(e)}, 500

def main():
    print("\n====================================\n        JEBRAY BAN CHECK V3\n====================================")
    opt = input("1. Check MLBB ban status\n2. Check remaining points\n0. Exit\nPilihan: ").strip()

    if opt == "1":
        uid = input("Enter Player ID: ").strip()
        zid = input("Enter Zone ID  : ").strip()
        if not uid or not zid or not uid.isdigit() or not zid.isdigit():
            return print("[ERROR] Player ID dan Zone ID harus berupa angka!")
        
        print("\n[INFO] Sending ban status request...")
        res, code = req("/v3", "POST", {"player_id": uid, "zone_id": zid})
        
        if code == 200 and res.get("success"):
            print("\n========== BAN CHECK RESULT ==========")
            print(f"Player ID        : {res.get('player_id', '-')}")
            print(f"Zone ID          : {res.get('zone_id', '-')}")
            print(f"Nickname         : {res.get('nickname', '-')}")
            print(f"Ban Status       : {res.get('ban_status', '-')}")
            print(f"Ban Reason       : {res.get('ban_reason', '-')}")
            print(f"Points Deducted  : {res.get('points_deducted', 0)}")
            print(f"Remaining Points : {res.get('points_remaining', '-')}")
            print(f"Processing Time  : {res.get('processing_time', '-')}")
            print("======================================")
        else:
            print(f"\n[ERROR] Request failed. HTTP {code}\n{res}")

    elif opt == "2":
        print("\n[INFO] Checking remaining points...")
        res, code = req("/api/balance", "GET")
        
        if code == 200 and res.get("success"):
            print("\n========== API INFORMATION ==========")
            print(f"Name             : {res.get('name', '-')}")
            print(f"Remaining Points : {res.get('points_remaining', 0)}")
            print(f"Total Usage      : {res.get('total_usage', 0)}")
            print(f"Last Used        : {res.get('last_used', '-')}")
            print(f"Created At       : {res.get('created_at', '-')}")
            print("=====================================")
        else:
            print(f"\n[ERROR] Failed to check balance. HTTP {code}\n{res}")

if __name__ == "__main__":
    main()