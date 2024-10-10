--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2024-10-10 12:40:35

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16399)
-- Name: citizen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.citizen (
    citizen_id integer NOT NULL,
    name character varying NOT NULL,
    address character varying NOT NULL,
    phone character varying NOT NULL
);


ALTER TABLE public.citizen OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16420)
-- Name: clinic; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clinic (
    clinic_id integer NOT NULL,
    address character varying NOT NULL
);


ALTER TABLE public.clinic OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16413)
-- Name: doctor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor (
    doctor_id integer NOT NULL,
    name character varying NOT NULL,
    phone character varying NOT NULL
);


ALTER TABLE public.doctor OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16427)
-- Name: doctor_clinic; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor_clinic (
    table_id integer NOT NULL,
    doctor_id integer NOT NULL,
    clinic_id integer NOT NULL
);


ALTER TABLE public.doctor_clinic OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16460)
-- Name: vaccination; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vaccination (
    vaccination_id integer NOT NULL,
    citizen_id integer NOT NULL,
    doctor_id integer NOT NULL,
    vaccine_id integer NOT NULL
);


ALTER TABLE public.vaccination OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16408)
-- Name: vaccine; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vaccine (
    vaccine_id integer NOT NULL,
    dosage integer NOT NULL
);


ALTER TABLE public.vaccine OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16445)
-- Name: vaccine_clinic; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vaccine_clinic (
    table_id integer NOT NULL,
    vaccine_id integer NOT NULL,
    clinic_id integer NOT NULL
);


ALTER TABLE public.vaccine_clinic OWNER TO postgres;

--
-- TOC entry 4877 (class 0 OID 16399)
-- Dependencies: 215
-- Data for Name: citizen; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.citizen (citizen_id, name, address, phone) FROM stdin;
1	Jeff	Kyiv, Random Street, 1	+380333333333
\.


--
-- TOC entry 4880 (class 0 OID 16420)
-- Dependencies: 218
-- Data for Name: clinic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinic (clinic_id, address) FROM stdin;
1	Kyiv, Random Clinic str. 1
2	Kyiv, Random Clinic str.2
\.


--
-- TOC entry 4879 (class 0 OID 16413)
-- Dependencies: 217
-- Data for Name: doctor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor (doctor_id, name, phone) FROM stdin;
1	Bob	+380123456789
2	Jeff	+380111111111
\.


--
-- TOC entry 4881 (class 0 OID 16427)
-- Dependencies: 219
-- Data for Name: doctor_clinic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor_clinic (table_id, doctor_id, clinic_id) FROM stdin;
1	1	1
2	1	2
3	2	1
\.


--
-- TOC entry 4883 (class 0 OID 16460)
-- Dependencies: 221
-- Data for Name: vaccination; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vaccination (vaccination_id, citizen_id, doctor_id, vaccine_id) FROM stdin;
2	1	2	2
1	1	1	1
\.


--
-- TOC entry 4878 (class 0 OID 16408)
-- Dependencies: 216
-- Data for Name: vaccine; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vaccine (vaccine_id, dosage) FROM stdin;
1	5
2	3
\.


--
-- TOC entry 4882 (class 0 OID 16445)
-- Dependencies: 220
-- Data for Name: vaccine_clinic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vaccine_clinic (table_id, vaccine_id, clinic_id) FROM stdin;
1	1	1
2	1	2
3	1	2
\.


--
-- TOC entry 4712 (class 2606 OID 16407)
-- Name: citizen citizen_phone; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.citizen
    ADD CONSTRAINT citizen_phone UNIQUE (phone);


--
-- TOC entry 4714 (class 2606 OID 16405)
-- Name: citizen citizen_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.citizen
    ADD CONSTRAINT citizen_pk PRIMARY KEY (citizen_id);


--
-- TOC entry 4720 (class 2606 OID 16426)
-- Name: clinic clinic_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic
    ADD CONSTRAINT clinic_pk PRIMARY KEY (clinic_id);


--
-- TOC entry 4718 (class 2606 OID 16419)
-- Name: doctor doctor_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor
    ADD CONSTRAINT doctor_pk PRIMARY KEY (doctor_id);


--
-- TOC entry 4722 (class 2606 OID 16431)
-- Name: doctor_clinic table_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_clinic
    ADD CONSTRAINT table_pk PRIMARY KEY (table_id);


--
-- TOC entry 4726 (class 2606 OID 16464)
-- Name: vaccination vaccination_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccination
    ADD CONSTRAINT vaccination_pk PRIMARY KEY (vaccination_id);


--
-- TOC entry 4724 (class 2606 OID 16449)
-- Name: vaccine_clinic vaccine_clinic_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccine_clinic
    ADD CONSTRAINT vaccine_clinic_pk PRIMARY KEY (table_id);


--
-- TOC entry 4716 (class 2606 OID 16412)
-- Name: vaccine vaccine_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccine
    ADD CONSTRAINT vaccine_pk PRIMARY KEY (vaccine_id);


--
-- TOC entry 4731 (class 2606 OID 16465)
-- Name: vaccination citizen_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccination
    ADD CONSTRAINT citizen_id FOREIGN KEY (citizen_id) REFERENCES public.citizen(citizen_id);


--
-- TOC entry 4727 (class 2606 OID 16432)
-- Name: doctor_clinic clinic_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_clinic
    ADD CONSTRAINT clinic_id FOREIGN KEY (clinic_id) REFERENCES public.clinic(clinic_id);


--
-- TOC entry 4729 (class 2606 OID 16450)
-- Name: vaccine_clinic clinic_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccine_clinic
    ADD CONSTRAINT clinic_id FOREIGN KEY (clinic_id) REFERENCES public.clinic(clinic_id);


--
-- TOC entry 4728 (class 2606 OID 16437)
-- Name: doctor_clinic doctor_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_clinic
    ADD CONSTRAINT doctor_id FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
-- TOC entry 4732 (class 2606 OID 16470)
-- Name: vaccination doctor_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccination
    ADD CONSTRAINT doctor_id FOREIGN KEY (doctor_id) REFERENCES public.doctor(doctor_id);


--
-- TOC entry 4730 (class 2606 OID 16455)
-- Name: vaccine_clinic vaccine_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccine_clinic
    ADD CONSTRAINT vaccine_id FOREIGN KEY (vaccine_id) REFERENCES public.vaccine(vaccine_id);


--
-- TOC entry 4733 (class 2606 OID 16475)
-- Name: vaccination vaccine_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccination
    ADD CONSTRAINT vaccine_id FOREIGN KEY (vaccine_id) REFERENCES public.vaccine(vaccine_id);


-- Completed on 2024-10-10 12:40:35

--
-- PostgreSQL database dump complete
--

