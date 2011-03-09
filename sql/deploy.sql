BEGIN;

DROP TABLE IF EXISTS `media_imagecolor`;

CREATE TABLE `media_imagecolor` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `color_id` varchar(10) NOT NULL,
    `image_id` varchar(50) NOT NULL,
    `ratio` double precision NOT NULL
)
;
ALTER TABLE `media_imagecolor` ADD CONSTRAINT `color_id_refs_id_f581a077` FOREIGN KEY (`color_id`) REFERENCES `media_color` (`id`);
ALTER TABLE `media_imagecolor` ADD CONSTRAINT `image_id_refs_id_cf48f20d` FOREIGN KEY (`image_id`) REFERENCES `media_image` (`id`);

COMMIT;
