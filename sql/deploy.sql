BEGIN;
ALTER TABLE `releases_release` ADD COLUMN `kids_title` varchar(255) NOT NULL after `meltwater_keywords`;
ALTER TABLE `releases_release` ADD COLUMN `kids_description` longtext NOT NULL after `kids_title`;
COMMIT;
-- Upgrade to django 1.3
BEGIN;
CREATE INDEX `django_session_c25c2c28` ON `django_session` (`expire_date`);
COMMIT;