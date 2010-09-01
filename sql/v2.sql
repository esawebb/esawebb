BEGIN;

DROP TABLE archives_announcement;
ALTER TABLE archives_book RENAME TO products_book;
ALTER TABLE archives_brochure RENAME TO products_brochure;
ALTER TABLE archives_calendar RENAME TO products_calendar;
ALTER TABLE archives_cdrom RENAME TO products_cdrom;
ALTER TABLE archives_conferenceposter RENAME TO products_conferenceposter;
ALTER TABLE archives_educationalmaterial RENAME TO products_educationalmaterial;
ALTER TABLE archives_exhibition RENAME TO products_exhibition;
ALTER TABLE archives_fitsimage RENAME TO products_fitsimage;
ALTER TABLE archives_kidsdrawing RENAME TO products_kidsdrawing;
ALTER TABLE archives_logo RENAME TO products_logo;
ALTER TABLE archives_merchandise RENAME TO products_merchandise;
ALTER TABLE archives_newsletter RENAME TO products_newsletter;
ALTER TABLE archives_onlineart RENAME TO products_onlineart;
ALTER TABLE archives_onlineartauthor RENAME TO products_onlineartauthor;
ALTER TABLE archives_postcard RENAME TO products_postcard;
ALTER TABLE archives_poster RENAME TO products_poster;
ALTER TABLE archives_presentation RENAME TO products_presentation;
ALTER TABLE archives_presskit RENAME TO products_presskit;
ALTER TABLE archives_slideshow RENAME TO products_slideshow;
ALTER TABLE archives_sticker RENAME TO products_sticker;
ALTER TABLE archives_technicaldocument RENAME TO products_technicaldocument;
ALTER TABLE archives_uservideo RENAME TO products_uservideo;

COMMIT;