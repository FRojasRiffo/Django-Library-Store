BEGIN;
--
-- Create model Book
--
CREATE TABLE "shop_book" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "price" integer unsigned NOT NULL CHECK ("price" >= 0));
COMMIT;
