-- V001__add_user_email_column.sql
-- Safe migration example: Adding new column with index
-- Risk Level: SAFE

-- Add new email column
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- Create index for performance
CREATE INDEX idx_users_email ON users(email);

-- Add constraint for data integrity
ALTER TABLE users ADD CONSTRAINT chk_email_format 
    CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Update existing records with default value
UPDATE users SET email = 'user@example.com' WHERE email IS NULL;
