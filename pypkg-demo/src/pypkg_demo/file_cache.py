import os
import json
import datetime
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class FileCache:
    def __init__(self, file: str, ttl: int = 0) -> None:
        """Initialize FileCache with a file path and optional TTL.

        Args:
            file: Path to the JSON file
            ttl: Time to live in seconds (0 means no expiration)
        """
        self.file = file
        self.ttl = ttl
        self.data = self.load()

    def load(self) -> Dict:
        """Load the data from a file, or create a new one if it doesn't exist."""
        try:
            if not os.path.exists(self.file):
                return {}
            with open(self.file, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading file: {e}")
            return {}

    def save(self) -> None:
        """Save the data to a file."""
        try:
            os.makedirs(os.path.dirname(self.file), exist_ok=True)
            with open(self.file, 'w') as file:
                json.dump(self.data, file)
        except IOError as e:
            logger.error(f"Error saving file: {e}")

    def set(self, key: str, value: Any) -> None:
        """Set the value of the given key with optional expiration.

        Args:
            key: The key to set
            value: The value to store
        """
        if self.ttl > 0:
            expires_at = (datetime.datetime.now() +
                         datetime.timedelta(seconds=self.ttl)).isoformat()
        else:
            expires_at = None

        self.data[key] = {'value': value, 'expires_at': expires_at}
        self.cleanup()
        self.save()

    def get(self, key: str, default: Any = None) -> Any:
        """Get the value of the given key.

        Args:
            key: The key to retrieve
            default: Value to return if key doesn't exist or is expired

        Returns:
            The value associated with the key or default if not found/expired
        """
        if not self.has(key):
            return default

        entry = self.data[key]
        if self._is_expired(entry):
            del self.data[key]
            self.save()
            return default

        return entry['value']

    def has(self, key: str) -> bool:
        """Check if the given key exists and is not expired."""
        return key in self.data and not self._is_expired(self.data[key])

    def _is_expired(self, entry: Dict) -> bool:
        """Check if an entry is expired."""
        if not entry['expires_at']:
            return False
        return datetime.datetime.fromisoformat(entry['expires_at']) < datetime.datetime.now()

    def cleanup(self) -> None:
        """Remove expired entries from the dictionary."""
        if self.ttl == 0:
            return

        expired_keys = [key for key, value in self.data.items()
                       if self._is_expired(value)]
        for key in expired_keys:
            del self.data[key]
