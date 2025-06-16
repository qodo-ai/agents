# Python Example

This example demonstrates how the Diff Test Suite Agent generates tests for Python code changes.

## Source Code Change

**File: `src/user_service.py`**
```python
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_user(self, username, email, age=None):
        """Create a new user with validation."""
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        
        if age is not None and (age < 0 or age > 150):
            raise ValueError("Age must be between 0 and 150")
        
        user_data = {
            'username': username,
            'email': email,
            'age': age,
            'created_at': datetime.now()
        }
        
        return self.db.insert('users', user_data)
    
    def _is_valid_email(self, email):
        """Private method to validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
```

## Generated Test Suite

**File: `tests/test_user_service.py`**
```python
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.user_service import UserService


class TestUserService:
    
    @pytest.fixture
    def mock_db(self):
        """Mock database connection for testing."""
        db = Mock()
        db.insert.return_value = {'id': 1, 'username': 'testuser'}
        return db
    
    @pytest.fixture
    def user_service(self, mock_db):
        """UserService instance with mocked database."""
        return UserService(mock_db)
    
    def test_create_user_valid_data(self, user_service, mock_db):
        """Test creating user with valid data."""
        result = user_service.create_user('testuser', 'test@example.com', 25)
        
        assert result == {'id': 1, 'username': 'testuser'}
        mock_db.insert.assert_called_once()
        
        # Verify the data passed to database
        call_args = mock_db.insert.call_args[0]
        assert call_args[0] == 'users'
        user_data = call_args[1]
        assert user_data['username'] == 'testuser'
        assert user_data['email'] == 'test@example.com'
        assert user_data['age'] == 25
        assert isinstance(user_data['created_at'], datetime)
    
    def test_create_user_without_age(self, user_service, mock_db):
        """Test creating user without age (optional parameter)."""
        result = user_service.create_user('testuser', 'test@example.com')
        
        assert result == {'id': 1, 'username': 'testuser'}
        call_args = mock_db.insert.call_args[0]
        user_data = call_args[1]
        assert user_data['age'] is None
    
    def test_create_user_invalid_username_empty(self, user_service):
        """Test creating user with empty username."""
        with pytest.raises(ValueError, match="Username must be at least 3 characters long"):
            user_service.create_user('', 'test@example.com')
    
    def test_create_user_invalid_username_too_short(self, user_service):
        """Test creating user with username too short."""
        with pytest.raises(ValueError, match="Username must be at least 3 characters long"):
            user_service.create_user('ab', 'test@example.com')
    
    def test_create_user_invalid_email_format(self, user_service):
        """Test creating user with invalid email format."""
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.create_user('testuser', 'invalid-email')
    
    def test_create_user_invalid_email_missing_domain(self, user_service):
        """Test creating user with email missing domain."""
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.create_user('testuser', 'test@')
    
    def test_create_user_invalid_age_negative(self, user_service):
        """Test creating user with negative age."""
        with pytest.raises(ValueError, match="Age must be between 0 and 150"):
            user_service.create_user('testuser', 'test@example.com', -1)
    
    def test_create_user_invalid_age_too_high(self, user_service):
        """Test creating user with age too high."""
        with pytest.raises(ValueError, match="Age must be between 0 and 150"):
            user_service.create_user('testuser', 'test@example.com', 151)
    
    def test_create_user_boundary_age_zero(self, user_service, mock_db):
        """Test creating user with age at lower boundary (0)."""
        result = user_service.create_user('testuser', 'test@example.com', 0)
        assert result == {'id': 1, 'username': 'testuser'}
    
    def test_create_user_boundary_age_max(self, user_service, mock_db):
        """Test creating user with age at upper boundary (150)."""
        result = user_service.create_user('testuser', 'test@example.com', 150)
        assert result == {'id': 1, 'username': 'testuser'}
    
    def test_create_user_minimum_valid_username(self, user_service, mock_db):
        """Test creating user with minimum valid username length."""
        result = user_service.create_user('abc', 'test@example.com')
        assert result == {'id': 1, 'username': 'testuser'}
    
    @patch('src.user_service.datetime')
    def test_create_user_timestamp_generation(self, mock_datetime, user_service, mock_db):
        """Test that created_at timestamp is properly generated."""
        fixed_time = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time
        
        user_service.create_user('testuser', 'test@example.com')
        
        call_args = mock_db.insert.call_args[0]
        user_data = call_args[1]
        assert user_data['created_at'] == fixed_time


class TestUserServicePrivateMethods:
    """Test private methods of UserService."""
    
    def test_is_valid_email_valid_formats(self):
        """Test email validation with various valid formats."""
        service = UserService(Mock())
        
        valid_emails = [
            'test@example.com',
            'user.name@domain.co.uk',
            'user+tag@example.org',
            'user123@test-domain.com',
            'a@b.co'
        ]
        
        for email in valid_emails:
            assert service._is_valid_email(email), f"Email {email} should be valid"
    
    def test_is_valid_email_invalid_formats(self):
        """Test email validation with various invalid formats."""
        service = UserService(Mock())
        
        invalid_emails = [
            'invalid-email',
            '@example.com',
            'user@',
            'user@domain',
            'user.domain.com',
            'user@domain.',
            'user name@domain.com',
            ''
        ]
        
        for email in invalid_emails:
            assert not service._is_valid_email(email), f"Email {email} should be invalid"
```

## Running the Tests

```bash
# Install dependencies
pip install pytest

# Run the generated tests
pytest tests/test_user_service.py -v

# Run with coverage
pytest tests/test_user_service.py --cov=src.user_service --cov-report=html
```

## Expected Output

```
tests/test_user_service.py::TestUserService::test_create_user_valid_data PASSED
tests/test_user_service.py::TestUserService::test_create_user_without_age PASSED
tests/test_user_service.py::TestUserService::test_create_user_invalid_username_empty PASSED
tests/test_user_service.py::TestUserService::test_create_user_invalid_username_too_short PASSED
tests/test_user_service.py::TestUserService::test_create_user_invalid_email_format PASSED
tests/test_user_service.py::TestUserService::test_create_user_invalid_email_missing_domain PASSED
tests/test_user_service.py::TestUserService::test_create_user_invalid_age_negative PASSED
tests/test_user_service.py::TestUserService::test_create_user_invalid_age_too_high PASSED
tests/test_user_service.py::TestUserService::test_create_user_boundary_age_zero PASSED
tests/test_user_service.py::TestUserService::test_create_user_boundary_age_max PASSED
tests/test_user_service.py::TestUserService::test_create_user_minimum_valid_username PASSED
tests/test_user_service.py::TestUserService::test_create_user_timestamp_generation PASSED
tests/test_user_service.py::TestUserServicePrivateMethods::test_is_valid_email_valid_formats PASSED
tests/test_user_service.py::TestUserServicePrivateMethods::test_is_valid_email_invalid_formats PASSED

========================= 14 passed in 0.12s =========================
```

## Agent Output

```json
{
  "summary": "Generated 14 test cases covering the UserService.create_user method and _is_valid_email helper. Tests include positive cases, error conditions, boundary values, and edge cases. All tests pass successfully with 100% coverage of the modified code.",
  "generated_tests": [
    "tests/test_user_service.py"
  ],
  "test_results": {
    "passed": 14,
    "failed": 0,
    "failures": []
  },
  "success": true
}
```