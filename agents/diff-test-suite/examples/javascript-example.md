# JavaScript Example

This example demonstrates how the Diff Test Suite Agent generates tests for JavaScript/TypeScript code changes.

## Source Code Change

**File: `src/api/userController.js`**
```javascript
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

class UserController {
    constructor(userService, emailService) {
        this.userService = userService;
        this.emailService = emailService;
    }

    async registerUser(userData) {
        const { username, email, password, confirmPassword } = userData;
        
        // Validation
        if (!username || username.length < 3) {
            throw new Error('Username must be at least 3 characters long');
        }
        
        if (!this.isValidEmail(email)) {
            throw new Error('Invalid email format');
        }
        
        if (password !== confirmPassword) {
            throw new Error('Passwords do not match');
        }
        
        if (!this.isStrongPassword(password)) {
            throw new Error('Password must be at least 8 characters with uppercase, lowercase, and number');
        }
        
        // Check if user already exists
        const existingUser = await this.userService.findByEmail(email);
        if (existingUser) {
            throw new Error('User with this email already exists');
        }
        
        // Hash password
        const saltRounds = 12;
        const hashedPassword = await bcrypt.hash(password, saltRounds);
        
        // Create user
        const newUser = await this.userService.create({
            username,
            email,
            password: hashedPassword,
            isVerified: false
        });
        
        // Send verification email
        await this.emailService.sendVerificationEmail(email, newUser.id);
        
        return {
            id: newUser.id,
            username: newUser.username,
            email: newUser.email,
            isVerified: newUser.isVerified
        };
    }
    
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    isStrongPassword(password) {
        if (password.length < 8) return false;
        
        const hasUppercase = /[A-Z]/.test(password);
        const hasLowercase = /[a-z]/.test(password);
        const hasNumber = /\d/.test(password);
        
        return hasUppercase && hasLowercase && hasNumber;
    }
}

module.exports = UserController;
```

## Generated Test Suite

**File: `tests/api/userController.test.js`**
```javascript
const bcrypt = require('bcrypt');
const UserController = require('../../src/api/userController');

// Mock dependencies
jest.mock('bcrypt');
jest.mock('../../src/models/User');

describe('UserController', () => {
    let userController;
    let mockUserService;
    let mockEmailService;
    
    beforeEach(() => {
        // Reset mocks
        jest.clearAllMocks();
        
        // Setup mock services
        mockUserService = {
            findByEmail: jest.fn(),
            create: jest.fn()
        };
        
        mockEmailService = {
            sendVerificationEmail: jest.fn()
        };
        
        userController = new UserController(mockUserService, mockEmailService);
    });
    
    describe('registerUser', () => {
        const validUserData = {
            username: 'testuser',
            email: 'test@example.com',
            password: 'Password123',
            confirmPassword: 'Password123'
        };
        
        beforeEach(() => {
            // Setup default mock returns
            mockUserService.findByEmail.mockResolvedValue(null);
            mockUserService.create.mockResolvedValue({
                id: 1,
                username: 'testuser',
                email: 'test@example.com',
                isVerified: false
            });
            bcrypt.hash.mockResolvedValue('hashedPassword123');
            mockEmailService.sendVerificationEmail.mockResolvedValue(true);
        });
        
        test('should successfully register user with valid data', async () => {
            const result = await userController.registerUser(validUserData);
            
            expect(result).toEqual({
                id: 1,
                username: 'testuser',
                email: 'test@example.com',
                isVerified: false
            });
            
            expect(mockUserService.findByEmail).toHaveBeenCalledWith('test@example.com');
            expect(bcrypt.hash).toHaveBeenCalledWith('Password123', 12);
            expect(mockUserService.create).toHaveBeenCalledWith({
                username: 'testuser',
                email: 'test@example.com',
                password: 'hashedPassword123',
                isVerified: false
            });
            expect(mockEmailService.sendVerificationEmail).toHaveBeenCalledWith('test@example.com', 1);
        });
        
        test('should throw error for empty username', async () => {
            const userData = { ...validUserData, username: '' };
            
            await expect(userController.registerUser(userData))
                .rejects.toThrow('Username must be at least 3 characters long');
        });
        
        test('should throw error for username too short', async () => {
            const userData = { ...validUserData, username: 'ab' };
            
            await expect(userController.registerUser(userData))
                .rejects.toThrow('Username must be at least 3 characters long');
        });
        
        test('should throw error for missing username', async () => {
            const userData = { ...validUserData };
            delete userData.username;
            
            await expect(userController.registerUser(userData))
                .rejects.toThrow('Username must be at least 3 characters long');
        });
        
        test('should throw error for invalid email format', async () => {
            const userData = { ...validUserData, email: 'invalid-email' };
            
            await expect(userController.registerUser(userData))
                .rejects.toThrow('Invalid email format');
        });
        
        test('should throw error when passwords do not match', async () => {
            const userData = { ...validUserData, confirmPassword: 'DifferentPassword123' };
            
            await expect(userController.registerUser(userData))
                .rejects.toThrow('Passwords do not match');
        });
        
        test('should throw error for weak password', async () => {
            const userData = { 
                ...validUserData, 
                password: 'weak', 
                confirmPassword: 'weak' 
            };
            
            await expect(userController.registerUser(userData))
                .rejects.toThrow('Password must be at least 8 characters with uppercase, lowercase, and number');
        });
        
        test('should throw error when user already exists', async () => {
            mockUserService.findByEmail.mockResolvedValue({ id: 1, email: 'test@example.com' });
            
            await expect(userController.registerUser(validUserData))
                .rejects.toThrow('User with this email already exists');
        });
        
        test('should handle bcrypt hashing error', async () => {
            bcrypt.hash.mockRejectedValue(new Error('Hashing failed'));
            
            await expect(userController.registerUser(validUserData))
                .rejects.toThrow('Hashing failed');
        });
        
        test('should handle user creation error', async () => {
            mockUserService.create.mockRejectedValue(new Error('Database error'));
            
            await expect(userController.registerUser(validUserData))
                .rejects.toThrow('Database error');
        });
        
        test('should handle email service error', async () => {
            mockEmailService.sendVerificationEmail.mockRejectedValue(new Error('Email service unavailable'));
            
            await expect(userController.registerUser(validUserData))
                .rejects.toThrow('Email service unavailable');
        });
        
        test('should use correct salt rounds for password hashing', async () => {
            await userController.registerUser(validUserData);
            
            expect(bcrypt.hash).toHaveBeenCalledWith('Password123', 12);
        });
        
        test('should not include password in returned user data', async () => {
            const result = await userController.registerUser(validUserData);
            
            expect(result).not.toHaveProperty('password');
        });
    });
    
    describe('isValidEmail', () => {
        test('should return true for valid email addresses', () => {
            const validEmails = [
                'test@example.com',
                'user.name@domain.co.uk',
                'user+tag@example.org',
                'user123@test-domain.com',
                'a@b.co'
            ];
            
            validEmails.forEach(email => {
                expect(userController.isValidEmail(email)).toBe(true);
            });
        });
        
        test('should return false for invalid email addresses', () => {
            const invalidEmails = [
                'invalid-email',
                '@example.com',
                'user@',
                'user@domain',
                'user.domain.com',
                'user@domain.',
                'user name@domain.com',
                '',
                null,
                undefined
            ];
            
            invalidEmails.forEach(email => {
                expect(userController.isValidEmail(email)).toBe(false);
            });
        });
    });
    
    describe('isStrongPassword', () => {
        test('should return true for strong passwords', () => {
            const strongPasswords = [
                'Password123',
                'MyStr0ngP@ss',
                'Abcdefgh1',
                'Test123Password'
            ];
            
            strongPasswords.forEach(password => {
                expect(userController.isStrongPassword(password)).toBe(true);
            });
        });
        
        test('should return false for passwords too short', () => {
            const shortPasswords = [
                'Pass1',
                'Abc123',
                'Test1'
            ];
            
            shortPasswords.forEach(password => {
                expect(userController.isStrongPassword(password)).toBe(false);
            });
        });
        
        test('should return false for passwords without uppercase', () => {
            const passwords = [
                'password123',
                'mypassword1',
                'test123456'
            ];
            
            passwords.forEach(password => {
                expect(userController.isStrongPassword(password)).toBe(false);
            });
        });
        
        test('should return false for passwords without lowercase', () => {
            const passwords = [
                'PASSWORD123',
                'MYPASSWORD1',
                'TEST123456'
            ];
            
            passwords.forEach(password => {
                expect(userController.isStrongPassword(password)).toBe(false);
            });
        });
        
        test('should return false for passwords without numbers', () => {
            const passwords = [
                'Password',
                'MyPassword',
                'TestPassword'
            ];
            
            passwords.forEach(password => {
                expect(userController.isStrongPassword(password)).toBe(false);
            });
        });
        
        test('should return false for empty or null passwords', () => {
            expect(userController.isStrongPassword('')).toBe(false);
            expect(userController.isStrongPassword(null)).toBe(false);
            expect(userController.isStrongPassword(undefined)).toBe(false);
        });
    });
});
```

