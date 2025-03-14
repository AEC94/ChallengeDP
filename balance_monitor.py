import duckdb
import requests
import json
import sys
from datetime import datetime

# Configuration
DUCKDB_PATH = 'deel_interview.duckdb'
SLACK_WEBHOOK_URL = ''
THRESHOLD_PERCENT = 50

def main():
    """
    Check for significant balance changes and send a Slack alert if found
    """
    print(f"[{datetime.now()}] Starting balance change check...")
    
    try:
        conn = duckdb.connect(DUCKDB_PATH, read_only=True)
        
        query = f"""
        WITH current_day AS (
            SELECT 
                organization_id,
                analyzed_date,
                daily_balance
            FROM fact_daily_balance
            WHERE analyzed_date = current_date
        ),
        previous_day AS (
            SELECT 
                organization_id,
                daily_balance
            FROM fact_daily_balance
            WHERE analyzed_date = current_date - interval '1 day'
        )
        SELECT
            c.organization_id,
            c.daily_balance as current_balance,
            p.daily_balance as previous_balance,
            ABS((c.daily_balance - p.daily_balance) / 
                CASE WHEN ABS(p.daily_balance) < 0.01 THEN 0.01 
                     ELSE ABS(p.daily_balance) END) * 100 AS percent_change
        FROM current_day c
        JOIN previous_day p ON c.organization_id = p.organization_id
        WHERE ABS((c.daily_balance - p.daily_balance) / 
                 CASE WHEN ABS(p.daily_balance) < 0.01 THEN 0.01 
                      ELSE ABS(p.daily_balance) END) * 100 > {THRESHOLD_PERCENT}
        ORDER BY percent_change DESC
        """
        
        df = conn.execute(query).fetchdf()
        conn.close()
        
        if df.empty:
            print("No significant balance changes detected")
            return 0
        
        print(f"Found {len(df)} organizations with significant balance changes")
        
        message = {
            "text": "🚨 Balance Change Alert 🚨",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🚨 Balance Change Alert 🚨"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{len(df)}* organizations have balance changes exceeding {THRESHOLD_PERCENT}%"
                    }
                }
            ]
        }
        
        # Here we would send the Slack alert (printing the repose instead)
        print(message)
        """ 
        response = requests.post(
            SLACK_WEBHOOK_URL,
            data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"Error sending Slack alert: {response.status_code}, {response.text}")
            return 1
        else:
            print(f"Slack alert sent successfully")
            return 0
        """
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())