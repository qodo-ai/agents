"""
Sample Python module demonstrating clean-code improvements.

Changes from the original:
- Removed unused imports and variables
- Eliminated duplicated logic by extracting helper function
- Introduced named constants for magic numbers
- Added type hints and docstrings
- Improved function and variable names
- Wrapped executable example in a main guard
- Added a dataclass to avoid long parameter list and kept a thin wrapper
  for backward compatibility with the original function signature
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

# Named constants (avoid magic numbers)
THRESHOLD: int = 10
MULTIPLIER: int = 2
BONUS: int = 5


def _transform_item(value: int) -> int:
    """Transform a single integer according to business rules.

    - If value > THRESHOLD, return value * MULTIPLIER + BONUS
    - Otherwise, return value * MULTIPLIER
    """
    if value > THRESHOLD:
        return value * MULTIPLIER + BONUS
    return value * MULTIPLIER


def transform_values(values: Iterable[int]) -> List[int]:
    """Apply the transformation to an iterable of integers.

    Args:
        values: Iterable of integers to transform.

    Returns:
        List of transformed integers.
    """
    return [_transform_item(v) for v in values]


# Backward-compatible wrapper with improved name kept alongside
# the original name for external callers.

def process_data(data_list: Iterable[int], flag: bool) -> List[int]:  # noqa: D401
    """Process a list of integers.

    Note: The `flag` parameter is retained for backward compatibility but is
    currently unused because the same transformation applies regardless of
    the flag value. It may be removed in a future version.
    """
    # The original implementation duplicated the same logic for True/False.
    # We unify the behavior and ignore `flag`.
    del flag  # explicitly mark as intentionally unused
    return transform_values(data_list)


# Dataclass to avoid a long parameter list for user creation
@dataclass(frozen=True)
class UserProfile:
    name: str
    email: str
    password: str
    age: int
    address: str
    phone_number: str
    country: str


def create_user_profile(profile: UserProfile) -> dict:
    """Create a user dictionary from a UserProfile.

    In a real application, this is where validation and persistence would occur.
    """
    print(f"Creating user {profile.name} from {profile.country}")
    return {"name": profile.name, "email": profile.email}


# Backward-compatible thin wrapper that preserves the original signature
# while delegating to the cleaner API based on the dataclass.

def create_user(
    name: str,
    email: str,
    password: str,
    age: int,
    address: str,
    phone_number: str,
    country: str,
) -> dict:
    """Backward-compatible wrapper for user creation.

    Prefer using `create_user_profile(UserProfile(...))` to avoid long
    parameter lists.
    """
    profile = UserProfile(
        name=name,
        email=email,
        password=password,
        age=age,
        address=address,
        phone_number=phone_number,
        country=country,
    )
    return create_user_profile(profile)


def _example_usage() -> None:
    values = [5, 15, 3, 25]
    processed = process_data(values, True)
    print(processed)


if __name__ == "__main__":
    _example_usage()
