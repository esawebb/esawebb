BEGIN;
UPDATE pages_embeddedpagekey SET application='djangoplicity', page_key='djangoplicity.shop_right_column' where application='spacetelescope' and page_key='spacetelescope.shop_right_column'; 
COMMIT;