BEGIN;

-- 0002
CREATE TABLE `product_attributeoption` (
  `name` varchar(100) NOT NULL,
  `error_message` varchar(100) NOT NULL default 'Inavlid Entry',
  `sort_order` int(11) NOT NULL default '1',
  `validation` varchar(100) NOT NULL,
  `id` int(11) NOT NULL auto_increment,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `product_attributeoption_52094d6e` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=355 DEFAULT CHARSET=utf8;

INSERT INTO `product_attributeoption` VALUES ('Job', 'Invalid Entry', '1', 'product.utils.validation_simple', '1', ''), ('JSP', 'Invalid Entry', '1', 'product.utils.validation_integer', '2', '');
-- 0003
ALTER TABLE `product_productattribute` ADD COLUMN `option_id` integer NOT NULL AFTER `name`;
UPDATE `product_productattribute` SET option_id=1 WHERE name="Job";
UPDATE `product_productattribute` SET option_id=2 WHERE name="JSP";
-- 0004
ALTER TABLE `product_productattribute` DROP COLUMN `name`;
-- 0005
-- 0006
-- 0007/0008
ALTER TABLE product_discount_validProducts RENAME TO product_discount_valid_products;

-- 0009
CREATE TABLE `product_categoryattribute` (
  `category_id` int(11) NOT NULL,
  `languagecode` varchar(10) default NULL,
  `id` int(11) NOT NULL auto_increment,
  `value` varchar(255) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `product_categoryattribute_42dc49bc` (`category_id`),
  KEY `product_categoryattribute_2f3b0dc9` (`option_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- 0010
CREATE TABLE `product_discount_valid_categories` (
  `id` int(11) NOT NULL auto_increment,
  `discount_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `product_discount_valid_categories_discount_id_3c06d1e3_uniq` (`discount_id`,`category_id`),
  KEY `product_discount_valid_categories_5c536bf3` (`discount_id`),
  KEY `product_discount_valid_categories_42dc49bc` (`category_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


COMMIT;