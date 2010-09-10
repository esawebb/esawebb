BEGIN;
ALTER TABLE products_calendar
ADD(
     `sale` bool NOT NULL,
     `price` numeric(8, 2) NOT NULL,
     `product_id` integer UNIQUE,
     `job` varchar(4) NOT NULL,
     `jsp` integer,
     `width` varchar(10) NOT NULL,
     `height` varchar(10) NOT NULL,
     `weight` varchar(10) NOT NULL
);

COMMIT;