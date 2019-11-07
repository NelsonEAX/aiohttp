--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10
-- Dumped by pg_dump version 10.10

-- Started on 2019-11-07 06:52:40

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12924)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2828 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 197 (class 1259 OID 16402)
-- Name: rule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rule (
    id bigint NOT NULL,
    rule text,
    comment text
);


ALTER TABLE public.rule OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 17061)
-- Name: tbl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl (
    id integer NOT NULL,
    val character varying(255)
);


ALTER TABLE public.tbl OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 17059)
-- Name: tbl_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbl_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbl_id_seq OWNER TO postgres;

--
-- TOC entry 2829 (class 0 OID 0)
-- Dependencies: 199
-- Name: tbl_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbl_id_seq OWNED BY public.tbl.id;


--
-- TOC entry 196 (class 1259 OID 16394)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id bigint NOT NULL,
    email text,
    password text,
    name text,
    surname text
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 16410)
-- Name: user_rule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_rule (
    id bigint NOT NULL,
    rule bigint,
    "user" bigint
);


ALTER TABLE public.user_rule OWNER TO postgres;

--
-- TOC entry 2684 (class 2604 OID 17064)
-- Name: tbl id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl ALTER COLUMN id SET DEFAULT nextval('public.tbl_id_seq'::regclass);


--
-- TOC entry 2817 (class 0 OID 16402)
-- Dependencies: 197
-- Data for Name: rule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rule (id, rule, comment) FROM stdin;
1	admin	Администратор системы
2	edit	Редактирование
3	view	Просмотр 
\.


--
-- TOC entry 2820 (class 0 OID 17061)
-- Dependencies: 200
-- Data for Name: tbl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbl (id, val) FROM stdin;
\.


--
-- TOC entry 2816 (class 0 OID 16394)
-- Dependencies: 196
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, email, password, name, surname) FROM stdin;
1	admin@example.com	abcd1234	Admin	Adminskiy
2	editor@example.com	12345678	Editor	Editorskiy
3	viewer@example.com	87654321	Viewer	Viewerskiy
5	abc2@mail.ru	abcd	\N	\N
6	abc3@mail.ru	abcd	\N	\N
4	abc1@mail.ru	abcd	\N	\N
7	abc@mail.ru	abcd	\N	\N
8	abc@mail4.ru	abcd	\N	\N
9	abc@mail9.ru	abcd	\N	\N
10	abc@mail10.ru	abcd	\N	\N
\.


--
-- TOC entry 2818 (class 0 OID 16410)
-- Dependencies: 198
-- Data for Name: user_rule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_rule (id, rule, "user") FROM stdin;
1	1	1
2	2	2
3	3	2
4	3	3
\.


--
-- TOC entry 2830 (class 0 OID 0)
-- Dependencies: 199
-- Name: tbl_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbl_id_seq', 1, false);


--
-- TOC entry 2686 (class 2606 OID 16426)
-- Name: user email_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT email_unique UNIQUE (email);


--
-- TOC entry 2690 (class 2606 OID 16409)
-- Name: rule rule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rule
    ADD CONSTRAINT rule_pkey PRIMARY KEY (id);


--
-- TOC entry 2694 (class 2606 OID 17066)
-- Name: tbl tbl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl
    ADD CONSTRAINT tbl_pkey PRIMARY KEY (id);


--
-- TOC entry 2688 (class 2606 OID 16401)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 2692 (class 2606 OID 16414)
-- Name: user_rule user_rule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_rule
    ADD CONSTRAINT user_rule_pkey PRIMARY KEY (id);


-- Completed on 2019-11-07 06:52:42

--
-- PostgreSQL database dump complete
--

