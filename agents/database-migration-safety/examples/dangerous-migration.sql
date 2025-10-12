-- V002__remove_old_columns.sql
-- Dangerous migration example: Removing columns without proper safety measures
-- Risk Level: DANGEROUS

-- Remove old email column (potential data loss)
ALTER TABLE users DROP COLUMN old_email;

-- Remove temporary data column
ALTER TABLE users DROP COLUMN temp_data;

-- Remove unused index
DROP INDEX idx_users_old_email;

-- Remove foreign key constraint
ALTER TABLE orders DROP CONSTRAINT fk_orders_user_id;
