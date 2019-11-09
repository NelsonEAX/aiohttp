--
-- PostgreSQL table dump
--

CREATE TABLE public.rule (
    id serial NOT NULL,
    rule text,
    comment text
);

ALTER TABLE public.rule OWNER TO postgres;

CREATE TABLE public."user" (
    id serial NOT NULL,
    email text,
    password text,
    name text,
    surname text,
    create_at timestamp(6) without time zone,
    delete_at timestamp(6) without time zone
);

ALTER TABLE public."user" OWNER TO postgres;

CREATE TABLE public.user_rule (
    id serial NOT NULL,
    rule bigint,
    "user" bigint
);

ALTER TABLE public.user_rule OWNER TO postgres;

INSERT INTO public.rule (id, rule, comment) VALUES (1, 'admin', 'Администратор системы');
INSERT INTO public.rule (id, rule, comment) VALUES (2, 'edit', 'Редактирование');
INSERT INTO public.rule (id, rule, comment) VALUES (3, 'view', 'Просмотр ');

INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (1, 'admin@example.com', 'abcd1234', 'Admin', 'Adminskiy', '2013-11-03 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (2, 'editor@example.com', '12345678', 'Editor', 'Editorskiy', '2013-11-04 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (3, 'viewer@example.com', '87654321', 'Viewer', 'Viewerskiy', '2013-11-05 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (10, 'abc@mail10.ru', 'abcd', NULL, NULL, '2017-11-03 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (4, 'abc1@mail.ru', 'abcd', NULL, NULL, '2017-11-03 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (6, 'abc3@mail.ru', 'abcd', NULL, NULL, '2017-11-03 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (7, 'abc@mail.ru', 'abcd', NULL, NULL, '2017-11-03 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (8, 'abc@mail4.ru', 'abcd', NULL, NULL, '2017-11-03 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (9, 'abc@mail9.ru', 'abcd', NULL, NULL, '2017-11-03 00:00:00', NULL);
INSERT INTO public."user" (id, email, password, name, surname, create_at, delete_at) VALUES (5, 'abc2@mail.ru', 'abcd', NULL, NULL, '2017-11-03 00:00:00', NULL);

INSERT INTO public.user_rule (id, rule, "user") VALUES (1, 1, 1);
INSERT INTO public.user_rule (id, rule, "user") VALUES (2, 2, 2);
INSERT INTO public.user_rule (id, rule, "user") VALUES (3, 3, 2);
INSERT INTO public.user_rule (id, rule, "user") VALUES (4, 3, 3);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT email_unique UNIQUE (email);

ALTER TABLE ONLY public.rule
    ADD CONSTRAINT rule_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.user_rule
    ADD CONSTRAINT user_rule_pkey PRIMARY KEY (id);

BEGIN;
    SELECT setval(pg_get_serial_sequence('"user"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "user";
    SELECT setval(pg_get_serial_sequence('"rule"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "rule";
    SELECT setval(pg_get_serial_sequence('"user_rule"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "user_rule";
COMMIT;