import json
from pathlib import Path


class UserStore:
  def __init__(self, snapshot_path: Path) -> None:
    """
    A simple in-memory store for user data, with JSON snapshot persistence.
    """
    self._users_by_id: dict[int, dict[str, str]] = {}
    self._next_id = 1
    self._snapshot_path = snapshot_path

  def load(self) -> None:
    """
    Load the JSON snapshot from disk.
    """
    try:
      raw = self._snapshot_path.read_text(encoding='utf-8')
      data = json.loads(raw)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
      self._users_by_id = {}
      self._next_id = 1
      data = {}
      return

    users = {}
    max_id = 0
    for key, value in data.items():
      try:
        user_id = int(key)
        first_name = value.get('first_name', '')
        last_name = value.get('last_name', '')
      except (TypeError, ValueError):
        continue

      users[user_id] = {'first_name': first_name, 'last_name': last_name}
      if user_id > max_id:
        max_id = user_id

    self._users_by_id = users
    self._next_id = max_id + 1 if max_id else 1

  def save(self) -> None:
    """
    Persist the current in-memory state to disk.
    """
    try:
      with open(self._snapshot_path, 'w', encoding='utf-8') as f:
        json.dump(self._users_by_id, f, indent=2, sort_keys=True)
        f.write('\n')
    except OSError:
      pass

  def get_users(self) -> dict[int, dict[str, str]]:
    """
    Return the entire users collection as a dictionary mapping user IDs to user records.
    """
    return self._users_by_id

  def get_user(self, user_id: int) -> dict[str, str] | None:
    """
    Return the user record for the given user ID, or None if the user does not exist.
    """
    user = self._users_by_id.get(user_id)
    if user is None:
      return None
    return {'id': str(user_id), 'first_name': user['first_name'], 'last_name': user['last_name']}

  def create_user(self, first_name: str, last_name: str) -> dict[str, str]:
    """
    Create a new user with the given first and last name, assign them a new unique ID, and return the user record.
    """
    user_id = self._next_id
    self._next_id += 1
    self._users_by_id[user_id] = {'first_name': first_name, 'last_name': last_name}
    return {'id': str(user_id), 'first_name': first_name, 'last_name': last_name}

  def update_user(self, user_id: int, first_name: str, last_name: str) -> bool:
    """
    Update the user record for the given user ID with the new first and last name.
    Return True if the update was successful, or False if the user does not exist.
    """
    if user_id not in self._users_by_id:
      return False
    self._users_by_id[user_id] = {'first_name': first_name, 'last_name': last_name}
    return True

  def delete_user(self, user_id: int) -> bool:
    """
    Delete the user record for the given user ID.
    Return True if the deletion was successful, or False if the user does not exist.
    """
    if user_id not in self._users_by_id:
      return False
    del self._users_by_id[user_id]
    return True


user_store = UserStore(Path(__file__).resolve().parent / 'snapshot.users.json')
