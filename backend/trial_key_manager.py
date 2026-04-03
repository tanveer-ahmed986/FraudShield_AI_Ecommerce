"""
Trial API Key Management System
Tracks trial keys, expiration, and usage limits
"""

import json
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

class TrialKeyManager:
    """Manage trial API keys with expiration and usage tracking"""

    def __init__(self, storage_file: str = "trial_keys.json"):
        self.storage_file = Path(storage_file)
        self.keys = self._load_keys()

    def _load_keys(self) -> Dict:
        """Load trial keys from storage"""
        if self.storage_file.exists():
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_keys(self):
        """Save trial keys to storage"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.keys, f, indent=2)

    def generate_trial_key(
        self,
        email: str,
        duration_days: int = 30,
        request_limit: int = 1000
    ) -> str:
        """
        Generate a new trial API key

        Args:
            email: User email (for tracking)
            duration_days: Trial duration (default 30 days)
            request_limit: Max API requests (default 1000)

        Returns:
            Trial API key string
        """
        # Generate unique key
        key = f"TRIAL_{secrets.token_urlsafe(16)}"

        # Calculate expiration
        created_at = datetime.now()
        expires_at = created_at + timedelta(days=duration_days)

        # Store key info
        self.keys[key] = {
            "email": email,
            "created_at": created_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "duration_days": duration_days,
            "request_limit": request_limit,
            "requests_used": 0,
            "status": "active",
            "first_used_at": None,
            "last_used_at": None
        }

        self._save_keys()

        print(f"[OK] Trial key generated for {email}")
        print(f"   Key: {key}")
        print(f"   Expires: {expires_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Limit: {request_limit} requests")

        return key

    def validate_key(self, api_key: str) -> Dict:
        """
        Validate trial API key

        Returns:
            {
                "valid": bool,
                "reason": str (if invalid),
                "requests_remaining": int
            }
        """
        # Check if key exists
        if api_key not in self.keys:
            return {
                "valid": False,
                "reason": "Invalid API key"
            }

        key_info = self.keys[api_key]

        # Check if expired
        expires_at = datetime.fromisoformat(key_info["expires_at"])
        if datetime.now() > expires_at:
            key_info["status"] = "expired"
            self._save_keys()
            return {
                "valid": False,
                "reason": f"Trial expired on {expires_at.strftime('%Y-%m-%d')}"
            }

        # Check request limit
        if key_info["requests_used"] >= key_info["request_limit"]:
            key_info["status"] = "limit_reached"
            self._save_keys()
            return {
                "valid": False,
                "reason": f"Request limit ({key_info['request_limit']}) reached"
            }

        # Valid key
        requests_remaining = key_info["request_limit"] - key_info["requests_used"]

        return {
            "valid": True,
            "requests_remaining": requests_remaining,
            "expires_at": expires_at.isoformat()
        }

    def record_usage(self, api_key: str):
        """Record an API request for this key"""
        if api_key in self.keys:
            now = datetime.now().isoformat()

            # Update usage
            self.keys[api_key]["requests_used"] += 1
            self.keys[api_key]["last_used_at"] = now

            # Set first_used_at if not set
            if not self.keys[api_key]["first_used_at"]:
                self.keys[api_key]["first_used_at"] = now

            self._save_keys()

    def get_key_info(self, api_key: str) -> Optional[Dict]:
        """Get information about a trial key"""
        return self.keys.get(api_key)

    def list_all_keys(self) -> Dict:
        """List all trial keys (for admin dashboard)"""
        summary = {
            "total_keys": len(self.keys),
            "active": 0,
            "expired": 0,
            "limit_reached": 0,
            "total_requests": 0
        }

        for key_info in self.keys.values():
            summary["total_requests"] += key_info["requests_used"]

            status = key_info["status"]
            if status == "active":
                summary["active"] += 1
            elif status == "expired":
                summary["expired"] += 1
            elif status == "limit_reached":
                summary["limit_reached"] += 1

        return {
            "summary": summary,
            "keys": self.keys
        }

    def deactivate_key(self, api_key: str):
        """Manually deactivate a trial key"""
        if api_key in self.keys:
            self.keys[api_key]["status"] = "deactivated"
            self._save_keys()
            print(f"[OK] Key deactivated: {api_key}")

    def extend_trial(self, api_key: str, additional_days: int):
        """Extend trial period"""
        if api_key in self.keys:
            current_expires = datetime.fromisoformat(self.keys[api_key]["expires_at"])
            new_expires = current_expires + timedelta(days=additional_days)
            self.keys[api_key]["expires_at"] = new_expires.isoformat()
            self._save_keys()
            print(f"[OK] Trial extended to {new_expires.strftime('%Y-%m-%d')}")

    def increase_limit(self, api_key: str, additional_requests: int):
        """Increase request limit"""
        if api_key in self.keys:
            self.keys[api_key]["request_limit"] += additional_requests
            self._save_keys()
            new_limit = self.keys[api_key]["request_limit"]
            print(f"[OK] Request limit increased to {new_limit}")


# CLI Tool for managing trial keys
if __name__ == "__main__":
    import sys

    manager = TrialKeyManager()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python trial_key_manager.py generate <email>")
        print("  python trial_key_manager.py validate <key>")
        print("  python trial_key_manager.py info <key>")
        print("  python trial_key_manager.py list")
        print("  python trial_key_manager.py extend <key> <days>")
        print("  python trial_key_manager.py deactivate <key>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "generate":
        if len(sys.argv) < 3:
            print("Error: Email required")
            print("Usage: python trial_key_manager.py generate <email>")
            sys.exit(1)

        email = sys.argv[2]
        key = manager.generate_trial_key(email)

        print("\n" + "=" * 60)
        print("Copy this information to YOUR_TRIAL_API_KEY.txt:")
        print("=" * 60)
        print(f"Trial API Key: {key}")
        print(f"Email: {email}")
        print(f"Valid for: 30 days")
        print(f"Request Limit: 1,000 requests")
        print("=" * 60)

    elif command == "validate":
        if len(sys.argv) < 3:
            print("Error: API key required")
            sys.exit(1)

        api_key = sys.argv[2]
        result = manager.validate_key(api_key)

        print("\nValidation Result:")
        print(json.dumps(result, indent=2))

    elif command == "info":
        if len(sys.argv) < 3:
            print("Error: API key required")
            sys.exit(1)

        api_key = sys.argv[2]
        info = manager.get_key_info(api_key)

        if info:
            print("\nKey Information:")
            print(json.dumps(info, indent=2))
        else:
            print("Key not found")

    elif command == "list":
        all_keys = manager.list_all_keys()
        print("\nTrial Keys Summary:")
        print(json.dumps(all_keys["summary"], indent=2))
        print(f"\nTotal keys: {len(all_keys['keys'])}")

        if len(sys.argv) > 2 and sys.argv[2] == "--full":
            print("\nAll Keys:")
            print(json.dumps(all_keys["keys"], indent=2))

    elif command == "extend":
        if len(sys.argv) < 4:
            print("Error: API key and days required")
            print("Usage: python trial_key_manager.py extend <key> <days>")
            sys.exit(1)

        api_key = sys.argv[2]
        days = int(sys.argv[3])
        manager.extend_trial(api_key, days)

    elif command == "deactivate":
        if len(sys.argv) < 3:
            print("Error: API key required")
            sys.exit(1)

        api_key = sys.argv[2]
        manager.deactivate_key(api_key)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
