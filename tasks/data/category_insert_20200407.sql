
-- category

drop table if exists category;

create table category (category_no integer not null, category_name varchar(255), parent_no integer, depth integer not null, primary key (category_no));

INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (1, '스킨케어', null, 1); -- 1-100
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (2, '메이크업', null, 1); -- 101-200
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (3, '생활용품', null, 1); -- 201-300
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (4, '뷰티푸드', null, 1); -- 301-400
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (5, '남성', null, 1);    -- 401-500
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (6, '소품', null, 1);    -- 501-600
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (7, '크랜징폼', 1, 2);    -- 601-700
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (8, '클랜징 티슈', 1, 2);  -- 701-800
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (9, '립스틱', 2, 2);      -- 801-900
INSERT INTO category(category_no, category_name, parent_no, depth) VALUES (10, '립글로즈', 2, 2);   -- 901-1000