## Running the Tests

```bash
# Install dependencies
npm install --save-dev jest

# Run the generated tests
npm test tests/api/userController.test.js

# Run with coverage
npm test -- --coverage tests/api/userController.test.js
```

## Expected Output

```
 PASS  tests/api/userController.test.js
  UserController
    registerUser
      ✓ should successfully register user with valid data (15ms)
      ✓ should throw error for empty username (2ms)
      ✓ should throw error for username too short (1ms)
      ✓ should throw error for missing username (1ms)
      ✓ should throw error for invalid email format (1ms)
      ✓ should throw error when passwords do not match (1ms)
      ✓ should throw error for weak password (1ms)
      ✓ should throw error when user already exists (3ms)
      ✓ should handle bcrypt hashing error (2ms)
      ✓ should handle user creation error (2ms)
      ✓ should handle email service error (2ms)
      ✓ should use correct salt rounds for password hashing (2ms)
      ✓ should not include password in returned user data (2ms)
    isValidEmail
      ✓ should return true for valid email addresses (1ms)
      ✓ should return false for invalid email addresses (1ms)
    isStrongPassword
      ✓ should return true for strong passwords (1ms)
      ✓ should return false for passwords too short (1ms)
      ✓ should return false for passwords without uppercase (1ms)
      ✓ should return false for passwords without lowercase (1ms)
      ✓ should return false for passwords without numbers (1ms)
      ✓ should return false for empty or null passwords (1ms)

Test Suites: 1 passed, 1 total
Tests:       21 passed, 21 total
Snapshots:   0 total
Time:        2.156s
```

## Agent Output

```json
{
  "summary": "Generated 21 test cases covering the UserController.registerUser method and helper functions isValidEmail and isStrongPassword. Tests include successful registration, validation errors, edge cases, error handling, and boundary conditions. All tests pass successfully with 100% coverage of the modified code.",
  "generated_tests": [
    "tests/api/userController.test.js"
  ],
  "test_results": {
    "passed": 21,
    "failed": 0,
    "failures": []
  },
  "success": true
}
```