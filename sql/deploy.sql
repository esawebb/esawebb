BEGIN;
CREATE TABLE `downloadable_downloadableproduct` (
    `product_id` integer NOT NULL PRIMARY KEY,
    `file` varchar(100) NOT NULL,
    `num_allowed_downloads` integer NOT NULL,
    `expire_minutes` integer NOT NULL,
    `active` bool NOT NULL
)
;
ALTER TABLE `downloadable_downloadableproduct` ADD CONSTRAINT `product_id_refs_id_4bf3b11d` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`);
CREATE TABLE `downloadable_downloadlink` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `downloadable_product_id` integer NOT NULL,
    `order_id` integer NOT NULL,
    `key` varchar(40) NOT NULL,
    `num_attempts` integer NOT NULL,
    `time_stamp` datetime NOT NULL,
    `active` bool NOT NULL
)
;
ALTER TABLE `downloadable_downloadlink` ADD CONSTRAINT `downloadable_product_id_refs_product_id_bce07835` FOREIGN KEY (`downloadable_product_id`) REFERENCES `downloadable_downloadableproduct` (`product_id`);
ALTER TABLE `downloadable_downloadlink` ADD CONSTRAINT `order_id_refs_id_5f70a170` FOREIGN KEY (`order_id`) REFERENCES `shop_order` (`id`);
CREATE INDEX `downloadable_downloadlink_61816c1c` ON `downloadable_downloadlink` (`downloadable_product_id`);
CREATE INDEX `downloadable_downloadlink_8337030b` ON `downloadable_downloadlink` (`order_id`);
COMMIT;
BEGIN;
CREATE TABLE `configurable_configurableproduct_option_group` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `configurableproduct_id` integer NOT NULL,
    `optiongroup_id` integer NOT NULL,
    UNIQUE (`configurableproduct_id`, `optiongroup_id`)
)
;
ALTER TABLE `configurable_configurableproduct_option_group` ADD CONSTRAINT `optiongroup_id_refs_id_fdec498d` FOREIGN KEY (`optiongroup_id`) REFERENCES `product_optiongroup` (`id`);
CREATE TABLE `configurable_configurableproduct` (
    `product_id` integer NOT NULL PRIMARY KEY,
    `create_subs` bool NOT NULL
)
;
ALTER TABLE `configurable_configurableproduct` ADD CONSTRAINT `product_id_refs_id_d7a04701` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`);
ALTER TABLE `configurable_configurableproduct_option_group` ADD CONSTRAINT `configurableproduct_id_refs_product_id_9a785fba` FOREIGN KEY (`configurableproduct_id`) REFERENCES `configurable_configurableproduct` (`product_id`);
CREATE TABLE `configurable_productvariation_options` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `productvariation_id` integer NOT NULL,
    `option_id` integer NOT NULL,
    UNIQUE (`productvariation_id`, `option_id`)
)
;
ALTER TABLE `configurable_productvariation_options` ADD CONSTRAINT `option_id_refs_id_23d6c970` FOREIGN KEY (`option_id`) REFERENCES `product_option` (`id`);
CREATE TABLE `configurable_productvariation` (
    `product_id` integer NOT NULL PRIMARY KEY,
    `parent_id` integer NOT NULL
)
;
ALTER TABLE `configurable_productvariation` ADD CONSTRAINT `product_id_refs_id_b61c4dc2` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`);
ALTER TABLE `configurable_productvariation` ADD CONSTRAINT `parent_id_refs_product_id_63bcd3c6` FOREIGN KEY (`parent_id`) REFERENCES `configurable_configurableproduct` (`product_id`);
ALTER TABLE `configurable_productvariation_options` ADD CONSTRAINT `productvariation_id_refs_product_id_55e6e722` FOREIGN KEY (`productvariation_id`) REFERENCES `configurable_productvariation` (`product_id`);
CREATE INDEX `configurable_productvariation_63f17a16` ON `configurable_productvariation` (`parent_id`);
COMMIT;
