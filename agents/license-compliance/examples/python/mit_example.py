#!/usr/bin/env python3
# /// script
# dependencies = [
#     "pydantic"
# ]
# ///

"""
A simple data validation example using MIT-licensed dependencies.

This script demonstrates data validation using Pydantic.
All dependencies used have MIT or compatible licenses.
"""

import json
from pydantic import BaseModel, validator
from typing import Optional, List


class User(BaseModel):
    """User model with validation."""
    id: int
    name: str
    email: str
    age: Optional[int] = None
    tags: List[str] = []
    
    @validator('email')
    def email_must_contain_at(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('age')
    def age_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('Age must be positive')
        return v


def validate_users(users_data: List[dict]) -> List[User]:
    """Validate a list of user data."""
    validated_users = []
    
    for user_data in users_data:
        try:
            user = User(**user_data)
            validated_users.append(user)
            print(f"✓ Valid user: {user.name}")
        except Exception as e:
            print(f"✗ Invalid user data: {e}")
    
    return validated_users


def main():
    """Main function to demonstrate data validation."""
    
    # Sample user data (some valid, some invalid)
    sample_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25, "tags": ["admin", "user"]},
        {"id": 2, "name": "Bob", "email": "invalid-email", "age": 30},  # Invalid email
        {"id": 3, "name": "Carol", "email": "carol@example.com", "age": -5},  # Invalid age
        {"id": 4, "name": "David", "email": "david@example.com", "tags": ["user"]},
    ]
    
    print("Validating user data...")
    valid_users = validate_users(sample_data)
    
    print(f"\nValidation complete. {len(valid_users)} valid users out of {len(sample_data)} total.")
    
    # Export valid users as JSON
    if valid_users:
        output = [user.dict() for user in valid_users]
        print("\nValid users JSON:")
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()