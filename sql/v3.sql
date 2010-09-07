BEGIN;
ALTER TABLE announcements_announcementimage MODIFY `announcement_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE announcements_announcementimage MODIFY `override_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE announcements_announcementimage MODIFY `archive_item_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE announcements_announcementvideo MODIFY `announcement_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE announcements_announcementvideo MODIFY `override_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE announcements_announcementvideo MODIFY `archive_item_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci;
COMMIT;