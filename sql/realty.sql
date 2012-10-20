--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.auth_message OWNER TO postgres;

--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_message_id_seq OWNER TO postgres;

--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_message_id_seq', 1, false);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_permission_id_seq', 213, true);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_id_seq', 3, true);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 169, true);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_content_type_id_seq', 71, true);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Name: estatebase_beside; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_beside (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_beside OWNER TO postgres;

--
-- Name: estatebase_beside_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_beside_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_beside_id_seq OWNER TO postgres;

--
-- Name: estatebase_beside_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_beside_id_seq OWNED BY estatebase_beside.id;


--
-- Name: estatebase_beside_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_beside_id_seq', 12, true);


--
-- Name: estatebase_bid; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_bid (
    id integer NOT NULL,
    deleted boolean NOT NULL,
    client_id integer NOT NULL,
    estate_filter text,
    history_id integer,
    broker_id integer,
    agency_price_min integer,
    agency_price_max integer
);


ALTER TABLE public.estatebase_bid OWNER TO postgres;

--
-- Name: estatebase_bid_estate_types; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_bid_estate_types (
    id integer NOT NULL,
    bid_id integer NOT NULL,
    estatetype_id integer NOT NULL
);


ALTER TABLE public.estatebase_bid_estate_types OWNER TO postgres;

--
-- Name: estatebase_bid_estate_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_bid_estate_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_bid_estate_types_id_seq OWNER TO postgres;

--
-- Name: estatebase_bid_estate_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_bid_estate_types_id_seq OWNED BY estatebase_bid_estate_types.id;


--
-- Name: estatebase_bid_estate_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_bid_estate_types_id_seq', 12, true);


--
-- Name: estatebase_bid_estates; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_bid_estates (
    id integer NOT NULL,
    bid_id integer NOT NULL,
    estate_id integer NOT NULL
);


ALTER TABLE public.estatebase_bid_estates OWNER TO postgres;

--
-- Name: estatebase_bid_estates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_bid_estates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_bid_estates_id_seq OWNER TO postgres;

--
-- Name: estatebase_bid_estates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_bid_estates_id_seq OWNED BY estatebase_bid_estates.id;


--
-- Name: estatebase_bid_estates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_bid_estates_id_seq', 3, true);


--
-- Name: estatebase_bid_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_bid_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_bid_id_seq OWNER TO postgres;

--
-- Name: estatebase_bid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_bid_id_seq OWNED BY estatebase_bid.id;


--
-- Name: estatebase_bid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_bid_id_seq', 7, true);


--
-- Name: estatebase_bid_localities; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_bid_localities (
    id integer NOT NULL,
    bid_id integer NOT NULL,
    locality_id integer NOT NULL
);


ALTER TABLE public.estatebase_bid_localities OWNER TO postgres;

--
-- Name: estatebase_bid_localities_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_bid_localities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_bid_localities_id_seq OWNER TO postgres;

--
-- Name: estatebase_bid_localities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_bid_localities_id_seq OWNED BY estatebase_bid_localities.id;


--
-- Name: estatebase_bid_localities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_bid_localities_id_seq', 2, true);


--
-- Name: estatebase_bid_regions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_bid_regions (
    id integer NOT NULL,
    bid_id integer NOT NULL,
    region_id integer NOT NULL
);


ALTER TABLE public.estatebase_bid_regions OWNER TO postgres;

--
-- Name: estatebase_bid_regions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_bid_regions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_bid_regions_id_seq OWNER TO postgres;

--
-- Name: estatebase_bid_regions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_bid_regions_id_seq OWNED BY estatebase_bid_regions.id;


--
-- Name: estatebase_bid_regions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_bid_regions_id_seq', 2, true);


--
-- Name: estatebase_bidg; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_bidg (
    id integer NOT NULL,
    estate_id integer NOT NULL,
    estate_type_id integer NOT NULL,
    room_number character varying(10),
    year_built integer,
    floor integer,
    floor_count integer,
    elevator boolean NOT NULL,
    wall_construcion_id integer,
    exterior_finish_id integer,
    window_type_id integer,
    roof_id integer,
    heating_id integer,
    ceiling_height numeric(5,2),
    room_count integer,
    total_area numeric(7,2),
    used_area numeric(7,2),
    wall_finish_id integer,
    flooring_id integer,
    ceiling_id integer,
    interior_id integer,
    basic boolean NOT NULL,
    CONSTRAINT estatebase_bidg_floor_check CHECK ((floor >= 0)),
    CONSTRAINT estatebase_bidg_floor_count_check CHECK ((floor_count >= 0)),
    CONSTRAINT estatebase_bidg_room_count_check CHECK ((room_count >= 0)),
    CONSTRAINT estatebase_bidg_year_built_check CHECK ((year_built >= 0))
);


ALTER TABLE public.estatebase_bidg OWNER TO postgres;

--
-- Name: estatebase_bidg_documents; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_bidg_documents (
    id integer NOT NULL,
    bidg_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.estatebase_bidg_documents OWNER TO postgres;

--
-- Name: estatebase_bidg_documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_bidg_documents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_bidg_documents_id_seq OWNER TO postgres;

--
-- Name: estatebase_bidg_documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_bidg_documents_id_seq OWNED BY estatebase_bidg_documents.id;


--
-- Name: estatebase_bidg_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_bidg_documents_id_seq', 29, true);


--
-- Name: estatebase_bidg_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_bidg_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_bidg_id_seq OWNER TO postgres;

--
-- Name: estatebase_bidg_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_bidg_id_seq OWNED BY estatebase_bidg.id;


--
-- Name: estatebase_bidg_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_bidg_id_seq', 57, true);


--
-- Name: estatebase_ceiling; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_ceiling (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_ceiling OWNER TO postgres;

--
-- Name: estatebase_ceiling_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_ceiling_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_ceiling_id_seq OWNER TO postgres;

--
-- Name: estatebase_ceiling_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_ceiling_id_seq OWNED BY estatebase_ceiling.id;


--
-- Name: estatebase_ceiling_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_ceiling_id_seq', 8, true);


--
-- Name: estatebase_client; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_client (
    id integer NOT NULL,
    deleted boolean NOT NULL,
    name character varying(255) NOT NULL,
    client_type_id integer NOT NULL,
    origin_id integer,
    address character varying(255),
    note character varying(255),
    history_id integer,
    broker_id integer
);


ALTER TABLE public.estatebase_client OWNER TO postgres;

--
-- Name: estatebase_client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_client_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_client_id_seq OWNER TO postgres;

--
-- Name: estatebase_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_client_id_seq OWNED BY estatebase_client.id;


--
-- Name: estatebase_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_client_id_seq', 8, true);


--
-- Name: estatebase_clienttype; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_clienttype (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_clienttype OWNER TO postgres;

--
-- Name: estatebase_clienttype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_clienttype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_clienttype_id_seq OWNER TO postgres;

--
-- Name: estatebase_clienttype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_clienttype_id_seq OWNED BY estatebase_clienttype.id;


--
-- Name: estatebase_clienttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_clienttype_id_seq', 3, true);


--
-- Name: estatebase_comstatus; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_comstatus (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    status integer NOT NULL
);


ALTER TABLE public.estatebase_comstatus OWNER TO postgres;

--
-- Name: estatebase_comstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_comstatus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_comstatus_id_seq OWNER TO postgres;

--
-- Name: estatebase_comstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_comstatus_id_seq OWNED BY estatebase_comstatus.id;


--
-- Name: estatebase_comstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_comstatus_id_seq', 3, true);


--
-- Name: estatebase_contact; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_contact (
    id integer NOT NULL,
    client_id integer NOT NULL,
    contact_type_id integer NOT NULL,
    contact character varying(255) NOT NULL,
    updated timestamp with time zone,
    contact_state_id integer NOT NULL
);


ALTER TABLE public.estatebase_contact OWNER TO postgres;

--
-- Name: estatebase_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_contact_id_seq OWNER TO postgres;

--
-- Name: estatebase_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_contact_id_seq OWNED BY estatebase_contact.id;


--
-- Name: estatebase_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_contact_id_seq', 10, true);


--
-- Name: estatebase_contacthistory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_contacthistory (
    id integer NOT NULL,
    event_date timestamp with time zone NOT NULL,
    user_id integer,
    contact_state_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.estatebase_contacthistory OWNER TO postgres;

--
-- Name: estatebase_contacthistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_contacthistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_contacthistory_id_seq OWNER TO postgres;

--
-- Name: estatebase_contacthistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_contacthistory_id_seq OWNED BY estatebase_contacthistory.id;


--
-- Name: estatebase_contacthistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_contacthistory_id_seq', 11, true);


--
-- Name: estatebase_contactstate; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_contactstate (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_contactstate OWNER TO postgres;

--
-- Name: estatebase_contactstate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_contactstate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_contactstate_id_seq OWNER TO postgres;

--
-- Name: estatebase_contactstate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_contactstate_id_seq OWNED BY estatebase_contactstate.id;


--
-- Name: estatebase_contactstate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_contactstate_id_seq', 5, true);


--
-- Name: estatebase_contacttype; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_contacttype (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_contacttype OWNER TO postgres;

--
-- Name: estatebase_contacttype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_contacttype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_contacttype_id_seq OWNER TO postgres;

--
-- Name: estatebase_contacttype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_contacttype_id_seq OWNED BY estatebase_contacttype.id;


--
-- Name: estatebase_contacttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_contacttype_id_seq', 3, true);


--
-- Name: estatebase_document; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_document (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_document OWNER TO postgres;

--
-- Name: estatebase_document_estate_type_category; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_document_estate_type_category (
    id integer NOT NULL,
    document_id integer NOT NULL,
    estatetypecategory_id integer NOT NULL
);


ALTER TABLE public.estatebase_document_estate_type_category OWNER TO postgres;

--
-- Name: estatebase_document_estate_type_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_document_estate_type_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_document_estate_type_category_id_seq OWNER TO postgres;

--
-- Name: estatebase_document_estate_type_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_document_estate_type_category_id_seq OWNED BY estatebase_document_estate_type_category.id;


--
-- Name: estatebase_document_estate_type_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_document_estate_type_category_id_seq', 41, true);


--
-- Name: estatebase_document_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_document_id_seq OWNER TO postgres;

--
-- Name: estatebase_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_document_id_seq OWNED BY estatebase_document.id;


--
-- Name: estatebase_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_document_id_seq', 8, true);


--
-- Name: estatebase_driveway; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_driveway (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_driveway OWNER TO postgres;

--
-- Name: estatebase_driveway_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_driveway_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_driveway_id_seq OWNER TO postgres;

--
-- Name: estatebase_driveway_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_driveway_id_seq OWNED BY estatebase_driveway.id;


--
-- Name: estatebase_driveway_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_driveway_id_seq', 5, true);


--
-- Name: estatebase_electricity; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_electricity (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_electricity OWNER TO postgres;

--
-- Name: estatebase_electricity_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_electricity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_electricity_id_seq OWNER TO postgres;

--
-- Name: estatebase_electricity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_electricity_id_seq OWNED BY estatebase_electricity.id;


--
-- Name: estatebase_electricity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_electricity_id_seq', 6, true);


--
-- Name: estatebase_estate; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estate (
    id integer NOT NULL,
    deleted boolean NOT NULL,
    region_id integer NOT NULL,
    locality_id integer,
    microdistrict_id integer,
    street_id integer,
    estate_number character varying(10),
    origin_id integer,
    beside_id integer,
    beside_distance integer,
    saler_price integer,
    agency_price integer,
    estate_status_id integer NOT NULL,
    electricity_id integer,
    electricity_distance integer,
    watersupply_id integer,
    watersupply_distance integer,
    gassupply_id integer,
    gassupply_distance integer,
    sewerage_id integer,
    sewerage_distance integer,
    telephony_id integer,
    internet_id integer,
    driveway_id integer,
    driveway_distance integer,
    description text,
    comment text,
    history_id integer,
    contact_id integer,
    valid boolean NOT NULL,
    broker_id integer,
    estate_category_id integer NOT NULL,
    com_status_id integer,
    CONSTRAINT estatebase_estate_agency_price_check CHECK ((agency_price >= 0)),
    CONSTRAINT estatebase_estate_beside_distance_check CHECK ((beside_distance >= 0)),
    CONSTRAINT estatebase_estate_driveway_distance_check CHECK ((driveway_distance >= 0)),
    CONSTRAINT estatebase_estate_electricity_distance_check CHECK ((electricity_distance >= 0)),
    CONSTRAINT estatebase_estate_gassupply_distance_check CHECK ((gassupply_distance >= 0)),
    CONSTRAINT estatebase_estate_saler_price_check CHECK ((saler_price >= 0)),
    CONSTRAINT estatebase_estate_sewerage_distance_check CHECK ((sewerage_distance >= 0)),
    CONSTRAINT estatebase_estate_watersupply_distance_check CHECK ((watersupply_distance >= 0))
);


ALTER TABLE public.estatebase_estate OWNER TO postgres;

--
-- Name: estatebase_estate_estate_params; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estate_estate_params (
    id integer NOT NULL,
    estate_id integer NOT NULL,
    estateparam_id integer NOT NULL
);


ALTER TABLE public.estatebase_estate_estate_params OWNER TO postgres;

--
-- Name: estatebase_estate_estate_params_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estate_estate_params_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estate_estate_params_id_seq OWNER TO postgres;

--
-- Name: estatebase_estate_estate_params_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estate_estate_params_id_seq OWNED BY estatebase_estate_estate_params.id;


--
-- Name: estatebase_estate_estate_params_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estate_estate_params_id_seq', 23, true);


--
-- Name: estatebase_estate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estate_id_seq OWNER TO postgres;

--
-- Name: estatebase_estate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estate_id_seq OWNED BY estatebase_estate.id;


--
-- Name: estatebase_estate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estate_id_seq', 39, true);


--
-- Name: estatebase_estateclient; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estateclient (
    id integer NOT NULL,
    client_id integer NOT NULL,
    estate_id integer NOT NULL,
    estate_client_status_id integer NOT NULL
);


ALTER TABLE public.estatebase_estateclient OWNER TO postgres;

--
-- Name: estatebase_estateclient_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estateclient_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estateclient_id_seq OWNER TO postgres;

--
-- Name: estatebase_estateclient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estateclient_id_seq OWNED BY estatebase_estateclient.id;


--
-- Name: estatebase_estateclient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estateclient_id_seq', 21, true);


--
-- Name: estatebase_estateclientstatus; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estateclientstatus (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_estateclientstatus OWNER TO postgres;

--
-- Name: estatebase_estateclientstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estateclientstatus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estateclientstatus_id_seq OWNER TO postgres;

--
-- Name: estatebase_estateclientstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estateclientstatus_id_seq OWNED BY estatebase_estateclientstatus.id;


--
-- Name: estatebase_estateclientstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estateclientstatus_id_seq', 5, true);


--
-- Name: estatebase_estateparam; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estateparam (
    id integer NOT NULL,
    "order" integer NOT NULL,
    name character varying(100) NOT NULL,
    CONSTRAINT estatebase_estateparam_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.estatebase_estateparam OWNER TO postgres;

--
-- Name: estatebase_estateparam_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estateparam_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estateparam_id_seq OWNER TO postgres;

--
-- Name: estatebase_estateparam_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estateparam_id_seq OWNED BY estatebase_estateparam.id;


--
-- Name: estatebase_estateparam_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estateparam_id_seq', 6, true);


--
-- Name: estatebase_estatephoto; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estatephoto (
    id integer NOT NULL,
    "order" integer NOT NULL,
    estate_id integer NOT NULL,
    name character varying(100),
    note character varying(255),
    image character varying(100) NOT NULL,
    CONSTRAINT estatebase_estatephoto_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.estatebase_estatephoto OWNER TO postgres;

--
-- Name: estatebase_estatephoto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estatephoto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estatephoto_id_seq OWNER TO postgres;

--
-- Name: estatebase_estatephoto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estatephoto_id_seq OWNED BY estatebase_estatephoto.id;


--
-- Name: estatebase_estatephoto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estatephoto_id_seq', 21, true);


--
-- Name: estatebase_estateregister; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estateregister (
    id integer NOT NULL,
    deleted boolean NOT NULL,
    name character varying(255) NOT NULL,
    history_id integer,
    broker_id integer
);


ALTER TABLE public.estatebase_estateregister OWNER TO postgres;

--
-- Name: estatebase_estateregister_bids; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estateregister_bids (
    id integer NOT NULL,
    estateregister_id integer NOT NULL,
    bid_id integer NOT NULL
);


ALTER TABLE public.estatebase_estateregister_bids OWNER TO postgres;

--
-- Name: estatebase_estateregister_bids_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estateregister_bids_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estateregister_bids_id_seq OWNER TO postgres;

--
-- Name: estatebase_estateregister_bids_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estateregister_bids_id_seq OWNED BY estatebase_estateregister_bids.id;


--
-- Name: estatebase_estateregister_bids_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estateregister_bids_id_seq', 10, true);


--
-- Name: estatebase_estateregister_estates; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estateregister_estates (
    id integer NOT NULL,
    estateregister_id integer NOT NULL,
    estate_id integer NOT NULL
);


ALTER TABLE public.estatebase_estateregister_estates OWNER TO postgres;

--
-- Name: estatebase_estateregister_estates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estateregister_estates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estateregister_estates_id_seq OWNER TO postgres;

--
-- Name: estatebase_estateregister_estates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estateregister_estates_id_seq OWNED BY estatebase_estateregister_estates.id;


--
-- Name: estatebase_estateregister_estates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estateregister_estates_id_seq', 17, true);


--
-- Name: estatebase_estateregister_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estateregister_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estateregister_id_seq OWNER TO postgres;

--
-- Name: estatebase_estateregister_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estateregister_id_seq OWNED BY estatebase_estateregister.id;


--
-- Name: estatebase_estateregister_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estateregister_id_seq', 9, true);


--
-- Name: estatebase_estatestatus; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estatestatus (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_estatestatus OWNER TO postgres;

--
-- Name: estatebase_estatestatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estatestatus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estatestatus_id_seq OWNER TO postgres;

--
-- Name: estatebase_estatestatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estatestatus_id_seq OWNED BY estatebase_estatestatus.id;


--
-- Name: estatebase_estatestatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estatestatus_id_seq', 4, true);


--
-- Name: estatebase_estatetype; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estatetype (
    id integer NOT NULL,
    "order" integer NOT NULL,
    name character varying(100) NOT NULL,
    estate_type_category_id integer NOT NULL,
    note character varying(255),
    placeable boolean NOT NULL,
    template integer NOT NULL,
    CONSTRAINT estatebase_estatetype_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.estatebase_estatetype OWNER TO postgres;

--
-- Name: estatebase_estatetype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estatetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estatetype_id_seq OWNER TO postgres;

--
-- Name: estatebase_estatetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estatetype_id_seq OWNED BY estatebase_estatetype.id;


--
-- Name: estatebase_estatetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estatetype_id_seq', 50, true);


--
-- Name: estatebase_estatetypecategory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_estatetypecategory (
    id integer NOT NULL,
    "order" integer NOT NULL,
    name character varying(100) NOT NULL,
    independent boolean NOT NULL,
    has_bidg integer NOT NULL,
    has_stead integer NOT NULL,
    is_commerce boolean NOT NULL,
    CONSTRAINT estatebase_estatetypecategory_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.estatebase_estatetypecategory OWNER TO postgres;

--
-- Name: estatebase_estatetypecategory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_estatetypecategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_estatetypecategory_id_seq OWNER TO postgres;

--
-- Name: estatebase_estatetypecategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_estatetypecategory_id_seq OWNED BY estatebase_estatetypecategory.id;


--
-- Name: estatebase_estatetypecategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_estatetypecategory_id_seq', 8, true);


--
-- Name: estatebase_exteriorfinish; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_exteriorfinish (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_exteriorfinish OWNER TO postgres;

--
-- Name: estatebase_exteriorfinish_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_exteriorfinish_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_exteriorfinish_id_seq OWNER TO postgres;

--
-- Name: estatebase_exteriorfinish_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_exteriorfinish_id_seq OWNED BY estatebase_exteriorfinish.id;


--
-- Name: estatebase_exteriorfinish_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_exteriorfinish_id_seq', 10, true);


--
-- Name: estatebase_flooring; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_flooring (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_flooring OWNER TO postgres;

--
-- Name: estatebase_flooring_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_flooring_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_flooring_id_seq OWNER TO postgres;

--
-- Name: estatebase_flooring_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_flooring_id_seq OWNED BY estatebase_flooring.id;


--
-- Name: estatebase_flooring_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_flooring_id_seq', 8, true);


--
-- Name: estatebase_furniture; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_furniture (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_furniture OWNER TO postgres;

--
-- Name: estatebase_furniture_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_furniture_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_furniture_id_seq OWNER TO postgres;

--
-- Name: estatebase_furniture_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_furniture_id_seq OWNED BY estatebase_furniture.id;


--
-- Name: estatebase_furniture_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_furniture_id_seq', 3, true);


--
-- Name: estatebase_gassupply; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_gassupply (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_gassupply OWNER TO postgres;

--
-- Name: estatebase_gassupply_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_gassupply_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_gassupply_id_seq OWNER TO postgres;

--
-- Name: estatebase_gassupply_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_gassupply_id_seq OWNED BY estatebase_gassupply.id;


--
-- Name: estatebase_gassupply_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_gassupply_id_seq', 6, true);


--
-- Name: estatebase_geogroup; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_geogroup (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_geogroup OWNER TO postgres;

--
-- Name: estatebase_geogroup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_geogroup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_geogroup_id_seq OWNER TO postgres;

--
-- Name: estatebase_geogroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_geogroup_id_seq OWNED BY estatebase_geogroup.id;


--
-- Name: estatebase_geogroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_geogroup_id_seq', 4, true);


--
-- Name: estatebase_heating; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_heating (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_heating OWNER TO postgres;

--
-- Name: estatebase_heating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_heating_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_heating_id_seq OWNER TO postgres;

--
-- Name: estatebase_heating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_heating_id_seq OWNED BY estatebase_heating.id;


--
-- Name: estatebase_heating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_heating_id_seq', 4, true);


--
-- Name: estatebase_historymeta; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_historymeta (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    created_by_id integer NOT NULL,
    updated timestamp with time zone,
    updated_by_id integer,
    modificated timestamp with time zone NOT NULL
);


ALTER TABLE public.estatebase_historymeta OWNER TO postgres;

--
-- Name: estatebase_historymeta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_historymeta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_historymeta_id_seq OWNER TO postgres;

--
-- Name: estatebase_historymeta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_historymeta_id_seq OWNED BY estatebase_historymeta.id;


--
-- Name: estatebase_historymeta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_historymeta_id_seq', 63, true);


--
-- Name: estatebase_interior; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_interior (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_interior OWNER TO postgres;

--
-- Name: estatebase_interior_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_interior_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_interior_id_seq OWNER TO postgres;

--
-- Name: estatebase_interior_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_interior_id_seq OWNED BY estatebase_interior.id;


--
-- Name: estatebase_interior_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_interior_id_seq', 11, true);


--
-- Name: estatebase_internet; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_internet (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_internet OWNER TO postgres;

--
-- Name: estatebase_internet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_internet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_internet_id_seq OWNER TO postgres;

--
-- Name: estatebase_internet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_internet_id_seq OWNED BY estatebase_internet.id;


--
-- Name: estatebase_internet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_internet_id_seq', 3, true);


--
-- Name: estatebase_landtype; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_landtype (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_landtype OWNER TO postgres;

--
-- Name: estatebase_landtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_landtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_landtype_id_seq OWNER TO postgres;

--
-- Name: estatebase_landtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_landtype_id_seq OWNED BY estatebase_landtype.id;


--
-- Name: estatebase_landtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_landtype_id_seq', 4, true);


--
-- Name: estatebase_layout; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_layout (
    id integer NOT NULL,
    level_id integer NOT NULL,
    layout_type_id integer NOT NULL,
    area numeric(7,2),
    furniture_id integer,
    layout_feature_id integer,
    note character varying(255),
    interior_id integer
);


ALTER TABLE public.estatebase_layout OWNER TO postgres;

--
-- Name: estatebase_layout_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_layout_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_layout_id_seq OWNER TO postgres;

--
-- Name: estatebase_layout_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_layout_id_seq OWNED BY estatebase_layout.id;


--
-- Name: estatebase_layout_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_layout_id_seq', 28, true);


--
-- Name: estatebase_layoutfeature; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_layoutfeature (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_layoutfeature OWNER TO postgres;

--
-- Name: estatebase_layoutfeature_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_layoutfeature_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_layoutfeature_id_seq OWNER TO postgres;

--
-- Name: estatebase_layoutfeature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_layoutfeature_id_seq OWNED BY estatebase_layoutfeature.id;


--
-- Name: estatebase_layoutfeature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_layoutfeature_id_seq', 5, true);


--
-- Name: estatebase_layouttype; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_layouttype (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_layouttype OWNER TO postgres;

--
-- Name: estatebase_layouttype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_layouttype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_layouttype_id_seq OWNER TO postgres;

--
-- Name: estatebase_layouttype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_layouttype_id_seq OWNED BY estatebase_layouttype.id;


--
-- Name: estatebase_layouttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_layouttype_id_seq', 27, true);


--
-- Name: estatebase_level; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_level (
    id integer NOT NULL,
    level_name_id integer NOT NULL,
    bidg_id integer NOT NULL
);


ALTER TABLE public.estatebase_level OWNER TO postgres;

--
-- Name: estatebase_level_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_level_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_level_id_seq OWNER TO postgres;

--
-- Name: estatebase_level_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_level_id_seq OWNED BY estatebase_level.id;


--
-- Name: estatebase_level_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_level_id_seq', 16, true);


--
-- Name: estatebase_levelname; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_levelname (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_levelname OWNER TO postgres;

--
-- Name: estatebase_levelname_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_levelname_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_levelname_id_seq OWNER TO postgres;

--
-- Name: estatebase_levelname_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_levelname_id_seq OWNED BY estatebase_levelname.id;


--
-- Name: estatebase_levelname_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_levelname_id_seq', 8, true);


--
-- Name: estatebase_locality; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_locality (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    region_id integer
);


ALTER TABLE public.estatebase_locality OWNER TO postgres;

--
-- Name: estatebase_locality_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_locality_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_locality_id_seq OWNER TO postgres;

--
-- Name: estatebase_locality_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_locality_id_seq OWNED BY estatebase_locality.id;


--
-- Name: estatebase_locality_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_locality_id_seq', 129, true);


--
-- Name: estatebase_microdistrict; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_microdistrict (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    locality_id integer NOT NULL
);


ALTER TABLE public.estatebase_microdistrict OWNER TO postgres;

--
-- Name: estatebase_microdistrict_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_microdistrict_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_microdistrict_id_seq OWNER TO postgres;

--
-- Name: estatebase_microdistrict_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_microdistrict_id_seq OWNED BY estatebase_microdistrict.id;


--
-- Name: estatebase_microdistrict_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_microdistrict_id_seq', 1, false);


--
-- Name: estatebase_office; Type: TABLE; Schema: public; Owner: realty; Tablespace: 
--

CREATE TABLE estatebase_office (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address text NOT NULL
);


ALTER TABLE public.estatebase_office OWNER TO realty;

--
-- Name: estatebase_office_id_seq; Type: SEQUENCE; Schema: public; Owner: realty
--

CREATE SEQUENCE estatebase_office_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_office_id_seq OWNER TO realty;

--
-- Name: estatebase_office_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: realty
--

ALTER SEQUENCE estatebase_office_id_seq OWNED BY estatebase_office.id;


--
-- Name: estatebase_office_id_seq; Type: SEQUENCE SET; Schema: public; Owner: realty
--

SELECT pg_catalog.setval('estatebase_office_id_seq', 1, false);


--
-- Name: estatebase_office_regions; Type: TABLE; Schema: public; Owner: realty; Tablespace: 
--

CREATE TABLE estatebase_office_regions (
    id integer NOT NULL,
    office_id integer NOT NULL,
    region_id integer NOT NULL
);


ALTER TABLE public.estatebase_office_regions OWNER TO realty;

--
-- Name: estatebase_office_regions_id_seq; Type: SEQUENCE; Schema: public; Owner: realty
--

CREATE SEQUENCE estatebase_office_regions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_office_regions_id_seq OWNER TO realty;

--
-- Name: estatebase_office_regions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: realty
--

ALTER SEQUENCE estatebase_office_regions_id_seq OWNED BY estatebase_office_regions.id;


--
-- Name: estatebase_office_regions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: realty
--

SELECT pg_catalog.setval('estatebase_office_regions_id_seq', 1, false);


--
-- Name: estatebase_origin; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_origin (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_origin OWNER TO postgres;

--
-- Name: estatebase_origin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_origin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_origin_id_seq OWNER TO postgres;

--
-- Name: estatebase_origin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_origin_id_seq OWNED BY estatebase_origin.id;


--
-- Name: estatebase_origin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_origin_id_seq', 14, true);


--
-- Name: estatebase_purpose; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_purpose (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_purpose OWNER TO postgres;

--
-- Name: estatebase_purpose_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_purpose_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_purpose_id_seq OWNER TO postgres;

--
-- Name: estatebase_purpose_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_purpose_id_seq OWNED BY estatebase_purpose.id;


--
-- Name: estatebase_purpose_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_purpose_id_seq', 5, true);


--
-- Name: estatebase_region; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_region (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    geo_group_id integer NOT NULL
);


ALTER TABLE public.estatebase_region OWNER TO postgres;

--
-- Name: estatebase_region_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_region_id_seq OWNER TO postgres;

--
-- Name: estatebase_region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_region_id_seq OWNED BY estatebase_region.id;


--
-- Name: estatebase_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_region_id_seq', 4, true);


--
-- Name: estatebase_roof; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_roof (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_roof OWNER TO postgres;

--
-- Name: estatebase_roof_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_roof_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_roof_id_seq OWNER TO postgres;

--
-- Name: estatebase_roof_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_roof_id_seq OWNED BY estatebase_roof.id;


--
-- Name: estatebase_roof_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_roof_id_seq', 7, true);


--
-- Name: estatebase_sewerage; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_sewerage (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_sewerage OWNER TO postgres;

--
-- Name: estatebase_sewerage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_sewerage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_sewerage_id_seq OWNER TO postgres;

--
-- Name: estatebase_sewerage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_sewerage_id_seq OWNED BY estatebase_sewerage.id;


--
-- Name: estatebase_sewerage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_sewerage_id_seq', 6, true);


--
-- Name: estatebase_shape; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_shape (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_shape OWNER TO postgres;

--
-- Name: estatebase_shape_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_shape_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_shape_id_seq OWNER TO postgres;

--
-- Name: estatebase_shape_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_shape_id_seq OWNED BY estatebase_shape.id;


--
-- Name: estatebase_shape_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_shape_id_seq', 6, true);


--
-- Name: estatebase_stead; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_stead (
    id integer NOT NULL,
    estate_id integer NOT NULL,
    total_area numeric(7,2),
    face_area numeric(7,2),
    shape_id integer,
    land_type_id integer,
    purpose_id integer,
    estate_type_id integer NOT NULL
);


ALTER TABLE public.estatebase_stead OWNER TO postgres;

--
-- Name: estatebase_stead_documents; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_stead_documents (
    id integer NOT NULL,
    stead_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.estatebase_stead_documents OWNER TO postgres;

--
-- Name: estatebase_stead_documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_stead_documents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_stead_documents_id_seq OWNER TO postgres;

--
-- Name: estatebase_stead_documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_stead_documents_id_seq OWNED BY estatebase_stead_documents.id;


--
-- Name: estatebase_stead_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_stead_documents_id_seq', 19, true);


--
-- Name: estatebase_stead_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_stead_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_stead_id_seq OWNER TO postgres;

--
-- Name: estatebase_stead_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_stead_id_seq OWNED BY estatebase_stead.id;


--
-- Name: estatebase_stead_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_stead_id_seq', 21, true);


--
-- Name: estatebase_street; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_street (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    locality_id integer NOT NULL
);


ALTER TABLE public.estatebase_street OWNER TO postgres;

--
-- Name: estatebase_street_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_street_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_street_id_seq OWNER TO postgres;

--
-- Name: estatebase_street_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_street_id_seq OWNED BY estatebase_street.id;


--
-- Name: estatebase_street_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_street_id_seq', 1, false);


--
-- Name: estatebase_telephony; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_telephony (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_telephony OWNER TO postgres;

--
-- Name: estatebase_telephony_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_telephony_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_telephony_id_seq OWNER TO postgres;

--
-- Name: estatebase_telephony_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_telephony_id_seq OWNED BY estatebase_telephony.id;


--
-- Name: estatebase_telephony_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_telephony_id_seq', 3, true);


--
-- Name: estatebase_userprofile; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_userprofile (
    id integer NOT NULL,
    user_id integer NOT NULL,
    office_id integer
);


ALTER TABLE public.estatebase_userprofile OWNER TO postgres;

--
-- Name: estatebase_userprofile_geo_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_userprofile_geo_groups (
    id integer NOT NULL,
    userprofile_id integer NOT NULL,
    geogroup_id integer NOT NULL
);


ALTER TABLE public.estatebase_userprofile_geo_groups OWNER TO postgres;

--
-- Name: estatebase_userprofile_geo_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_userprofile_geo_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_userprofile_geo_groups_id_seq OWNER TO postgres;

--
-- Name: estatebase_userprofile_geo_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_userprofile_geo_groups_id_seq OWNED BY estatebase_userprofile_geo_groups.id;


--
-- Name: estatebase_userprofile_geo_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_userprofile_geo_groups_id_seq', 8, true);


--
-- Name: estatebase_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_userprofile_id_seq OWNER TO postgres;

--
-- Name: estatebase_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_userprofile_id_seq OWNED BY estatebase_userprofile.id;


--
-- Name: estatebase_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_userprofile_id_seq', 2, true);


--
-- Name: estatebase_wallconstrucion; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_wallconstrucion (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_wallconstrucion OWNER TO postgres;

--
-- Name: estatebase_wallconstrucion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_wallconstrucion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_wallconstrucion_id_seq OWNER TO postgres;

--
-- Name: estatebase_wallconstrucion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_wallconstrucion_id_seq OWNED BY estatebase_wallconstrucion.id;


--
-- Name: estatebase_wallconstrucion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_wallconstrucion_id_seq', 10, true);


--
-- Name: estatebase_wallfinish; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_wallfinish (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_wallfinish OWNER TO postgres;

--
-- Name: estatebase_wallfinish_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_wallfinish_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_wallfinish_id_seq OWNER TO postgres;

--
-- Name: estatebase_wallfinish_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_wallfinish_id_seq OWNED BY estatebase_wallfinish.id;


--
-- Name: estatebase_wallfinish_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_wallfinish_id_seq', 9, true);


--
-- Name: estatebase_watersupply; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_watersupply (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_watersupply OWNER TO postgres;

--
-- Name: estatebase_watersupply_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_watersupply_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_watersupply_id_seq OWNER TO postgres;

--
-- Name: estatebase_watersupply_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_watersupply_id_seq OWNED BY estatebase_watersupply.id;


--
-- Name: estatebase_watersupply_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_watersupply_id_seq', 9, true);


--
-- Name: estatebase_windowtype; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE estatebase_windowtype (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.estatebase_windowtype OWNER TO postgres;

--
-- Name: estatebase_windowtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE estatebase_windowtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.estatebase_windowtype_id_seq OWNER TO postgres;

--
-- Name: estatebase_windowtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE estatebase_windowtype_id_seq OWNED BY estatebase_windowtype.id;


--
-- Name: estatebase_windowtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('estatebase_windowtype_id_seq', 5, true);


--
-- Name: sitetree_tree; Type: TABLE; Schema: public; Owner: realty; Tablespace: 
--

CREATE TABLE sitetree_tree (
    id integer NOT NULL,
    alias character varying(80) NOT NULL,
    title character varying(100) NOT NULL
);


ALTER TABLE public.sitetree_tree OWNER TO realty;

--
-- Name: sitetree_tree_id_seq; Type: SEQUENCE; Schema: public; Owner: realty
--

CREATE SEQUENCE sitetree_tree_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sitetree_tree_id_seq OWNER TO realty;

--
-- Name: sitetree_tree_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: realty
--

ALTER SEQUENCE sitetree_tree_id_seq OWNED BY sitetree_tree.id;


--
-- Name: sitetree_tree_id_seq; Type: SEQUENCE SET; Schema: public; Owner: realty
--

SELECT pg_catalog.setval('sitetree_tree_id_seq', 1, true);


--
-- Name: sitetree_treeitem; Type: TABLE; Schema: public; Owner: realty; Tablespace: 
--

CREATE TABLE sitetree_treeitem (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    hint character varying(200) NOT NULL,
    url character varying(200) NOT NULL,
    urlaspattern boolean NOT NULL,
    tree_id integer NOT NULL,
    hidden boolean NOT NULL,
    alias character varying(80),
    description text NOT NULL,
    inmenu boolean NOT NULL,
    inbreadcrumbs boolean NOT NULL,
    insitetree boolean NOT NULL,
    parent_id integer,
    sort_order integer NOT NULL,
    access_restricted boolean NOT NULL,
    access_perm_type integer NOT NULL,
    access_loggedin boolean NOT NULL
);


ALTER TABLE public.sitetree_treeitem OWNER TO realty;

--
-- Name: sitetree_treeitem_access_permissions; Type: TABLE; Schema: public; Owner: realty; Tablespace: 
--

CREATE TABLE sitetree_treeitem_access_permissions (
    id integer NOT NULL,
    treeitem_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.sitetree_treeitem_access_permissions OWNER TO realty;

--
-- Name: sitetree_treeitem_access_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: realty
--

CREATE SEQUENCE sitetree_treeitem_access_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sitetree_treeitem_access_permissions_id_seq OWNER TO realty;

--
-- Name: sitetree_treeitem_access_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: realty
--

ALTER SEQUENCE sitetree_treeitem_access_permissions_id_seq OWNED BY sitetree_treeitem_access_permissions.id;


--
-- Name: sitetree_treeitem_access_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: realty
--

SELECT pg_catalog.setval('sitetree_treeitem_access_permissions_id_seq', 1, false);


--
-- Name: sitetree_treeitem_id_seq; Type: SEQUENCE; Schema: public; Owner: realty
--

CREATE SEQUENCE sitetree_treeitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sitetree_treeitem_id_seq OWNER TO realty;

--
-- Name: sitetree_treeitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: realty
--

ALTER SEQUENCE sitetree_treeitem_id_seq OWNED BY sitetree_treeitem.id;


--
-- Name: sitetree_treeitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: realty
--

SELECT pg_catalog.setval('sitetree_treeitem_id_seq', 4, true);


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.south_migrationhistory OWNER TO postgres;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.south_migrationhistory_id_seq OWNER TO postgres;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('south_migrationhistory_id_seq', 132, true);


--
-- Name: thumbnail_kvstore; Type: TABLE; Schema: public; Owner: realty; Tablespace: 
--

CREATE TABLE thumbnail_kvstore (
    key character varying(200) NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.thumbnail_kvstore OWNER TO realty;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_beside ALTER COLUMN id SET DEFAULT nextval('estatebase_beside_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid ALTER COLUMN id SET DEFAULT nextval('estatebase_bid_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_estate_types ALTER COLUMN id SET DEFAULT nextval('estatebase_bid_estate_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_estates ALTER COLUMN id SET DEFAULT nextval('estatebase_bid_estates_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_localities ALTER COLUMN id SET DEFAULT nextval('estatebase_bid_localities_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_regions ALTER COLUMN id SET DEFAULT nextval('estatebase_bid_regions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg ALTER COLUMN id SET DEFAULT nextval('estatebase_bidg_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg_documents ALTER COLUMN id SET DEFAULT nextval('estatebase_bidg_documents_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_ceiling ALTER COLUMN id SET DEFAULT nextval('estatebase_ceiling_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_client ALTER COLUMN id SET DEFAULT nextval('estatebase_client_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_clienttype ALTER COLUMN id SET DEFAULT nextval('estatebase_clienttype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_comstatus ALTER COLUMN id SET DEFAULT nextval('estatebase_comstatus_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contact ALTER COLUMN id SET DEFAULT nextval('estatebase_contact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contacthistory ALTER COLUMN id SET DEFAULT nextval('estatebase_contacthistory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contactstate ALTER COLUMN id SET DEFAULT nextval('estatebase_contactstate_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contacttype ALTER COLUMN id SET DEFAULT nextval('estatebase_contacttype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_document ALTER COLUMN id SET DEFAULT nextval('estatebase_document_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_document_estate_type_category ALTER COLUMN id SET DEFAULT nextval('estatebase_document_estate_type_category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_driveway ALTER COLUMN id SET DEFAULT nextval('estatebase_driveway_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_electricity ALTER COLUMN id SET DEFAULT nextval('estatebase_electricity_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate ALTER COLUMN id SET DEFAULT nextval('estatebase_estate_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate_estate_params ALTER COLUMN id SET DEFAULT nextval('estatebase_estate_estate_params_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateclient ALTER COLUMN id SET DEFAULT nextval('estatebase_estateclient_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateclientstatus ALTER COLUMN id SET DEFAULT nextval('estatebase_estateclientstatus_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateparam ALTER COLUMN id SET DEFAULT nextval('estatebase_estateparam_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estatephoto ALTER COLUMN id SET DEFAULT nextval('estatebase_estatephoto_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister ALTER COLUMN id SET DEFAULT nextval('estatebase_estateregister_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister_bids ALTER COLUMN id SET DEFAULT nextval('estatebase_estateregister_bids_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister_estates ALTER COLUMN id SET DEFAULT nextval('estatebase_estateregister_estates_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estatestatus ALTER COLUMN id SET DEFAULT nextval('estatebase_estatestatus_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estatetype ALTER COLUMN id SET DEFAULT nextval('estatebase_estatetype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estatetypecategory ALTER COLUMN id SET DEFAULT nextval('estatebase_estatetypecategory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_exteriorfinish ALTER COLUMN id SET DEFAULT nextval('estatebase_exteriorfinish_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_flooring ALTER COLUMN id SET DEFAULT nextval('estatebase_flooring_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_furniture ALTER COLUMN id SET DEFAULT nextval('estatebase_furniture_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_gassupply ALTER COLUMN id SET DEFAULT nextval('estatebase_gassupply_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_geogroup ALTER COLUMN id SET DEFAULT nextval('estatebase_geogroup_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_heating ALTER COLUMN id SET DEFAULT nextval('estatebase_heating_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_historymeta ALTER COLUMN id SET DEFAULT nextval('estatebase_historymeta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_interior ALTER COLUMN id SET DEFAULT nextval('estatebase_interior_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_internet ALTER COLUMN id SET DEFAULT nextval('estatebase_internet_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_landtype ALTER COLUMN id SET DEFAULT nextval('estatebase_landtype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_layout ALTER COLUMN id SET DEFAULT nextval('estatebase_layout_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_layoutfeature ALTER COLUMN id SET DEFAULT nextval('estatebase_layoutfeature_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_layouttype ALTER COLUMN id SET DEFAULT nextval('estatebase_layouttype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_level ALTER COLUMN id SET DEFAULT nextval('estatebase_level_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_levelname ALTER COLUMN id SET DEFAULT nextval('estatebase_levelname_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_locality ALTER COLUMN id SET DEFAULT nextval('estatebase_locality_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_microdistrict ALTER COLUMN id SET DEFAULT nextval('estatebase_microdistrict_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: realty
--

ALTER TABLE ONLY estatebase_office ALTER COLUMN id SET DEFAULT nextval('estatebase_office_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: realty
--

ALTER TABLE ONLY estatebase_office_regions ALTER COLUMN id SET DEFAULT nextval('estatebase_office_regions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_origin ALTER COLUMN id SET DEFAULT nextval('estatebase_origin_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_purpose ALTER COLUMN id SET DEFAULT nextval('estatebase_purpose_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_region ALTER COLUMN id SET DEFAULT nextval('estatebase_region_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_roof ALTER COLUMN id SET DEFAULT nextval('estatebase_roof_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_sewerage ALTER COLUMN id SET DEFAULT nextval('estatebase_sewerage_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_shape ALTER COLUMN id SET DEFAULT nextval('estatebase_shape_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead ALTER COLUMN id SET DEFAULT nextval('estatebase_stead_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead_documents ALTER COLUMN id SET DEFAULT nextval('estatebase_stead_documents_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_street ALTER COLUMN id SET DEFAULT nextval('estatebase_street_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_telephony ALTER COLUMN id SET DEFAULT nextval('estatebase_telephony_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_userprofile ALTER COLUMN id SET DEFAULT nextval('estatebase_userprofile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_userprofile_geo_groups ALTER COLUMN id SET DEFAULT nextval('estatebase_userprofile_geo_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_wallconstrucion ALTER COLUMN id SET DEFAULT nextval('estatebase_wallconstrucion_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_wallfinish ALTER COLUMN id SET DEFAULT nextval('estatebase_wallfinish_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_watersupply ALTER COLUMN id SET DEFAULT nextval('estatebase_watersupply_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_windowtype ALTER COLUMN id SET DEFAULT nextval('estatebase_windowtype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: realty
--

ALTER TABLE ONLY sitetree_tree ALTER COLUMN id SET DEFAULT nextval('sitetree_tree_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: realty
--

ALTER TABLE ONLY sitetree_treeitem ALTER COLUMN id SET DEFAULT nextval('sitetree_treeitem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: realty
--

ALTER TABLE ONLY sitetree_treeitem_access_permissions ALTER COLUMN id SET DEFAULT nextval('sitetree_treeitem_access_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add log entry	8	add_logentry
23	Can change log entry	8	change_logentry
24	Can delete log entry	8	delete_logentry
25	Can add migration history	9	add_migrationhistory
26	Can change migration history	9	change_migrationhistory
27	Can delete migration history	9	delete_migrationhistory
28	Can add estate	10	add_estate
29	Can change estate	10	change_estate
30	Can delete estate	10	delete_estate
31	Can add region	11	add_region
32	Can change region	11	change_region
33	Can delete region	11	delete_region
34	Can add locality	12	add_locality
35	Can change locality	12	change_locality
36	Can delete locality	12	delete_locality
37	Can add microdistrict	13	add_microdistrict
38	Can change microdistrict	13	change_microdistrict
39	Can delete microdistrict	13	delete_microdistrict
40	Can add street	14	add_street
41	Can change street	14	change_street
42	Can delete street	14	delete_street
43	Can add estate type category	15	add_estatetypecategory
44	Can change estate type category	15	change_estatetypecategory
45	Can delete estate type category	15	delete_estatetypecategory
46	Can add estate type	16	add_estatetype
47	Can change estate type	16	change_estatetype
48	Can delete estate type	16	delete_estatetype
49	Can add Site Tree	17	add_tree
50	Can change Site Tree	17	change_tree
51	Can delete Site Tree	17	delete_tree
52	Can add Site Tree Item	18	add_treeitem
53	Can change Site Tree Item	18	change_treeitem
54	Can delete Site Tree Item	18	delete_treeitem
55	Can add client type	19	add_clienttype
56	Can change client type	19	change_clienttype
57	Can delete client type	19	delete_clienttype
58	Can add origin	20	add_origin
59	Can change origin	20	change_origin
60	Can delete origin	20	delete_origin
61	Can add client	21	add_client
62	Can change client	21	change_client
63	Can delete client	21	delete_client
64	Can add contact type	22	add_contacttype
65	Can change contact type	22	change_contacttype
66	Can delete contact type	22	delete_contacttype
67	Can add contact	23	add_contact
68	Can change contact	23	change_contact
69	Can delete contact	23	delete_contact
70	Can add contact state	24	add_contactstate
71	Can change contact state	24	change_contactstate
72	Can delete contact state	24	delete_contactstate
73	Can add contact history	25	add_contacthistory
74	Can change contact history	25	change_contacthistory
75	Can delete contact history	25	delete_contacthistory
76	Can add ex user	3	add_exuser
77	Can change ex user	3	change_exuser
78	Can delete ex user	3	delete_exuser
79	Can add bidg	26	add_bidg
80	Can change bidg	26	change_bidg
81	Can delete bidg	26	delete_bidg
82	Can add beside	28	add_beside
83	Can change beside	28	change_beside
84	Can delete beside	28	delete_beside
85	Can add electricity	29	add_electricity
86	Can change electricity	29	change_electricity
87	Can delete electricity	29	delete_electricity
88	Can add watersupply	30	add_watersupply
89	Can change watersupply	30	change_watersupply
90	Can delete watersupply	30	delete_watersupply
91	Can add gassupply	31	add_gassupply
92	Can change gassupply	31	change_gassupply
93	Can delete gassupply	31	delete_gassupply
94	Can add sewerage	32	add_sewerage
95	Can change sewerage	32	change_sewerage
96	Can delete sewerage	32	delete_sewerage
97	Can add telephony	33	add_telephony
98	Can change telephony	33	change_telephony
99	Can delete telephony	33	delete_telephony
100	Can add internet	34	add_internet
101	Can change internet	34	change_internet
102	Can delete internet	34	delete_internet
103	Can add driveway	35	add_driveway
104	Can change driveway	35	change_driveway
105	Can delete driveway	35	delete_driveway
106	Can add estate status	36	add_estatestatus
107	Can change estate status	36	change_estatestatus
108	Can delete estate status	36	delete_estatestatus
109	Can add document	37	add_document
110	Can change document	37	change_document
111	Can delete document	37	delete_document
112	Can add estate param	38	add_estateparam
113	Can change estate param	38	change_estateparam
114	Can delete estate param	38	delete_estateparam
118	Can add history meta	40	add_historymeta
119	Can change history meta	40	change_historymeta
120	Can delete history meta	40	delete_historymeta
124	Can add wall construcion	42	add_wallconstrucion
125	Can change wall construcion	42	change_wallconstrucion
126	Can delete wall construcion	42	delete_wallconstrucion
127	Can add exterior finish	43	add_exteriorfinish
128	Can change exterior finish	43	change_exteriorfinish
129	Can delete exterior finish	43	delete_exteriorfinish
130	Can add window type	44	add_windowtype
131	Can change window type	44	change_windowtype
132	Can delete window type	44	delete_windowtype
133	Can add heating	45	add_heating
134	Can change heating	45	change_heating
135	Can delete heating	45	delete_heating
139	Can add Wall finish	47	add_wallfinish
140	Can change Wall finish	47	change_wallfinish
141	Can delete Wall finish	47	delete_wallfinish
142	Can add Flooring	48	add_flooring
143	Can change Flooring	48	change_flooring
144	Can delete Flooring	48	delete_flooring
145	Can add Ceiling	49	add_ceiling
146	Can change Ceiling	49	change_ceiling
147	Can delete Ceiling	49	delete_ceiling
148	Can add Interior	50	add_interior
149	Can change Interior	50	change_interior
150	Can delete Interior	50	delete_interior
151	Can add Roof	51	add_roof
152	Can change Roof	51	change_roof
153	Can delete Roof	51	delete_roof
154	Can add Level	52	add_level
155	Can change Level	52	change_level
156	Can delete Level	52	delete_level
157	Can add Layout type	53	add_layouttype
158	Can change Layout type	53	change_layouttype
159	Can delete Layout type	53	delete_layouttype
160	Can add Furniture	54	add_furniture
161	Can change Furniture	54	change_furniture
162	Can delete Furniture	54	delete_furniture
163	Can add Layout feature	55	add_layoutfeature
164	Can change Layout feature	55	change_layoutfeature
165	Can delete Layout feature	55	delete_layoutfeature
166	Can add layout	56	add_layout
167	Can change layout	56	change_layout
168	Can delete layout	56	delete_layout
169	Can add Level name	57	add_levelname
170	Can change Level name	57	change_levelname
171	Can delete Level name	57	delete_levelname
172	Can add EstatePhoto	58	add_estatephoto
173	Can change EstatePhoto	58	change_estatephoto
174	Can delete EstatePhoto	58	delete_estatephoto
175	Can add kv store	59	add_kvstore
176	Can change kv store	59	change_kvstore
177	Can delete kv store	59	delete_kvstore
178	Can add stead	60	add_stead
179	Can change stead	60	change_stead
180	Can delete stead	60	delete_stead
181	Can add Shape	61	add_shape
182	Can change Shape	61	change_shape
183	Can delete Shape	61	delete_shape
184	Can add Land type	62	add_landtype
185	Can change Land type	62	change_landtype
186	Can delete Land type	62	delete_landtype
187	Can add Purpose	63	add_purpose
188	Can change Purpose	63	change_purpose
189	Can delete Purpose	63	delete_purpose
190	Can add user profile	64	add_userprofile
191	Can change user profile	64	change_userprofile
192	Can delete user profile	64	delete_userprofile
193	Can add Geo group	65	add_geogroup
194	Can change Geo group	65	change_geogroup
195	Can delete Geo group	65	delete_geogroup
196	Can add bid	66	add_bid
197	Can change bid	66	change_bid
198	Can delete bid	66	delete_bid
199	Can add estate register	67	add_estateregister
200	Can change estate register	67	change_estateregister
201	Can delete estate register	67	delete_estateregister
202	Can add estate client	68	add_estateclient
203	Can change estate client	68	change_estateclient
204	Can delete estate client	68	delete_estateclient
205	Can add Estate client status	69	add_estateclientstatus
206	Can change Estate client status	69	change_estateclientstatus
207	Can delete Estate client status	69	delete_estateclientstatus
208	Can add Com status	70	add_comstatus
209	Can change Com status	70	change_comstatus
210	Can delete Com status	70	delete_comstatus
211	Can add Office	71	add_office
212	Can change Office	71	change_office
213	Can delete Office	71	delete_office
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
2	guest	Гость			pbkdf2_sha256$10000$dIZSiYcRrKdH$K3YsOa3Csop97WIT37nIWRQani42HKRspNSZIirwYsM=	f	t	f	2012-09-11 15:15:37+04	2012-09-11 15:15:37+04
1	picasso	Павел	Саввин	picasso75@yandex.ru	pbkdf2_sha256$10000$JrpVfcKQPkuA$b9WPRNoP2NYDVDXIRy9db8uTGdAqepuAtTyJyVSOISg=	t	t	t	2012-10-17 00:17:20.092749+04	2012-04-22 12:11:49+04
3	realty	Риэлтор	Главный		pbkdf2_sha256$10000$3Z3AtI6aFuPI$iQEnNTQGjlX0aSXJr2jvhumG2qrKyMk8IA7/kJ11Oz8=	t	t	t	2012-10-20 13:18:24.34377+04	2012-10-17 23:13:28+04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
1	2012-04-23 22:34:01.550634+04	1	12	1	Новороссийск	1	
2	2012-04-23 22:34:38.579618+04	1	14	1	Южная, ул.	1	
3	2012-04-23 22:41:20.650997+04	1	12	2	Геленджик	1	
4	2012-04-23 22:41:46.624218+04	1	14	2	Зеленая, ул.	1	
5	2012-04-23 22:42:15.236111+04	1	14	3	Красная, ул.	1	
6	2012-04-23 23:03:21.900697+04	1	14	4	Новая	1	
7	2012-04-23 23:03:37.074439+04	1	14	4	Новая, ул.	2	Изменен name.
8	2012-04-23 23:05:48.65226+04	1	14	5	123	1	
9	2012-04-24 00:03:05.807595+04	1	14	6	333	1	
10	2012-04-24 00:03:21.639871+04	1	14	7	tutyut	1	
11	2012-04-24 00:03:51.401647+04	1	14	7	tutyut	3	
12	2012-04-24 00:03:51.420669+04	1	14	5	123	3	
13	2012-04-24 00:09:45.091647+04	1	14	8	57856756	1	
14	2012-04-24 00:10:07.633227+04	1	14	8	57856756	3	
15	2012-04-24 00:10:07.649436+04	1	14	6	333	3	
16	2012-04-26 00:38:29.474283+04	1	15	1	123	1	
17	2012-04-26 22:39:18.269709+04	1	16	1	1.123	1	
18	2012-04-26 22:57:47.846202+04	1	15	2	22222	1	
19	2012-04-26 22:57:54.726525+04	1	15	3	33333	1	
20	2012-04-26 23:13:49.704658+04	1	16	2	2222	1	
21	2012-04-26 23:14:10.581405+04	1	16	3	44444	1	
22	2012-04-30 16:27:56.077106+04	1	10	3	Estate object	3	
23	2012-04-30 16:27:56.178743+04	1	10	2	Estate object	3	
24	2012-04-30 16:27:56.187903+04	1	10	1	Estate object	3	
25	2012-04-30 16:37:58.135207+04	1	10	4	Estate object	3	
26	2012-05-01 11:19:04.452843+04	1	14	9	Ленина, пр.	1	
27	2012-05-01 11:21:04.034658+04	1	14	10	Ленина, пр.	1	
28	2012-05-01 11:23:14.438647+04	1	14	10	Ленина, пр.	3	
29	2012-05-01 12:54:01.548572+04	1	10	9	Estate object	3	
30	2012-05-01 12:54:01.572157+04	1	10	8	Estate object	3	
31	2012-05-01 12:54:01.58041+04	1	10	7	Estate object	3	
32	2012-05-01 12:54:01.588951+04	1	10	6	Estate object	3	
33	2012-05-01 12:54:01.597093+04	1	10	5	Estate object	3	
34	2012-05-01 13:15:40.340342+04	1	10	11	Estate object	3	
35	2012-05-01 13:15:40.357154+04	1	10	10	Estate object	3	
36	2012-05-27 20:03:31.362479+04	1	3	1	picasso	2	Изменен password,first_name и last_name.
37	2012-06-02 18:48:03.996356+04	1	12	1	Анапа	1	
38	2012-06-02 18:48:17.334648+04	1	14	1	Ленина	1	
39	2012-06-02 18:48:33.863865+04	1	12	2	Новороссийск	1	
40	2012-06-02 18:48:35.731266+04	1	14	2	Мира, ул.	1	
41	2012-06-02 18:48:42.387016+04	1	14	1	Ленина, пр.	2	Изменен name.
42	2012-06-02 18:59:20.468645+04	1	10	1	Estate object	3	
43	2012-06-11 01:09:20.855169+04	1	11	1	Анапский	1	
44	2012-06-11 01:09:31.514151+04	1	12	1	Анапа	2	Изменен region.
45	2012-06-11 11:33:26.247073+04	1	13	1	Южный	1	
46	2012-06-11 11:33:41.729773+04	1	13	2	Анапский	1	
47	2012-06-16 12:51:44.588119+04	1	10	14	Estate object	3	
48	2012-06-16 12:51:44.645998+04	1	10	15	Estate object	3	
49	2012-06-16 12:51:44.666963+04	1	10	16	Estate object	3	
50	2012-06-16 12:51:44.679258+04	1	10	17	Estate object	3	
51	2012-06-16 12:54:00.663263+04	1	10	18	Estate object	3	
52	2012-06-16 19:02:07.676341+04	1	26	19	Bidg object	2	Изменен bidg_number.
53	2012-06-17 12:01:10.276382+04	1	10	19	Estate object	3	
54	2012-06-17 12:01:10.343544+04	1	10	20	Estate object	3	
55	2012-06-17 12:56:26.349032+04	1	26	1	Bidg object	1	
56	2012-06-21 21:26:59.826734+04	1	38	1	EstateParam object	1	
57	2012-06-21 21:27:09.680235+04	1	38	2	EstateParam object	1	
58	2012-06-21 21:27:17.57339+04	1	38	3	EstateParam object	1	
59	2012-06-21 21:27:24.854853+04	1	38	4	EstateParam object	1	
60	2012-06-21 21:27:31.765316+04	1	38	5	EstateParam object	1	
61	2012-06-21 21:27:39.071565+04	1	38	6	EstateParam object	1	
62	2012-06-21 21:49:21.617886+04	1	37	1	Cвидетельство	1	
63	2012-06-21 21:49:46.718263+04	1	37	2	Технический паспорт	1	
64	2012-06-21 21:50:06.692668+04	1	37	3	Кадастровый номер	1	
65	2012-06-24 15:46:37.449671+04	1	28	1	Азовское море	1	
66	2012-06-24 15:46:51.302167+04	1	28	2	Ахтанизовский лиман	1	
67	2012-06-24 15:47:01.859619+04	1	28	3	Витязевский лиман	1	
68	2012-06-24 15:47:10.504175+04	1	28	4	Динской  залив	1	
69	2012-06-24 15:47:23.520868+04	1	28	5	Кизилташский лиман	1	
70	2012-06-24 15:47:32.01549+04	1	28	6	Курчанский лиман	1	
71	2012-06-24 15:47:39.757997+04	1	28	7	Старотитаровский лиман	1	
72	2012-06-24 15:47:50.139097+04	1	28	8	Таманский залив	1	
73	2012-06-24 15:48:07.839604+04	1	28	9	Черное море	1	
74	2012-06-24 15:48:17.264953+04	1	28	10	Цокур лиман	1	
75	2012-06-24 15:48:33.797725+04	1	28	11	Абрау озеро	1	
76	2012-06-24 15:48:42.722624+04	1	28	12	Кубань река	1	
77	2012-06-30 19:47:27.825744+04	1	37	2	Технический паспорт	2	Изменен estate_type.
78	2012-07-02 23:13:02.468725+04	1	57	1	1	1	
79	2012-07-03 22:28:03.096258+04	1	57	1	1-й	2	Изменен name.
80	2012-07-03 22:28:09.447826+04	1	57	2	2-й	1	
81	2012-07-05 23:24:09.060116+04	1	58	1	None	3	
82	2012-07-05 23:24:09.115295+04	1	58	2	None	3	
83	2012-07-05 23:24:09.123484+04	1	58	3	None	3	
84	2012-07-06 23:57:03.895817+04	1	58	4	None	3	
85	2012-07-06 23:57:03.948199+04	1	58	5	None	3	
86	2012-07-06 23:57:03.956432+04	1	58	6	None	3	
87	2012-07-06 23:57:03.964816+04	1	58	7	None	3	
88	2012-07-06 23:57:03.973026+04	1	58	8	None	3	
89	2012-07-08 18:45:28.759005+04	1	16	13	Новостройка	2	Изменен view_prefix.
90	2012-07-08 18:51:21.392225+04	1	16	13	Новостройка	2	Изменен view_prefix.
91	2012-07-08 18:55:15.122537+04	1	16	13	Новостройка	2	Изменен view_prefix.
92	2012-07-08 19:07:06.939513+04	1	16	13	Новостройка	2	Изменен view_prefix.
93	2012-07-13 00:01:51.657829+04	1	10	33	33	3	
94	2012-07-13 00:01:51.729664+04	1	10	34	34	3	
95	2012-07-13 00:01:51.73799+04	1	10	35	35	3	
96	2012-07-13 00:01:51.746352+04	1	10	36	36	3	
97	2012-07-13 00:01:51.754639+04	1	10	37	37	3	
98	2012-07-13 00:01:51.762967+04	1	10	38	38	3	
99	2012-07-14 13:54:31.093861+04	1	26	2	Bidg object	2	Изменен estate_type.
100	2012-07-14 13:55:32.830962+04	1	26	2	Bidg object	2	Изменен basic.
101	2012-07-14 13:56:08.985799+04	1	16	13	Новостройка	2	Изменен template.
102	2012-07-14 14:00:10.780631+04	1	16	14	Малосемейка	2	Изменен template.
103	2012-07-16 23:18:42.732255+04	1	16	9	Участок с фундаментом	2	Изменен object_type и template.
104	2012-07-16 23:35:04.950394+04	1	16	16	Новостройка	1	
105	2012-07-16 23:35:53.179814+04	1	16	13	Новостройка	2	Изменен template.
106	2012-07-16 23:35:59.933584+04	1	16	16	Новостройка	3	
107	2012-07-16 23:52:50.960022+04	1	60	1	Stead object	2	Изменен total_area.
108	2012-07-17 00:26:16.889607+04	1	16	17	Дом	1	
109	2012-07-17 00:45:32.747654+04	1	37	1	Cвидетельство	2	Изменен estate_type.
110	2012-07-22 00:22:37.979626+04	1	16	4	Дачный участок	2	Изменен object_type и template.
111	2012-07-22 00:36:07.092871+04	1	15	1	Земельный участок	2	Изменены template для вид недвижимости "Сельскохозяйственный участок". Изменены object_type и template для вид недвижимости "Коммерческий участок". Изменены object_type и template для вид недвижимости "Участок с квартирой". Изменены object_type и template для вид недвижимости "Дача". Изменены object_type и template для вид недвижимости "Участок с недостроем". Изменены object_type и template для вид недвижимости "Участок с ветхим домом".
112	2012-07-22 12:15:56.683293+04	1	16	17	Дом	2	Изменен template.
113	2012-07-22 18:33:31.55122+04	1	15	3	Квартира	2	Изменены template для вид недвижимости "Малосемейка". Изменены template для вид недвижимости "Вторичка".
114	2012-07-22 18:33:37.270102+04	1	15	1	Земельный участок	2	Ни одно поле не изменено.
115	2012-07-22 18:33:47.653452+04	1	15	2	Гараж	2	Изменены template для вид недвижимости "Гараж".
116	2012-07-22 18:52:37.290646+04	1	26	18	Bidg object	2	Ни одно поле не изменено.
117	2012-07-22 18:52:51.150451+04	1	26	16	Bidg object	2	Изменен estate_type.
118	2012-07-22 18:53:04.03498+04	1	26	1	Bidg object	2	Изменен estate_type.
119	2012-07-22 18:53:14.449434+04	1	26	3	Bidg object	2	Изменен estate_type.
120	2012-07-22 18:53:28.148056+04	1	26	6	Bidg object	2	Изменен estate_type.
121	2012-08-01 00:11:51.354845+04	1	16	12	Гараж	2	Изменен placeable.
122	2012-08-10 23:21:52.911379+04	1	65	1	Тамань	1	
123	2012-08-10 23:22:03.723809+04	1	65	2	Новороссийск	1	
124	2012-08-10 23:22:36.955308+04	1	64	1	UserProfile object	1	
125	2012-08-10 23:25:18.085115+04	1	64	1	UserProfile object	2	Изменен geo_groups.
126	2012-08-10 23:25:40.317485+04	1	12	2	Новороссийск	2	Изменен geo_group.
127	2012-08-10 23:34:29.139154+04	1	64	1	UserProfile object	2	Изменен geo_groups.
128	2012-08-10 23:35:54.193139+04	1	64	1	UserProfile object	2	Изменен geo_groups.
129	2012-08-11 11:27:45.953387+04	1	64	1	UserProfile object	2	Изменен geo_groups.
130	2012-08-12 13:42:55.882736+04	1	64	1	UserProfile object	2	Изменен geo_groups.
131	2012-08-12 13:47:51.08924+04	1	3	1	picasso	2	Изменен password. Изменены geo_groups для user profile "UserProfile object".
132	2012-08-13 23:04:46.450955+04	1	3	1	picasso	2	Изменен password. Изменены geo_groups для user profile "UserProfile object".
133	2012-09-05 23:42:04.729909+04	1	66	6	Bid object	2	Изменен deleted.
134	2012-09-11 15:15:37.883507+04	1	3	2	guest	1	
135	2012-09-11 15:15:48.369472+04	1	3	2	guest	2	Изменен password и first_name.
136	2012-09-11 15:35:26.233196+04	1	21	44	Новый мир 	2	Изменен deleted.
137	2012-09-11 15:35:30.807702+04	1	21	43	Глюк 	2	Изменен deleted.
138	2012-10-01 21:56:10.052685+04	1	3	1	picasso	2	Изменен password. Изменены geo_groups для user profile "UserProfile object".
139	2012-10-01 22:12:36.736119+04	1	3	1	picasso	2	Изменен password. Добавлен user profile "UserProfile object".
140	2012-10-01 22:31:23.275429+04	1	16	12	Гараж	2	Изменен template.
141	2012-10-01 22:31:53.622383+04	1	16	15	Вторичка	2	Изменен template.
142	2012-10-02 23:17:37.963123+04	1	16	13	Новостройка	2	Изменен template.
143	2012-10-02 23:18:56.069634+04	1	16	14	Малосемейка	2	Изменен template.
144	2012-10-05 21:14:53.922894+04	1	16	15	Вторичка	2	Изменен template.
145	2012-10-07 19:36:19.996992+04	1	3	1	picasso	2	Изменен password. Добавлен user profile "UserProfile object".
146	2012-10-07 21:05:13.047087+04	1	15	4	Квартира	2	Изменены has_bidg для вид недвижимости "Вторичка". Изменены has_bidg для вид недвижимости "Комната". Изменены has_bidg для вид недвижимости "Малосемейка". Изменены has_bidg для вид недвижимости "Новостройка".
147	2012-10-11 22:03:21.705098+04	1	37	1	Cвидетельство	1	
148	2012-10-11 22:03:47.726616+04	1	37	2	Технический паспорт	1	
149	2012-10-11 22:04:06.601946+04	1	37	3	Кадастровый номер	1	
150	2012-10-11 22:31:16.366418+04	1	37	4	Свидетельство	1	
151	2012-10-11 22:32:16.173177+04	1	37	5	Технический паспорт	1	
152	2012-10-11 22:32:51.10945+04	1	37	6	Кадастровый номер	1	
153	2012-10-11 22:46:38.339182+04	1	37	6	Кадастровый номер	2	Изменен estate_type_category.
154	2012-10-11 22:46:58.897549+04	1	37	7	Свидетельство на участок	1	
155	2012-10-11 22:47:17.591525+04	1	37	8	Межевой план	1	
156	2012-10-13 15:09:14.212784+04	1	70	1	Используется	1	
157	2012-10-13 15:09:27.799304+04	1	70	2	Возможно	1	
158	2012-10-13 15:09:40.200314+04	1	70	2	Возможно ком. исп.	2	Изменен name.
159	2012-10-13 15:09:48.564591+04	1	70	2	Возможно	2	Изменен name.
160	2012-10-13 15:10:11.901108+04	1	70	3	Нельзя	1	
161	2012-10-13 15:10:27.94186+04	1	70	3	Нет возможности	2	Изменен name.
162	2012-10-17 23:13:28.874523+04	1	3	3	realty	1	
163	2012-10-17 23:13:41.136802+04	1	3	3	realty	2	Изменен password,is_staff и is_superuser.
164	2012-10-17 23:14:20.322969+04	1	3	3	realty	2	Изменен password,first_name и last_name.
165	2012-10-19 09:34:54.199133+04	3	16	14	Дачный участок	2	Изменен name.
166	2012-10-19 09:35:05.739931+04	3	16	15	Участок для строительства жилого дома	2	Изменен name.
167	2012-10-19 09:35:30.518636+04	3	16	42	Участок сельскохозяйственного назначения	2	Изменен name.
168	2012-10-19 09:35:52.180382+04	3	16	20	Участок коммерческого назначения	2	Изменен name.
169	2012-10-19 13:52:18.451944+04	3	16	15	Участок для строительства дома	2	Изменен name.
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	log entry	admin	logentry
9	migration history	south	migrationhistory
10	estate	estatebase	estate
11	region	estatebase	region
12	locality	estatebase	locality
13	microdistrict	estatebase	microdistrict
14	street	estatebase	street
15	estate type category	estatebase	estatetypecategory
16	estate type	estatebase	estatetype
17	Site Tree	sitetree	tree
18	Site Tree Item	sitetree	treeitem
19	client type	estatebase	clienttype
20	origin	estatebase	origin
21	client	estatebase	client
22	contact type	estatebase	contacttype
23	contact	estatebase	contact
24	contact state	estatebase	contactstate
25	contact history	estatebase	contacthistory
26	bidg	estatebase	bidg
27	ex user	estatebase	exuser
28	beside	estatebase	beside
29	electricity	estatebase	electricity
30	watersupply	estatebase	watersupply
31	gassupply	estatebase	gassupply
32	sewerage	estatebase	sewerage
33	telephony	estatebase	telephony
34	internet	estatebase	internet
35	driveway	estatebase	driveway
36	estate status	estatebase	estatestatus
37	document	estatebase	document
38	estate param	estatebase	estateparam
40	history meta	estatebase	historymeta
42	wall construcion	estatebase	wallconstrucion
43	exterior finish	estatebase	exteriorfinish
44	window type	estatebase	windowtype
45	heating	estatebase	heating
47	Wall finish	estatebase	wallfinish
48	Flooring	estatebase	flooring
49	Ceiling	estatebase	ceiling
50	Interior	estatebase	interior
51	Roof	estatebase	roof
52	Level	estatebase	level
53	Layout type	estatebase	layouttype
54	Furniture	estatebase	furniture
55	Layout feature	estatebase	layoutfeature
56	layout	estatebase	layout
57	Level name	estatebase	levelname
58	EstatePhoto	estatebase	estatephoto
59	kv store	thumbnail	kvstore
60	stead	estatebase	stead
61	Shape	estatebase	shape
62	Land type	estatebase	landtype
63	Purpose	estatebase	purpose
64	user profile	estatebase	userprofile
65	Geo group	estatebase	geogroup
66	bid	estatebase	bid
67	estate register	estatebase	estateregister
68	estate client	estatebase	estateclient
69	Estate client status	estatebase	estateclientstatus
70	Com status	estatebase	comstatus
71	Office	estatebase	office
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
d8a502c071e9b11e9c9db2f40a4dad19	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-08-13 00:29:41.532663+04
9e4835b8e00d9a4c434f782a303dd882	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-08-13 02:02:12.414019+04
b7400675b058296e772be079f0880196	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-09-04 21:09:31.541562+04
b21687332a68c0011009d50cc48e1830	Mzc4YTRhM2FlNmY1NWUxODM3YjgyY2YwZDhjMDUyZjBlM2FkZGZmYjqAAn1xAShVCGZpbHRlcmVk\nTlgcAAAAa2V5X2FkbWluX2VzdGF0ZWJhc2Vfc3RyZWV0X1UVbG9jYWxpdHlfX2lkX19leGFjdD0x\nVRJfYXV0aF91c2VyX2JhY2tlbmRVKWRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxC\nYWNrZW5kVQ1fYXV0aF91c2VyX2lkSwF1Lg==\n	2012-05-25 22:37:38.204471+04
cb3ea2b47dd89f2c2e0710a55380195e	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-09-09 23:36:24.316918+04
e844e081500ca0dac060dad3f129a2c1	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-06-08 23:08:15.940597+04
888673bf1c1f8462631b480399da84d4	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-06-10 20:32:50.220095+04
d934c2b88734af56f444d5ee3506bad0	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-07-29 00:36:09.168505+04
a98d713bd65e44b6d6aa6a0414696f12	OWQ3MWFiMTEwYTkzZjZhYzdiNmVlMGE3OGJhMDkxZDEyMmI4MzkyMjqAAn1xAShYIgAAAGtleV9h\nZG1pbl9lc3RhdGViYXNlX2xvY2FsaXR5X2FkZF9VCF9wb3B1cD0xcQJVEl9hdXRoX3VzZXJfYmFj\na2VuZFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRVDV9hdXRoX3Vz\nZXJfaWRLAXUu\n	2012-06-16 18:48:33.878638+04
de0c1e864882c0e93c6efa3f0e6d5a7c	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-06-25 01:09:04.098697+04
cc817a47b7970b251a3a4e6922b4c583	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-07-10 00:23:28.610857+04
492d1a16a3dd9e4ced70daa42404e8f0	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-08-03 23:07:42.547803+04
80dcab1776ddc94bf5e5128289b764a6	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-07-14 14:03:55.385084+04
7db5f19e5dd92ec28142ce3c11b61d12	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-09-26 17:26:34.02957+04
6372f53f750045a2ffbcb0e66398bea8	ODM5MTA3NmRhMjg1YmNhOTE5OGRmZGZmNjIxZTNmNWQzOTI2YTVkMzqAAn1xAShVCnRlc3Rjb29r\naWVVBndvcmtlZHECVRJfYXV0aF91c2VyX2JhY2tlbmRVKWRqYW5nby5jb250cmliLmF1dGguYmFj\na2VuZHMuTW9kZWxCYWNrZW5kVQ1fYXV0aF91c2VyX2lkSwF1Lg==\n	2012-09-30 00:11:02.377485+04
1e35479ac98997b60b46eb0f312d2a98	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-14 00:19:47.129374+04
cffe33bd80f7ea539404419312fe6ee6	YzAwNDgxYjExZDdmMTE2M2U5OGU1MDdiMDIyODc2YjQ4MjVhZjFmMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLA3Uu\n	2012-11-02 09:48:03.971863+04
853b9b59db74a2d9a3b912de933204d2	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-30 20:45:14.41849+04
9942508dc70a5950cdecacb5f698d4c4	YTJkMWE5M2IxMTk1NzhkYmZhNDI4NmIzNGYzNWUxZjVlOWZiM2QwZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-10-31 00:17:20.107063+04
997b90383c6f502a07f8154965005cdd	YzAwNDgxYjExZDdmMTE2M2U5OGU1MDdiMDIyODc2YjQ4MjVhZjFmMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLA3Uu\n	2012-11-02 21:16:40.181921+04
d9aa607e08b8afb62f72a80a6d31f06f	YzAwNDgxYjExZDdmMTE2M2U5OGU1MDdiMDIyODc2YjQ4MjVhZjFmMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLA3Uu\n	2012-11-03 13:18:24.355425+04
3affd4076260a8e80a1f7542e6d7d278	YzAwNDgxYjExZDdmMTE2M2U5OGU1MDdiMDIyODc2YjQ4MjVhZjFmMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLA3Uu\n	2012-10-31 23:28:15.400405+04
47f79571db2188feef495d943f1622f9	YzAwNDgxYjExZDdmMTE2M2U5OGU1MDdiMDIyODc2YjQ4MjVhZjFmMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLA3Uu\n	2012-11-01 07:14:33.491108+04
034e76e141d74913a3e5cce27300ba60	Zjc0ZjI0YTg5M2QxMWIzZDkwYjZhZjFiMzcxMmEwNWIyZDU3MmIxMjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n	2012-11-01 10:13:13.952593+04
9b65ca002471f282c3582c0dc1e3db55	YzAwNDgxYjExZDdmMTE2M2U5OGU1MDdiMDIyODc2YjQ4MjVhZjFmMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLA3Uu\n	2012-11-01 11:10:48.24167+04
ab04a444c8236dd7e2afccdc8f77b4da	YzAwNDgxYjExZDdmMTE2M2U5OGU1MDdiMDIyODc2YjQ4MjVhZjFmMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLA3Uu\n	2012-11-01 12:11:49.118192+04
bae82b3e8a99fdfbec25be0ab4e99a97	YzAwNDgxYjExZDdmMTE2M2U5OGU1MDdiMDIyODc2YjQ4MjVhZjFmMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLA3Uu\n	2012-11-01 18:44:56.473159+04
82a1b8545dbbdf9da9002d4752340822	M2ZkOGFmNzI1N2U1Mjg1ZmRlNGIwY2M3MWI2YTEzYjQ1MDYyMjBhYTqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRLA1USX2F1dGhfdXNlcl9iYWNrZW5kVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRz\nLk1vZGVsQmFja2VuZHECdS4=\n	2012-11-02 09:24:45.868019+04
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: estatebase_beside; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_beside (id, name) FROM stdin;
1	Абрау озеро
2	Азовское море
3	Ахтанизовский лиман
4	Витязевский лиман
5	Динской залив
6	Кизилташский лиман
7	Кубань река
8	Курчанский лиман
9	Старотитаровский лиман
10	Таманский залив
11	Цокур лиман
12	Черное море
\.


--
-- Data for Name: estatebase_bid; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_bid (id, deleted, client_id, estate_filter, history_id, broker_id, agency_price_min, agency_price_max) FROM stdin;
1	f	1	gAJjZGphbmdvLmh0dHAKUXVlcnlEaWN0CnEBKYFxAihYCwAAAGdhc3N1cHBseV8xcQNYAAAAAFgJAAAAY3JlYXRlZF8wcQRYAAAAAFgJAAAAY3JlYXRlZF8xcQVYAAAAAFgNAAAAZ2Fzc3VwcGx5XzBfMXEGWAAAAABYDQAAAGdhc3N1cHBseV8wXzBxB1gAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzFxCFgAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzBxCVgAAAAAWAoAAAB0b3RhbF9hcmVhcQpYAAAAAFgIAAAAYmVzaWRlXzFxC1gAAAAAWAoAAAByb29tX2NvdW50cQxYAAAAAFgKAAAAaW50ZXJpb3JfMHENWAAAAABYDwAAAGVsZWN0cmljaXR5XzBfMHEOWAAAAABYCAAAAG9yaWdpbl8wcQ9YAAAAAFgKAAAAYmVzaWRlXzBfMHEQWAAAAABYCwAAAGZsb29yX2NvdW50cRFYAAAAAFgFAAAAZmxvb3JxElgAAAAAWAgAAAByZWdpb25fMHETWAAAAABYDAAAAGFnZW5jeV9wcmljZXEUWAAAAABYCQAAAGZhY2VfYXJlYXEVWAAAAABYEgAAAHdhbGxfY29uc3RydWNpb25fMHEWWAAAAABYDAAAAGRyaXZld2F5XzBfMXEXWAAAAABYCQAAAHVwZGF0ZWRfMHEYWAAAAABYEwAAAGNzcmZtaWRkbGV3YXJldG9rZW5xGVggAAAAZlZWSUVtUXFhVFhDVjFpMFlSWlNSZnBjWWpOeFVWR29xGlgKAAAAbG9jYWxpdHlfMHEbWAAAAABYCAAAAGJyb2tlcl8wcRxYIQAAANCf0LDQstC10Lsg0KHQsNCy0LLQuNC9IChwaWNhc3NvKXEdWAgAAABicm9rZXJfMXEeWAEAAAAxWAUAAABfc2F2ZXEfWBIAAADQodC+0YXRgNCw0L3QuNGC0YxxIFgPAAAAZXN0YXRlX3N0YXR1c18wcSFYAAAAAFgJAAAAdXBkYXRlZF8xcSJYAAAAAFgMAAAAZHJpdmV3YXlfMF8wcSNYAAAAAFgKAAAAc2V3ZXJhZ2VfMXEkWAAAAABYDwAAAG1pY3JvZGlzdHJpY3RfMHElWAAAAABYCgAAAGRyaXZld2F5XzFxJlgAAAAAWAwAAABzZXdlcmFnZV8wXzFxJ1gAAAAAWAwAAABzZXdlcmFnZV8wXzBxKFgAAAAAWAoAAABzdGVhZF9hcmVhcSlYAAAAAFgNAAAAZWxlY3RyaWNpdHlfMXEqWAAAAABYCgAAAGJlc2lkZV8wXzFxK1gAAAAAWA0AAABlc3RhdGVfdHlwZV8xcSxYAgAAADE2cS1YDQAAAGVzdGF0ZV90eXBlXzBxLlgAAAAAWAoAAAB5ZWFyX2J1aWx0cS9YAAAAAFgJAAAAZXN0YXRlc18wcTBYAAAAAFgNAAAAd2F0ZXJzdXBwbHlfMXExWAAAAABYCQAAAHVzZWRfYXJlYXEyWAAAAABYDwAAAGVsZWN0cmljaXR5XzBfMXEzWAAAAABYCAAAAGNsaWVudF8wcTRYGQAAANCU0L7QvCDQvdCwINCi0LDQvNCw0L3QuCBxNVgIAAAAY2xpZW50XzFxNlgBAAAAMXV9cTcoVQlfZW5jb2RpbmdxOFUFdXRmLThxOVUFX2RhdGFxOn1xOyhoA11xPFgAAAAAYWgEXXE9WAAAAABhaAVdcT5YAAAAAGFoBl1xP1gAAAAAYWgHXXFAWAAAAABhaAhdcUFYAAAAAGFoCV1xQlgAAAAAYWgKXXFDWAAAAABhaAtdcURYAAAAAGFoDF1xRVgAAAAAYWgNXXFGWAAAAABhaA5dcUdYAAAAAGFoD11xSFgAAAAAYWgQXXFJWAAAAABhaBFdcUpYAAAAAGFoEl1xS1gAAAAAYWgTXXFMWAAAAABhaBRdcU1YAAAAAGFoFV1xTlgAAAAAYWgWXXFPWAAAAABhaCJdcVBYAAAAAGFoI11xUVgAAAAAYWgZXXFSKFggAAAAZlZWSUVtUXFhVFhDVjFpMFlSWlNSZnBjWWpOeFVWR29xU2gaZWgbXXFUWAAAAABhaBxdcVVoHWFoHl1xVlgBAAAAMWFoH11xV2ggYWghXXFYWAAAAABhaBddcVlYAAAAAGFoGF1xWlgAAAAAYWgkXXFbWAAAAABhaCVdcVxYAAAAAGFoLl1xXVgAAAAAYWgnXXFeWAAAAABhaChdcV9YAAAAAGFoKV1xYFgAAAAAYWgqXXFhWAAAAABhaCtdcWJYAAAAAGFoLF1xY2gtYWgmXXFkWAAAAABhaC9dcWVYAAAAAGFoMF1xZlgAAAAAYWgxXXFnWAAAAABhaDJdcWhYAAAAAGFoM11xaVgAAAAAYWg0XXFqaDVhaDZdcWtYAQAAADFhdVUIX211dGFibGVxbIh1Yi4=	25	1	\N	\N
2	f	1	gAJjZGphbmdvLmh0dHAKUXVlcnlEaWN0CnEBKYFxAihYCwAAAGdhc3N1cHBseV8xcQNYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8wcQRYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8xcQVYAAAAAFgNAAAAZ2Fzc3VwcGx5XzBfMXEGWAAAAABYDQAAAGdhc3N1cHBseV8wXzBxB1gAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzFxCFgAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzBxCVgAAAAAWAoAAAB0b3RhbF9hcmVhcQpYAAAAAFgIAAAAYmVzaWRlXzFxC1gAAAAAWAoAAAByb29tX2NvdW50cQxYAAAAAFgKAAAAaW50ZXJpb3JfMHENWAAAAABYCAAAAG9yaWdpbl8wcQ5YAAAAAFgKAAAAYmVzaWRlXzBfMHEPWAAAAABYCwAAAGZsb29yX2NvdW50cRBYAAAAAFgFAAAAZmxvb3JxEVgAAAAAWAgAAAByZWdpb25fMHESWAAAAABYDAAAAGFnZW5jeV9wcmljZXETWAAAAABYCQAAAGZhY2VfYXJlYXEUWAAAAABYEgAAAHdhbGxfY29uc3RydWNpb25fMHEVWAAAAABYDAAAAGRyaXZld2F5XzBfMHEWWAAAAABYEwAAAGNzcmZtaWRkbGV3YXJldG9rZW5xF1ggAAAAZlZWSUVtUXFhVFhDVjFpMFlSWlNSZnBjWWpOeFVWR29xGFgIAAAAYnJva2VyXzBxGVghAAAA0J/QsNCy0LXQuyDQodCw0LLQstC40L0gKHBpY2Fzc28pcRpYCAAAAGJyb2tlcl8xcRtYAQAAADFYBQAAAF9zYXZlcRxYEgAAANCh0L7RhdGA0LDQvdC40YLRjHEdWA8AAABlc3RhdGVfc3RhdHVzXzBxHlgAAAAAWAwAAABkcml2ZXdheV8wXzFxH1gAAAAAWAoAAABsb2NhbGl0eV8wcSBYAAAAAFgKAAAAc2V3ZXJhZ2VfMXEhWAAAAABYDwAAAG1pY3JvZGlzdHJpY3RfMHEiWAAAAABYCgAAAGRyaXZld2F5XzFxI1gAAAAAWAwAAABzZXdlcmFnZV8wXzFxJFgAAAAAWAwAAABzZXdlcmFnZV8wXzBxJVgAAAAAWAoAAABzdGVhZF9hcmVhcSZYAAAAAFgNAAAAZWxlY3RyaWNpdHlfMXEnWAAAAABYCgAAAGJlc2lkZV8wXzFxKFgAAAAAWA0AAABlc3RhdGVfdHlwZV8xcSlYAgAAADE2cSpYDQAAAGVzdGF0ZV90eXBlXzBxK1gOAAAA0J/QvtC70LTQvtC80LBxLFgKAAAAeWVhcl9idWlsdHEtWAAAAABYCQAAAGVzdGF0ZXNfMHEuWAAAAABYDQAAAHdhdGVyc3VwcGx5XzFxL1gAAAAAWAkAAAB1c2VkX2FyZWFxMFgAAAAAWAgAAABjbGllbnRfMHExWBkAAADQlNC+0Lwg0L3QsCDQotCw0LzQsNC90LggcTJYCAAAAGNsaWVudF8xcTNYAQAAADF1fXE0KFUJX2VuY29kaW5ncTVVBXV0Zi04cTZVBV9kYXRhcTd9cTgoaANdcTlYAAAAAGFoBF1xOlgAAAAAYWgFXXE7WAAAAABhaAZdcTxYAAAAAGFoB11xPVgAAAAAYWgIXXE+WAAAAABhaAldcT9YAAAAAGFoCl1xQFgAAAAAYWgLXXFBWAAAAABhaAxdcUJYAAAAAGFoDV1xQ1gAAAAAYWgOXXFEWAAAAABhaA9dcUVYAAAAAGFoEF1xRlgAAAAAYWgRXXFHWAAAAABhaBJdcUhYAAAAAGFoE11xSVgAAAAAYWgUXXFKWAAAAABhaBVdcUtYAAAAAGFoF11xTChYIAAAAGZWVklFbVFxYVRYQ1YxaTBZUlpTUmZwY1lqTnhVVkdvcU1oGGVoIF1xTlgAAAAAYWgZXXFPaBphaBtdcVBYAQAAADFhaBxdcVFoHWFoHl1xUlgAAAAAYWgfXXFTWAAAAABhaBZdcVRYAAAAAGFoIV1xVVgAAAAAYWgiXXFWWAAAAABhaCtdcVdoLGFoJF1xWFgAAAAAYWglXXFZWAAAAABhaCZdcVpYAAAAAGFoJ11xW1gAAAAAYWgoXXFcWAAAAABhaCldcV0oWAIAAAAzOXFeaCplaCNdcV9YAAAAAGFoLV1xYFgAAAAAYWguXXFhWAAAAABhaC9dcWJYAAAAAGFoMF1xY1gAAAAAYWgxXXFkaDJhaDNdcWVYAQAAADFhdVUIX211dGFibGVxZoh1Yi4=	34	1	\N	\N
3	f	2	gAJjZGphbmdvLmh0dHAKUXVlcnlEaWN0CnEBKYFxAihYCwAAAGdhc3N1cHBseV8xcQNYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8wcQRYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8xcQVYAAAAAFgNAAAAZ2Fzc3VwcGx5XzBfMXEGWAAAAABYDQAAAGdhc3N1cHBseV8wXzBxB1gAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzFxCFgAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzBxCVgAAAAAWAoAAAB0b3RhbF9hcmVhcQpYBwAAADEwMC0yMDBxC1gKAAAAbG9jYWxpdHlfMXEMWAMAAAAxMTBxDVgIAAAAYmVzaWRlXzFxDlgFAAAAMTAwMDBxD1gKAAAAcm9vbV9jb3VudHEQWAMAAAAyLTVxEVgKAAAAaW50ZXJpb3JfMXESWAEAAAAzWAoAAABpbnRlcmlvcl8wcRNYAAAAAFgIAAAAb3JpZ2luXzBxFFgAAAAAWAoAAABiZXNpZGVfMF8wcRVYGQAAANCQ0LfQvtCy0YHQutC+0LUg0LzQvtGA0LVxFlgLAAAAZmxvb3JfY291bnRxF1gAAAAAWAUAAABmbG9vcnEYWAMAAAAyLTVxGVgIAAAAcmVnaW9uXzFxGlgBAAAANFgIAAAAcmVnaW9uXzBxG1gAAAAAWAwAAABhZ2VuY3lfcHJpY2VxHFgOAAAANTAwMDAwLTEwMDAwMDBxHVgJAAAAZmFjZV9hcmVhcR5YAAAAAFgSAAAAd2FsbF9jb25zdHJ1Y2lvbl8xcR9YAQAAADZYEgAAAHdhbGxfY29uc3RydWNpb25fMHEgWAAAAABYDAAAAGRyaXZld2F5XzBfMHEhWAAAAABYEwAAAGNzcmZtaWRkbGV3YXJldG9rZW5xIlggAAAAYjZNMUFKVTVGVXZRTDQyVUd2U3BvN1BsdDNzU0tVMVVxI1gIAAAAYnJva2VyXzBxJFgmAAAA0KDQuNGN0LvRgtC+0YAg0JPQu9Cw0LLQvdGL0LkgKHJlYWx0eSlxJVgIAAAAYnJva2VyXzFxJlgBAAAAM1gFAAAAX3NhdmVxJ1gSAAAA0KHQvtGF0YDQsNC90LjRgtGMcShYDwAAAGVzdGF0ZV9zdGF0dXNfMHEpWAAAAABYDAAAAGRyaXZld2F5XzBfMXEqWAAAAABYCgAAAGxvY2FsaXR5XzBxK1gAAAAAWAoAAABzZXdlcmFnZV8xcSxYAAAAAFgPAAAAbWljcm9kaXN0cmljdF8wcS1YAAAAAFgKAAAAZHJpdmV3YXlfMXEuWAAAAABYDAAAAHNld2VyYWdlXzBfMXEvWAAAAABYDAAAAHNld2VyYWdlXzBfMHEwWAAAAABYCgAAAHN0ZWFkX2FyZWFxMVgBAAAAM1gNAAAAZWxlY3RyaWNpdHlfMXEyWAAAAABYCgAAAGJlc2lkZV8wXzFxM1gBAAAAMlgNAAAAZXN0YXRlX3R5cGVfMXE0WAIAAAAxNHE1WA0AAABlc3RhdGVfdHlwZV8wcTZYAAAAAFgKAAAAeWVhcl9idWlsdHE3WAkAAAAxOTgyLTE5OTBxOFgJAAAAZXN0YXRlc18wcTlYAAAAAFgNAAAAd2F0ZXJzdXBwbHlfMXE6WAAAAABYCQAAAHVzZWRfYXJlYXE7WAAAAABYCAAAAGNsaWVudF8wcTxYIQAAANCQ0L3QvdCwINCd0L7QstC+0YDQvtGB0YHQuNC50YHQunE9WAgAAABjbGllbnRfMXE+WAEAAAAydX1xPyhVCV9lbmNvZGluZ3FAVQV1dGYtOHFBVQVfZGF0YXFCfXFDKGgDXXFEWAAAAABhaARdcUVYAAAAAGFoBV1xRlgAAAAAYWgGXXFHWAAAAABhaAddcUhYAAAAAGFoCF1xSVgAAAAAYWgJXXFKWAAAAABhaApdcUtoC2FoDF1xTGgNYWgOXXFNaA9haBBdcU5oEWFoEl1xTyhYAQAAADhYAQAAADFYAQAAADNlaBNdcVBYAAAAAGFoFF1xUVgAAAAAYWgVXXFSaBZhaBddcVNYAAAAAGFoGF1xVGgZYWgaXXFVWAEAAAA0YWgbXXFWWAAAAABhaBxdcVdoHWFoHl1xWFgAAAAAYWgfXXFZKFgBAAAAMVgBAAAANmVoIF1xWlgAAAAAYWgiXXFbKFggAAAAYjZNMUFKVTVGVXZRTDQyVUd2U3BvN1BsdDNzU0tVMVVxXGgjZWgrXXFdWAAAAABhaCRdcV5oJWFoJl1xX1gBAAAAM2FoJ11xYGgoYWgpXXFhWAAAAABhaCpdcWJYAAAAAGFoIV1xY1gAAAAAYWgsXXFkWAAAAABhaC1dcWVYAAAAAGFoNl1xZlgAAAAAYWgvXXFnWAAAAABhaDBdcWhYAAAAAGFoMV1xaVgBAAAAM2FoMl1xalgAAAAAYWgzXXFrWAEAAAAyYWg0XXFsKFgCAAAAMTVxbWg1ZWguXXFuWAAAAABhaDddcW9oOGFoOV1xcFgAAAAAYWg6XXFxWAAAAABhaDtdcXJYAAAAAGFoPF1xc2g9YWg+XXF0WAEAAAAyYXVVCF9tdXRhYmxlcXWIdWIu	40	3	500000	1000000
4	f	2	gAJjZGphbmdvLmh0dHAKUXVlcnlEaWN0CnEBKYFxAihYCwAAAGdhc3N1cHBseV8xcQNYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8wcQRYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8xcQVYAAAAAFgNAAAAZ2Fzc3VwcGx5XzBfMXEGWAAAAABYDQAAAGdhc3N1cHBseV8wXzBxB1gAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzFxCFgAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzBxCVgAAAAAWAoAAAB0b3RhbF9hcmVhcQpYBwAAADEwMC0yMDBxC1gIAAAAYmVzaWRlXzFxDFgFAAAAMTAwMDBxDVgKAAAAcm9vbV9jb3VudHEOWAMAAAAyLTVxD1gKAAAAaW50ZXJpb3JfMHEQWAAAAABYCAAAAG9yaWdpbl8wcRFYAAAAAFgKAAAAYmVzaWRlXzBfMHESWBkAAADQkNC30L7QstGB0LrQvtC1INC80L7RgNC1cRNYCwAAAGZsb29yX2NvdW50cRRYAAAAAFgFAAAAZmxvb3JxFVgDAAAAMi01cRZYCAAAAHJlZ2lvbl8wcRdYAAAAAFgMAAAAYWdlbmN5X3ByaWNlcRhYDgAAADUwMDAwMC0xMDAwMDAwcRlYCQAAAGZhY2VfYXJlYXEaWAAAAABYEgAAAHdhbGxfY29uc3RydWNpb25fMHEbWAAAAABYDAAAAGRyaXZld2F5XzBfMHEcWAAAAABYEwAAAGNzcmZtaWRkbGV3YXJldG9rZW5xHVggAAAAYjZNMUFKVTVGVXZRTDQyVUd2U3BvN1BsdDNzU0tVMVVxHlgIAAAAYnJva2VyXzBxH1gmAAAA0KDQuNGN0LvRgtC+0YAg0JPQu9Cw0LLQvdGL0LkgKHJlYWx0eSlxIFgIAAAAYnJva2VyXzFxIVgBAAAAM1gFAAAAX3NhdmVxIlgSAAAA0KHQvtGF0YDQsNC90LjRgtGMcSNYDwAAAGVzdGF0ZV9zdGF0dXNfMHEkWAAAAABYDAAAAGRyaXZld2F5XzBfMXElWAAAAABYCgAAAGxvY2FsaXR5XzBxJlgAAAAAWAoAAABzZXdlcmFnZV8xcSdYAAAAAFgPAAAAbWljcm9kaXN0cmljdF8wcShYAAAAAFgKAAAAZHJpdmV3YXlfMXEpWAAAAABYDAAAAHNld2VyYWdlXzBfMXEqWAAAAABYDAAAAHNld2VyYWdlXzBfMHErWAAAAABYCgAAAHN0ZWFkX2FyZWFxLFgBAAAAM1gNAAAAZWxlY3RyaWNpdHlfMXEtWAAAAABYCgAAAGJlc2lkZV8wXzFxLlgBAAAAMlgNAAAAZXN0YXRlX3R5cGVfMXEvWAIAAAAxNXEwWA0AAABlc3RhdGVfdHlwZV8wcTFYRgAAANCj0YfQsNGB0YLQvtC6INC00LvRjyDRgdGC0YDQvtC40YLQtdC70YzRgdGC0LLQsCDQttC40LvQvtCz0L4g0LTQvtC80LBxMlgKAAAAeWVhcl9idWlsdHEzWAkAAAAxOTgyLTE5OTBxNFgJAAAAZXN0YXRlc18wcTVYAAAAAFgNAAAAd2F0ZXJzdXBwbHlfMXE2WAAAAABYCQAAAHVzZWRfYXJlYXE3WAAAAABYCAAAAGNsaWVudF8wcThYIQAAANCQ0L3QvdCwINCd0L7QstC+0YDQvtGB0YHQuNC50YHQunE5WAgAAABjbGllbnRfMXE6WAEAAAAydX1xOyhVCV9lbmNvZGluZ3E8VQV1dGYtOHE9VQVfZGF0YXE+fXE/KGgDXXFAWAAAAABhaARdcUFYAAAAAGFoBV1xQlgAAAAAYWgGXXFDWAAAAABhaAddcURYAAAAAGFoCF1xRVgAAAAAYWgJXXFGWAAAAABhaApdcUdoC2FoDF1xSGgNYWgOXXFJaA9haBBdcUpYAAAAAGFoEV1xS1gAAAAAYWgSXXFMaBNhaBRdcU1YAAAAAGFoFV1xTmgWYWgXXXFPWAAAAABhaBhdcVBoGWFoGl1xUVgAAAAAYWgbXXFSWAAAAABhaB1dcVMoWCAAAABiNk0xQUpVNUZVdlFMNDJVR3ZTcG83UGx0M3NTS1UxVXFUaB5laCZdcVVYAAAAAGFoH11xVmggYWghXXFXWAEAAAAzYWgiXXFYaCNhaCRdcVlYAAAAAGFoJV1xWlgAAAAAYWgcXXFbWAAAAABhaCddcVxYAAAAAGFoKF1xXVgAAAAAYWgxXXFeaDJhaCpdcV9YAAAAAGFoK11xYFgAAAAAYWgsXXFhWAEAAAAzYWgtXXFiWAAAAABhaC5dcWNYAQAAADJhaC9dcWRoMGFoKV1xZVgAAAAAYWgzXXFmaDRhaDVdcWdYAAAAAGFoNl1xaFgAAAAAYWg3XXFpWAAAAABhaDhdcWpoOWFoOl1xa1gBAAAAMmF1VQhfbXV0YWJsZXFsiHViLg==	41	3	500000	1000000
5	f	2	gAJjZGphbmdvLmh0dHAKUXVlcnlEaWN0CnEBKYFxAihYCwAAAGdhc3N1cHBseV8xcQNYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8wcQRYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8xcQVYAAAAAFgNAAAAZ2Fzc3VwcGx5XzBfMXEGWAAAAABYDQAAAGdhc3N1cHBseV8wXzBxB1gAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzFxCFgAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzBxCVgAAAAAWAoAAAB0b3RhbF9hcmVhcQpYBwAAADEwMC0yMDBxC1gIAAAAYmVzaWRlXzFxDFgFAAAAMTAwMDBxDVgKAAAAcm9vbV9jb3VudHEOWAMAAAAyLTVxD1gKAAAAaW50ZXJpb3JfMHEQWAAAAABYCAAAAG9yaWdpbl8wcRFYAAAAAFgKAAAAYmVzaWRlXzBfMHESWBkAAADQkNC30L7QstGB0LrQvtC1INC80L7RgNC1cRNYCwAAAGZsb29yX2NvdW50cRRYAAAAAFgFAAAAZmxvb3JxFVgDAAAAMi01cRZYCAAAAHJlZ2lvbl8wcRdYAAAAAFgMAAAAYWdlbmN5X3ByaWNlcRhYDgAAADUwMDAwMC0xMDAwMDAwcRlYCQAAAGZhY2VfYXJlYXEaWAAAAABYEgAAAHdhbGxfY29uc3RydWNpb25fMHEbWAAAAABYDAAAAGRyaXZld2F5XzBfMHEcWAAAAABYEwAAAGNzcmZtaWRkbGV3YXJldG9rZW5xHVggAAAAYjZNMUFKVTVGVXZRTDQyVUd2U3BvN1BsdDNzU0tVMVVxHlgIAAAAYnJva2VyXzBxH1gmAAAA0KDQuNGN0LvRgtC+0YAg0JPQu9Cw0LLQvdGL0LkgKHJlYWx0eSlxIFgIAAAAYnJva2VyXzFxIVgBAAAAM1gFAAAAX3NhdmVxIlgSAAAA0KHQvtGF0YDQsNC90LjRgtGMcSNYDwAAAGVzdGF0ZV9zdGF0dXNfMHEkWAAAAABYDAAAAGRyaXZld2F5XzBfMXElWAAAAABYCgAAAGxvY2FsaXR5XzBxJlgAAAAAWAoAAABzZXdlcmFnZV8xcSdYAAAAAFgPAAAAbWljcm9kaXN0cmljdF8wcShYAAAAAFgKAAAAZHJpdmV3YXlfMXEpWAAAAABYDAAAAHNld2VyYWdlXzBfMXEqWAAAAABYDAAAAHNld2VyYWdlXzBfMHErWAAAAABYCgAAAHN0ZWFkX2FyZWFxLFgBAAAAM1gNAAAAZWxlY3RyaWNpdHlfMXEtWAAAAABYCgAAAGJlc2lkZV8wXzFxLlgBAAAAMlgNAAAAZXN0YXRlX3R5cGVfMXEvWAIAAAAxNXEwWA0AAABlc3RhdGVfdHlwZV8wcTFYBgAAANCU0L7QvHEyWAoAAAB5ZWFyX2J1aWx0cTNYCQAAADE5ODItMTk5MHE0WAkAAABlc3RhdGVzXzBxNVgAAAAAWA0AAAB3YXRlcnN1cHBseV8xcTZYAAAAAFgJAAAAdXNlZF9hcmVhcTdYAAAAAFgIAAAAY2xpZW50XzBxOFghAAAA0JDQvdC90LAg0J3QvtCy0L7RgNC+0YHRgdC40LnRgdC6cTlYCAAAAGNsaWVudF8xcTpYAQAAADJ1fXE7KFUJX2VuY29kaW5ncTxVBXV0Zi04cT1VBV9kYXRhcT59cT8oaANdcUBYAAAAAGFoBF1xQVgAAAAAYWgFXXFCWAAAAABhaAZdcUNYAAAAAGFoB11xRFgAAAAAYWgIXXFFWAAAAABhaAldcUZYAAAAAGFoCl1xR2gLYWgMXXFIaA1haA5dcUloD2FoEF1xSlgAAAAAYWgRXXFLWAAAAABhaBJdcUxoE2FoFF1xTVgAAAAAYWgVXXFOaBZhaBddcU9YAAAAAGFoGF1xUGgZYWgaXXFRWAAAAABhaBtdcVJYAAAAAGFoHV1xUyhYIAAAAGI2TTFBSlU1RlV2UUw0MlVHdlNwbzdQbHQzc1NLVTFVcVRoHmVoJl1xVVgAAAAAYWgfXXFWaCBhaCFdcVdYAQAAADNhaCJdcVhoI2FoJF1xWVgAAAAAYWglXXFaWAAAAABhaBxdcVtYAAAAAGFoJ11xXFgAAAAAYWgoXXFdWAAAAABhaDFdcV5oMmFoKl1xX1gAAAAAYWgrXXFgWAAAAABhaCxdcWFYAQAAADNhaC1dcWJYAAAAAGFoLl1xY1gBAAAAMmFoL11xZChYAgAAADE2cWVoMGVoKV1xZlgAAAAAYWgzXXFnaDRhaDVdcWhYAAAAAGFoNl1xaVgAAAAAYWg3XXFqWAAAAABhaDhdcWtoOWFoOl1xbFgBAAAAMmF1VQhfbXV0YWJsZXFtiHViLg==	42	3	500000	1000000
6	f	2	gAJjZGphbmdvLmh0dHAKUXVlcnlEaWN0CnEBKYFxAihYCwAAAGdhc3N1cHBseV8xcQNYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8wcQRYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8xcQVYAAAAAFgNAAAAZ2Fzc3VwcGx5XzBfMXEGWAAAAABYDQAAAGdhc3N1cHBseV8wXzBxB1gAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzFxCFgAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzBxCVgAAAAAWAoAAAB0b3RhbF9hcmVhcQpYAAAAAFgIAAAAYmVzaWRlXzFxC1gAAAAAWAoAAAByb29tX2NvdW50cQxYAAAAAFgKAAAAaW50ZXJpb3JfMHENWAAAAABYCAAAAG9yaWdpbl8wcQ5YAAAAAFgKAAAAYmVzaWRlXzBfMHEPWAAAAABYCwAAAGZsb29yX2NvdW50cRBYAAAAAFgFAAAAZmxvb3JxEVgAAAAAWAgAAAByZWdpb25fMHESWAAAAABYDAAAAGFnZW5jeV9wcmljZXETWAAAAABYCQAAAGZhY2VfYXJlYXEUWAAAAABYEgAAAHdhbGxfY29uc3RydWNpb25fMHEVWAAAAABYDAAAAGRyaXZld2F5XzBfMHEWWAAAAABYEwAAAGNzcmZtaWRkbGV3YXJldG9rZW5xF1ggAAAAWEt0djJ6WXh3QlFRcDNPS1pYOXNZUmt5QVhDM3FxVnVxGFgIAAAAYnJva2VyXzBxGVgmAAAA0KDQuNGN0LvRgtC+0YAg0JPQu9Cw0LLQvdGL0LkgKHJlYWx0eSlxGlgIAAAAYnJva2VyXzFxG1gBAAAAM1gFAAAAX3NhdmVxHFgSAAAA0KHQvtGF0YDQsNC90LjRgtGMcR1YDwAAAGVzdGF0ZV9zdGF0dXNfMHEeWAAAAABYDAAAAGRyaXZld2F5XzBfMXEfWAAAAABYCgAAAGxvY2FsaXR5XzBxIFgAAAAAWAoAAABzZXdlcmFnZV8xcSFYAAAAAFgPAAAAbWljcm9kaXN0cmljdF8wcSJYAAAAAFgKAAAAZHJpdmV3YXlfMXEjWAAAAABYDAAAAHNld2VyYWdlXzBfMXEkWAAAAABYDAAAAHNld2VyYWdlXzBfMHElWAAAAABYCgAAAHN0ZWFkX2FyZWFxJlgAAAAAWA0AAABlbGVjdHJpY2l0eV8xcSdYAAAAAFgKAAAAYmVzaWRlXzBfMXEoWAAAAABYDQAAAGVzdGF0ZV90eXBlXzFxKVgCAAAAMThxKlgNAAAAZXN0YXRlX3R5cGVfMHErWAAAAABYCgAAAHllYXJfYnVpbHRxLFgAAAAAWAkAAABlc3RhdGVzXzBxLVgAAAAAWA0AAAB3YXRlcnN1cHBseV8xcS5YAAAAAFgJAAAAdXNlZF9hcmVhcS9YAAAAAFgIAAAAY2xpZW50XzBxMFghAAAA0JDQvdC90LAg0J3QvtCy0L7RgNC+0YHRgdC40LnRgdC6cTFYCAAAAGNsaWVudF8xcTJYAQAAADJ1fXEzKFUJX2VuY29kaW5ncTRVBXV0Zi04cTVVBV9kYXRhcTZ9cTcoaANdcThYAAAAAGFoBF1xOVgAAAAAYWgFXXE6WAAAAABhaAZdcTtYAAAAAGFoB11xPFgAAAAAYWgIXXE9WAAAAABhaAldcT5YAAAAAGFoCl1xP1gAAAAAYWgLXXFAWAAAAABhaAxdcUFYAAAAAGFoDV1xQlgAAAAAYWgOXXFDWAAAAABhaA9dcURYAAAAAGFoEF1xRVgAAAAAYWgRXXFGWAAAAABhaBJdcUdYAAAAAGFoE11xSFgAAAAAYWgUXXFJWAAAAABhaBVdcUpYAAAAAGFoF11xSyhYIAAAAFhLdHYyell4d0JRUXAzT0taWDlzWVJreUFYQzNxcVZ1cUxoGGVoIF1xTVgAAAAAYWgZXXFOaBphaBtdcU9YAQAAADNhaBxdcVBoHWFoHl1xUVgAAAAAYWgfXXFSWAAAAABhaBZdcVNYAAAAAGFoIV1xVFgAAAAAYWgiXXFVWAAAAABhaCtdcVZYAAAAAGFoJF1xV1gAAAAAYWglXXFYWAAAAABhaCZdcVlYAAAAAGFoJ11xWlgAAAAAYWgoXXFbWAAAAABhaCldcVxoKmFoI11xXVgAAAAAYWgsXXFeWAAAAABhaC1dcV9YAAAAAGFoLl1xYFgAAAAAYWgvXXFhWAAAAABhaDBdcWJoMWFoMl1xY1gBAAAAMmF1VQhfbXV0YWJsZXFkiHViLg==	43	3	500000	1000000
7	f	6	gAJjZGphbmdvLmh0dHAKUXVlcnlEaWN0CnEBKYFxAihYCwAAAGdhc3N1cHBseV8xcQNYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8wcQRYAAAAAFgPAAAAZWxlY3RyaWNpdHlfMF8xcQVYAAAAAFgNAAAAZ2Fzc3VwcGx5XzBfMXEGWAAAAABYDQAAAGdhc3N1cHBseV8wXzBxB1gAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzFxCFgAAAAAWA8AAAB3YXRlcnN1cHBseV8wXzBxCVgAAAAAWAoAAAB0b3RhbF9hcmVhcQpYAAAAAFgKAAAAbG9jYWxpdHlfMXELWAEAAAAzWAgAAABiZXNpZGVfMXEMWAAAAABYCgAAAHJvb21fY291bnRxDVgAAAAAWAoAAABpbnRlcmlvcl8wcQ5YAAAAAFgIAAAAb3JpZ2luXzBxD1gAAAAAWAoAAABiZXNpZGVfMF8wcRBYAAAAAFgLAAAAZmxvb3JfY291bnRxEVgAAAAAWAUAAABmbG9vcnESWAAAAABYCAAAAHJlZ2lvbl8xcRNYAQAAADFYCAAAAHJlZ2lvbl8wcRRYAAAAAFgMAAAAYWdlbmN5X3ByaWNlcRVYDAAAANC00L4gMzAwMDAwMHEWWAkAAABmYWNlX2FyZWFxF1gAAAAAWBIAAAB3YWxsX2NvbnN0cnVjaW9uXzBxGFgAAAAAWAwAAABkcml2ZXdheV8wXzBxGVgAAAAAWBMAAABjc3JmbWlkZGxld2FyZXRva2VucRpYIAAAAExJcVJMUW1KT1FBT1c5b1RjaWl4THk5RVl3cEtwWVVocRtYCAAAAGJyb2tlcl8wcRxYJgAAANCg0LjRjdC70YLQvtGAINCT0LvQsNCy0L3Ri9C5IChyZWFsdHkpcR1YCAAAAGJyb2tlcl8xcR5YAQAAADNYBQAAAF9zYXZlcR9YEgAAANCh0L7RhdGA0LDQvdC40YLRjHEgWA8AAABlc3RhdGVfc3RhdHVzXzBxIVgAAAAAWAwAAABkcml2ZXdheV8wXzFxIlgAAAAAWAoAAABsb2NhbGl0eV8wcSNYAAAAAFgKAAAAc2V3ZXJhZ2VfMXEkWAAAAABYDwAAAG1pY3JvZGlzdHJpY3RfMHElWAAAAABYCgAAAGRyaXZld2F5XzFxJlgAAAAAWAwAAABzZXdlcmFnZV8wXzFxJ1gAAAAAWAwAAABzZXdlcmFnZV8wXzBxKFgAAAAAWAoAAABzdGVhZF9hcmVhcSlYAAAAAFgNAAAAZWxlY3RyaWNpdHlfMXEqWAAAAABYCgAAAGJlc2lkZV8wXzFxK1gAAAAAWA0AAABlc3RhdGVfdHlwZV8xcSxYAgAAADM0cS1YDQAAAGVzdGF0ZV90eXBlXzBxLlgAAAAAWAoAAAB5ZWFyX2J1aWx0cS9YAAAAAFgJAAAAZXN0YXRlc18xcTBYAgAAADMycTFYCQAAAGVzdGF0ZXNfMHEyWAAAAABYDQAAAHdhdGVyc3VwcGx5XzFxM1gAAAAAWAkAAAB1c2VkX2FyZWFxNFgAAAAAWAgAAABjbGllbnRfMHE1WBUAAADQm9C10L3QsCDQnNC+0YHQutCy0LBxNlgIAAAAY2xpZW50XzFxN1gBAAAANnV9cTgoVQlfZW5jb2RpbmdxOVUFdXRmLThxOlUFX2RhdGFxO31xPChoA11xPVgAAAAAYWgEXXE+WAAAAABhaAVdcT9YAAAAAGFoBl1xQFgAAAAAYWgHXXFBWAAAAABhaAhdcUJYAAAAAGFoCV1xQ1gAAAAAYWgKXXFEWAAAAABhaAtdcUVYAQAAADNhaAxdcUZYAAAAAGFoDV1xR1gAAAAAYWgOXXFIWAAAAABhaA9dcUlYAAAAAGFoEF1xSlgAAAAAYWgRXXFLWAAAAABhaBJdcUxYAAAAAGFoE11xTVgBAAAAMWFoFF1xTlgAAAAAYWgVXXFPaBZhaBddcVBYAAAAAGFoGF1xUVgAAAAAYWgaXXFSKFggAAAATElxUkxRbUpPUUFPVzlvVGNpaXhMeTlFWXdwS3BZVWhxU2gbZWgjXXFUWAAAAABhaBxdcVVoHWFoHl1xVlgBAAAAM2FoH11xV2ggYWghXXFYWAAAAABhaCJdcVlYAAAAAGFoGV1xWlgAAAAAYWgkXXFbWAAAAABhaCVdcVxYAAAAAGFoLl1xXVgAAAAAYWgnXXFeWAAAAABhaChdcV9YAAAAAGFoKV1xYFgAAAAAYWgqXXFhWAAAAABhaCtdcWJYAAAAAGFoLF1xYyhYAQAAADZoLWVoJl1xZFgAAAAAYWgvXXFlWAAAAABhaDBdcWYoWAIAAAAyNHFnWAIAAAAzNXFoaDFlaDJdcWlYAAAAAGFoM11xalgAAAAAYWg0XXFrWAAAAABhaDVdcWxoNmFoN11xbVgBAAAANmF1VQhfbXV0YWJsZXFuiHViLg==	57	3	\N	\N
\.


--
-- Data for Name: estatebase_bid_estate_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_bid_estate_types (id, bid_id, estatetype_id) FROM stdin;
3	2	39
4	2	16
5	3	15
6	3	14
7	4	15
8	5	15
9	5	16
10	7	6
11	7	34
12	6	18
\.


--
-- Data for Name: estatebase_bid_estates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_bid_estates (id, bid_id, estate_id) FROM stdin;
1	7	24
2	7	32
3	7	35
\.


--
-- Data for Name: estatebase_bid_localities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_bid_localities (id, bid_id, locality_id) FROM stdin;
1	3	110
2	7	3
\.


--
-- Data for Name: estatebase_bid_regions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_bid_regions (id, bid_id, region_id) FROM stdin;
1	3	4
2	7	1
\.


--
-- Data for Name: estatebase_bidg; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_bidg (id, estate_id, estate_type_id, room_number, year_built, floor, floor_count, elevator, wall_construcion_id, exterior_finish_id, window_type_id, roof_id, heating_id, ceiling_height, room_count, total_area, used_area, wall_finish_id, flooring_id, ceiling_id, interior_id, basic) FROM stdin;
26	24	6		\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	1	2	1	1	t
36	26	10	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
37	26	2	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
31	26	27	\N	2001	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	1	1	3	5	t
38	27	37	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
39	28	45	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	t
40	28	12	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
27	25	39		2001	2	2	t	2	4	3	2	2	2.92	1	2.00	202.00	2	\N	\N	5	t
28	25	27	\N	2001	5	5	t	1	4	4	3	3	3.00	\N	\N	\N	\N	\N	\N	7	f
29	25	29	\N	2001	\N	5	f	1	2	\N	\N	\N	\N	4	4.00	\N	2	1	1	3	f
41	30	40	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	t
42	31	28	17	1998	3	9	t	8	\N	4	\N	4	\N	1	35.00	18.00	5	6	8	11	t
43	32	16	\N	1982	1	1	f	1	5	4	1	1	2.60	4	500.00	200.00	8	8	6	3	t
45	33	10	\N	2001	2	2	f	1	3	4	2	3	3.00	6	200.00	100.00	5	6	2	7	t
47	35	16	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	t
44	32	12	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
49	38	22	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	t
50	39	18	8	1999	2	2	f	1	5	4	\N	1	2.30	3	60.00	40.00	5	5	4	7	t
51	30	29	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
52	30	7	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
48	36	16	\N	1990	1	\N	f	2	6	1	1	1	2.50	5	200.00	1250.00	7	8	6	3	t
53	36	5	\N	1990	\N	1	f	1	3	\N	\N	\N	\N	2	30.00	\N	5	5	3	4	f
54	36	2	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
55	34	5	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
46	34	16	\N	\N	\N	\N	f	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	t
57	39	26	\N	\N	\N	\N	f	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f
56	39	23	\N	1989	\N	2	f	2	5	\N	\N	\N	\N	5	70.00	\N	3	1	1	11	f
\.


--
-- Data for Name: estatebase_bidg_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_bidg_documents (id, bidg_id, document_id) FROM stdin;
8	31	4
9	31	5
10	31	6
11	27	4
12	27	5
13	27	6
14	28	6
15	42	4
16	42	5
17	42	6
18	43	4
19	43	5
20	43	6
21	45	4
22	45	5
23	45	6
24	50	4
25	50	5
26	50	6
27	48	4
28	48	5
29	48	6
\.


--
-- Data for Name: estatebase_ceiling; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_ceiling (id, name) FROM stdin;
1	без отделки
2	гипсокартон
3	натяжные
4	окрашены
5	оштукатурены
6	пластик
7	побелены
8	подвесные
\.


--
-- Data for Name: estatebase_client; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_client (id, deleted, name, client_type_id, origin_id, address, note, history_id, broker_id) FROM stdin;
1	f	Дом на Тамани	2	\N		Заказчик	12	1
2	f	Анна	3	2	Новороссийск		38	3
3	f	Мария	3	12	Темрюк		45	3
4	f	Галина	1	3	Анапа		52	3
5	f	Сергей Андреевич	3	1	Темрюк		54	3
6	f	Лена	3	14	Москва	хорошая с деньгами	56	3
7	f	Штригель Олег	3	14	Новороссийск	умный мужчина	58	3
8	f	Анапастрой	3	13	Анапа		59	3
\.


--
-- Data for Name: estatebase_clienttype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_clienttype (id, name) FROM stdin;
1	Риелтор
2	Агенство
3	Частное лицо
\.


--
-- Data for Name: estatebase_comstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_comstatus (id, name, status) FROM stdin;
1	Используется	1
2	Возможно	2
3	Нет возможности	0
\.


--
-- Data for Name: estatebase_contact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_contact (id, client_id, contact_type_id, contact, updated, contact_state_id) FROM stdin;
1	1	1	777-777-77	2012-10-13 20:19:36.356574+04	1
2	2	1	89180410666	2012-10-18 12:18:28.872674+04	1
3	2	2	shtrigel@mail.ru	2012-10-18 12:18:28.905071+04	5
4	3	1	89184835142	2012-10-19 09:57:44.437856+04	1
5	3	2	123@mail.ru	2012-10-19 09:57:44.454143+04	1
6	4	1	89161877403	2012-10-19 13:45:41.097028+04	5
7	5	1	89886589569	2012-10-19 13:50:00.990678+04	5
8	6	2	vite@yandex.ru	2012-10-19 13:59:45.451515+04	5
9	7	1	89887622448	2012-10-19 14:13:59.475647+04	1
10	8	1	84958974535	2012-10-19 21:24:44.681563+04	5
\.


--
-- Data for Name: estatebase_contacthistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_contacthistory (id, event_date, user_id, contact_state_id, contact_id) FROM stdin;
1	2012-10-07 23:31:39.727457+04	1	1	1
2	2012-10-13 20:19:36.356574+04	1	1	1
3	2012-10-18 12:18:25.189692+04	3	1	2
4	2012-10-18 12:18:25.338812+04	3	5	3
5	2012-10-19 09:57:44.437856+04	3	1	4
6	2012-10-19 09:57:44.454143+04	3	1	5
7	2012-10-19 13:45:37.19761+04	3	5	6
8	2012-10-19 13:50:00.990678+04	3	5	7
9	2012-10-19 13:59:40.952686+04	3	5	8
10	2012-10-19 14:05:40.470032+04	3	1	9
11	2012-10-19 21:24:40.304173+04	3	5	10
\.


--
-- Data for Name: estatebase_contactstate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_contactstate (id, name) FROM stdin;
1	Доступен
2	Недоступен
3	Заблокирован
4	Нет ответа
5	Не проверен
\.


--
-- Data for Name: estatebase_contacttype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_contacttype (id, name) FROM stdin;
1	Телефон
2	Email
3	Веб-сайт
\.


--
-- Data for Name: estatebase_document; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_document (id, name) FROM stdin;
6	Кадастровый номер
8	Межевой план
4	Свидетельство
7	Свидетельство на участок
5	Технический паспорт
\.


--
-- Data for Name: estatebase_document_estate_type_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_document_estate_type_category (id, document_id, estatetypecategory_id) FROM stdin;
24	6	1
25	6	2
26	6	5
27	6	4
28	6	6
29	6	8
30	8	8
31	4	1
32	4	2
33	4	5
34	4	4
35	4	6
36	7	8
37	5	1
38	5	2
39	5	5
40	5	4
41	5	6
\.


--
-- Data for Name: estatebase_driveway; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_driveway (id, name) FROM stdin;
1	Асфальт
2	Гравийный
3	Грунтовый
4	Нет
5	Хороший
\.


--
-- Data for Name: estatebase_electricity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_electricity (id, name) FROM stdin;
1	На расстоянии
2	По меже
3	Подведено
4	Подключение оплачено
5	Подключено
6	Технические условия
\.


--
-- Data for Name: estatebase_estate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estate (id, deleted, region_id, locality_id, microdistrict_id, street_id, estate_number, origin_id, beside_id, beside_distance, saler_price, agency_price, estate_status_id, electricity_id, electricity_distance, watersupply_id, watersupply_distance, gassupply_id, gassupply_distance, sewerage_id, sewerage_distance, telephony_id, internet_id, driveway_id, driveway_distance, description, comment, history_id, contact_id, valid, broker_id, estate_category_id, com_status_id) FROM stdin;
27	f	4	8	\N	\N		2	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	29	\N	f	1	8	\N
28	f	4	9	\N	\N		4	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	30	\N	f	1	5	1
29	f	4	\N	\N	\N		5	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	31	1	t	1	8	2
25	f	4	10	\N	\N	1	2	2	22	1000000	1000100	1	1	\N	2	\N	3	\N	3	\N	2	1	3	\N		Очень хорошо	27	1	t	1	2	1
24	f	2	7	\N	\N		2	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	26	1	t	1	4	3
26	f	3	1	\N	\N		4	\N	\N	\N	\N	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N			28	1	t	1	6	\N
31	f	3	80	\N	\N		3	12	700	1900000	1950000	1	5	\N	7	\N	5	\N	5	\N	\N	\N	\N	\N	\N	\N	37	\N	f	1	4	\N
32	f	3	80	\N	\N	11	12	12	1000	20000000	21000000	2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	39	\N	f	3	2	1
33	f	1	104	\N	\N		1	12	100	2000000	2100000	2	5	\N	8	\N	1	\N	6	\N	2	2	1	\N	на 1 этаже: 3 спальные комнаты, 2 санузла, холл, кухня/столовая, на 2 этаже: 3 гостевые благоустроенные комнаты, кухня/столовая, холл	не очень приятный тип	44	4	t	3	6	1
35	f	1	4	\N	\N		1	\N	\N	\N	\N	2	5	\N	7	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	47	4	t	3	2	3
37	f	4	69	\N	\N	9	5	2	200	200000	250000	1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	51	6	f	3	8	2
38	f	2	65	\N	\N	12	6	12	\N	9000000	9300000	1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	53	7	f	3	5	2
30	f	3	15	\N	\N		3	\N	\N	20000000	21000000	1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	32	9	t	1	6	1
36	f	1	3	\N	\N		12	\N	\N	340000	400000	1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	48	9	t	3	2	2
34	f	1	\N	\N	\N		\N	\N	\N	\N	\N	2	5	\N	7	\N	2	\N	3	\N	3	1	3	\N			46	1	t	3	2	2
39	f	3	41	\N	\N	12	12	12	3000	2000000	2100000	3	2	\N	8	\N	1	100	1	100	2	2	4	\N	техника дорогая, 10 сплит-систем, 20 антенн	проехать налево, направо, по улице вверх, тетя Глаша	55	9	t	3	5	1
\.


--
-- Data for Name: estatebase_estate_estate_params; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estate_estate_params (id, estate_id, estateparam_id) FROM stdin;
6	26	5
7	26	6
8	25	1
9	25	2
16	34	1
17	34	2
18	39	1
19	39	2
20	39	3
21	39	4
22	39	5
23	39	6
\.


--
-- Data for Name: estatebase_estateclient; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estateclient (id, client_id, estate_id, estate_client_status_id) FROM stdin;
8	1	24	3
9	1	25	3
10	1	29	3
11	1	26	3
12	3	33	3
13	1	34	3
14	3	35	3
15	4	37	3
16	5	38	3
17	7	39	3
18	7	30	3
20	8	36	3
21	7	36	3
\.


--
-- Data for Name: estatebase_estateclientstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estateclientstatus (id, name) FROM stdin;
1	Знакомый
2	Показывает
3	Собственник
4	Родственник
5	Сосед
\.


--
-- Data for Name: estatebase_estateparam; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estateparam (id, "order", name) FROM stdin;
1	1	На сайт
2	2	Ипотека
3	3	Обмен
4	4	Рекламировать
5	5	Сделать фото
6	6	Эксклюзив
\.


--
-- Data for Name: estatebase_estatephoto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estatephoto (id, "order", estate_id, name, note, image) FROM stdin;
1	1	26	\N	\N	photos/26/hubble-space-wallpaper-1920x1200-1010166.jpg
2	2	26	\N	\N	photos/26/milky_way_galaxy_1920x1200.jpg
3	3	26	\N	\N	photos/26/blue_stars_1_1920x1200.jpg
4	4	24	\N	\N	photos/24/hubble-space-wallpaper-1920x1200-1010166.jpg
5	5	30	\N	\N	photos/30/hubble-space-wallpaper-1920x1200-1010166.jpg
6	6	28	\N	\N	photos/28/milky_way_galaxy_1920x1200.jpg
7	7	29	\N	\N	photos/29/f2601-M31.JPG
8	8	29	\N	\N	photos/29/hubble-space-wallpaper-1920x1200-1010166.jpg
9	9	29	\N	\N	photos/29/milky_way_galaxy_1920x1200.jpg
10	10	29	\N	\N	photos/29/space_galactic_super_winds_1600x1200.jpg
11	11	27	\N	\N	photos/27/blue_stars_1_1920x1200.jpg
12	12	25	\N	\N	photos/25/blue_stars_1_1920x1200.jpg
13	13	25	\N	\N	photos/25/f2601-M31.JPG
14	14	25	\N	\N	photos/25/hubble-space-wallpaper-1920x1200-1010166.jpg
15	15	25	\N	\N	photos/25/hubble_space_telescope_crab_bebula.jpg
16	16	25	\N	\N	photos/25/milky_way_galaxy_1920x1200.jpg
17	17	25	\N	\N	photos/25/space_galactic_super_winds_1600x1200.jpg
18	18	27	\N	\N	photos/27/hubble-space-wallpaper-1920x1200-1010166.jpg
19	19	30	\N	\N	photos/30/DSC06437.JPG
20	20	30	\N	\N	photos/30/DSC06439.JPG
21	21	30	\N	\N	photos/30/DSC06441.JPG
\.


--
-- Data for Name: estatebase_estateregister; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estateregister (id, deleted, name, history_id, broker_id) FROM stdin;
1	f	По заявке [1]	33	1
2	t	По заявке [2]	35	1
3	f	По заявке [2]	36	1
4	f	По заявке [2]	49	3
5	f	участки в Анапе до 1 млн. руб.	50	3
6	f	Участки Анапа до 1 000 000 рублей	60	3
8	f	По заявке [6]	62	3
7	t	По заявке [6]	61	3
9	t	Автомат	63	3
\.


--
-- Data for Name: estatebase_estateregister_bids; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estateregister_bids (id, estateregister_id, bid_id) FROM stdin;
1	1	1
2	2	2
3	3	2
6	5	2
7	6	6
8	7	6
9	8	6
10	9	3
\.


--
-- Data for Name: estatebase_estateregister_estates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estateregister_estates (id, estateregister_id, estate_id) FROM stdin;
1	1	30
2	3	25
3	3	26
4	4	25
5	4	34
6	4	35
10	5	25
11	5	34
12	5	35
13	6	39
14	6	38
15	6	36
16	8	39
17	8	38
\.


--
-- Data for Name: estatebase_estatestatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estatestatus (id, name) FROM stdin;
1	Вакантно
2	Новый
3	Продано
4	Снят с продажи
\.


--
-- Data for Name: estatebase_estatetype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estatetype (id, "order", name, estate_type_category_id, note, placeable, template) FROM stdin;
13	13	Дача	2	\N	f	2
16	16	Дом	2	\N	t	2
39	39	Полдома	2	\N	t	2
6	6	Вторичка	4	\N	f	0
21	21	Комната	4	\N	f	0
28	28	Малосемейка	4	\N	f	0
34	34	Новостройка	4	\N	f	1
18	18	Квартира с участком	5	\N	t	0
22	22	Коттедж	5	\N	t	0
45	45	Таунхаус	5	\N	t	0
1	1	База отдыха	6	\N	t	2
4	4	Винзавод	6	\N	t	2
10	10	Гостевой дом	6	\N	t	2
11	11	Гостевые комнаты	6	\N	t	2
12	12	Гостиница	6	\N	t	2
27	27	Магазин	6	\N	t	2
30	30	Минигостиница	6	\N	t	2
33	33	Нежилое помещение	6	\N	t	0
35	35	Офис	6	\N	t	2
36	36	Пансионат	6	\N	t	2
40	40	Производственная база	6	\N	t	2
44	44	Строение для отдыхающих	6	\N	t	2
46	46	Торговый павильон	6	\N	t	2
9	9	Гараж	1	\N	t	4
8	8	Гараж лодочный	1	\N	t	4
2	2	Баня	7	\N	t	4
3	3	Ветхий дом	7	\N	t	4
5	5	Времянка	7	\N	t	4
7	7	Гараж	7	\N	t	4
17	17	Забор	7	\N	t	4
19	19	Колодец	7	\N	t	4
23	23	Летний дом	7	\N	t	4
24	24	Летний душ	7	\N	t	4
26	26	Летняя кухня	7	\N	t	4
25	25	Летняя кухня	7	\N	t	4
29	29	Мастерская	7	\N	t	4
31	31	Навес	7	\N	t	4
32	32	Недострой	7	\N	t	4
37	37	Погреб	7	\N	t	4
38	38	Подвал	7	\N	t	4
41	41	Сад	7	\N	t	4
43	43	Стоянка	7	\N	t	4
47	47	Уборная	7	\N	t	4
48	48	Фундамент	7	\N	t	4
49	49	Хозблок	7	\N	t	4
50	50	Хозяйственные постройки	7	\N	t	4
14	14	Дачный участок	8		f	3
42	42	Участок сельскохозяйственного назначения	8		f	3
20	20	Участок коммерческого назначения	8		f	3
15	15	Участок для строительства дома	8		f	3
\.


--
-- Data for Name: estatebase_estatetypecategory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_estatetypecategory (id, "order", name, independent, has_bidg, has_stead, is_commerce) FROM stdin;
2	1	Дом	t	1	1	f
4	2	Квартира	t	1	0	f
8	4	Участок	t	0	1	f
5	5	Квартира с участком	t	1	1	f
6	6	Коммерческая недвижимость	t	1	2	t
1	7	Гараж	t	1	2	f
7	8	Строения и сооружения	f	1	0	f
\.


--
-- Data for Name: estatebase_exteriorfinish; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_exteriorfinish (id, name) FROM stdin;
1	без отделки
2	дагестанский камень
3	камень
4	керамогранит
5	кирпич
6	короед
7	окрашено
8	оштукатурено
9	плитка
10	сайдинг
\.


--
-- Data for Name: estatebase_flooring; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_flooring (id, name) FROM stdin;
1	без стяжки
2	деревянный
3	ковролин
4	ламинат
5	линолеум
6	паркет
7	стяжка
8	теплый пол
\.


--
-- Data for Name: estatebase_furniture; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_furniture (id, name) FROM stdin;
1	Да
2	Нет
3	Частично
\.


--
-- Data for Name: estatebase_gassupply; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_gassupply (id, name) FROM stdin;
1	На расстоянии
2	По меже
3	Подведено
4	Подключение оплачено
5	Подключено
6	Технические условия
\.


--
-- Data for Name: estatebase_geogroup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_geogroup (id, name) FROM stdin;
1	Анапа
2	Геленджик
3	Новороссийск
4	Темрюкск
\.


--
-- Data for Name: estatebase_heating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_heating (id, name) FROM stdin;
1	индивидуальное газовое
2	индивидуальное твердотоплевное
3	индивидуальное электрическое
4	центральное
\.


--
-- Data for Name: estatebase_historymeta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_historymeta (id, created, created_by_id, updated, updated_by_id, modificated) FROM stdin;
1	2012-10-07 19:32:33.569219+04	1	\N	\N	2012-10-07 19:32:33.569219+04
2	2012-10-07 19:35:08.548041+04	1	\N	\N	2012-10-07 19:35:08.548041+04
3	2012-10-07 20:57:09.948906+04	1	2012-10-07 20:57:10.014533+04	1	2012-10-07 20:57:10.014533+04
4	2012-10-07 20:59:08.372139+04	1	2012-10-07 20:59:08.389168+04	1	2012-10-07 20:59:08.389168+04
5	2012-10-07 21:01:03.371847+04	1	2012-10-07 21:01:03.386385+04	1	2012-10-07 21:01:03.386385+04
6	2012-10-07 21:02:38.466259+04	1	2012-10-07 21:02:38.476865+04	1	2012-10-07 21:02:38.476865+04
7	2012-10-07 21:06:05.788576+04	1	2012-10-07 21:06:05.800138+04	1	2012-10-07 21:06:05.800138+04
8	2012-10-07 21:08:48.915244+04	1	2012-10-07 21:08:48.931619+04	1	2012-10-07 21:08:48.931619+04
9	2012-10-07 21:20:05.007144+04	1	2012-10-07 21:20:05.018801+04	1	2012-10-07 21:20:05.018801+04
10	2012-10-07 21:21:16.419235+04	1	2012-10-07 21:21:33.028916+04	1	2012-10-07 21:21:33.028916+04
11	2012-10-07 21:23:26.809448+04	1	2012-10-07 23:25:49.769066+04	1	2012-10-07 23:25:49.769066+04
13	2012-10-07 23:32:21.364443+04	1	\N	\N	2012-10-07 23:32:21.364443+04
14	2012-10-07 23:37:04.471554+04	1	\N	\N	2012-10-07 23:37:04.471554+04
15	2012-10-07 23:43:04.361479+04	1	\N	\N	2012-10-07 23:43:04.361479+04
16	2012-10-07 23:44:46.194839+04	1	2012-10-08 00:20:03.970946+04	1	2012-10-08 00:20:03.970946+04
18	2012-10-08 00:22:20.814831+04	1	2012-10-08 00:27:30.160215+04	1	2012-10-08 00:27:30.160215+04
17	2012-10-07 23:46:21.179607+04	1	2012-10-08 00:28:25.299947+04	1	2012-10-08 00:28:25.299947+04
19	2012-10-08 00:29:38.984101+04	1	2012-10-08 00:29:54.11587+04	1	2012-10-08 00:29:54.11587+04
20	2012-10-08 22:59:25.272399+04	1	\N	\N	2012-10-08 22:59:25.272399+04
22	2012-10-08 23:49:08.982384+04	1	\N	\N	2012-10-08 23:49:08.982384+04
29	2012-10-12 23:39:36.562941+04	1	2012-10-12 23:39:50.767815+04	1	2012-10-12 23:39:50.767815+04
21	2012-10-08 23:48:30.026407+04	1	2012-10-10 22:10:23.555583+04	1	2012-10-10 22:10:23.555583+04
24	2012-10-10 22:29:19.35623+04	1	2012-10-10 22:38:51.05676+04	1	2012-10-10 22:38:51.05676+04
23	2012-10-09 23:44:46.481064+04	1	2012-10-11 00:12:15.892336+04	1	2012-10-11 00:12:15.892336+04
25	2012-10-11 00:14:51.253269+04	1	\N	\N	2012-10-11 00:14:51.253269+04
30	2012-10-13 11:59:23.644924+04	1	2012-10-13 15:23:25.261206+04	1	2012-10-13 15:23:25.261206+04
12	2012-10-07 23:31:39.686455+04	1	2012-10-13 20:19:36.369687+04	1	2012-10-13 20:19:36.369687+04
31	2012-10-13 14:53:05.555341+04	1	2012-10-13 20:19:36.389573+04	1	2012-10-13 20:19:36.389573+04
27	2012-10-11 21:50:13.185498+04	1	2012-10-13 20:19:36.403645+04	1	2012-10-13 20:19:36.403645+04
26	2012-10-11 21:49:55.947532+04	1	2012-10-13 20:19:36.41696+04	1	2012-10-13 20:19:36.41696+04
33	2012-10-13 20:26:52.300608+04	1	\N	\N	2012-10-13 20:26:52.300608+04
35	2012-10-13 20:40:50.116384+04	1	\N	\N	2012-10-13 20:40:50.116384+04
34	2012-10-13 20:40:40.89727+04	1	2012-10-13 20:45:01.261228+04	1	2012-10-13 20:45:01.261228+04
36	2012-10-13 20:45:12.014641+04	1	\N	\N	2012-10-13 20:45:12.014641+04
28	2012-10-12 21:48:38.612289+04	1	2012-10-16 20:42:26.979898+04	1	2012-10-16 20:42:26.979898+04
38	2012-10-18 12:18:25.069922+04	3	2012-10-18 12:18:28.917355+04	3	2012-10-18 12:18:28.917355+04
58	2012-10-19 14:05:40.43972+04	3	2012-10-19 14:13:59.484021+04	3	2012-10-19 14:13:59.484021+04
37	2012-10-17 00:55:19.087137+04	1	2012-10-18 13:50:24.424059+04	3	2012-10-18 13:50:24.424059+04
46	2012-10-19 10:06:36.768067+04	3	2012-10-19 22:05:28.48294+04	3	2012-10-19 22:05:28.48294+04
40	2012-10-19 09:46:38.074808+04	3	\N	\N	2012-10-19 09:46:38.074808+04
41	2012-10-19 09:48:39.362722+04	3	\N	\N	2012-10-19 09:48:39.362722+04
42	2012-10-19 09:50:04.760042+04	3	\N	\N	2012-10-19 09:50:04.760042+04
45	2012-10-19 09:57:44.341141+04	3	\N	\N	2012-10-19 09:57:44.341141+04
32	2012-10-13 15:20:29.890944+04	1	2012-10-19 14:16:47.100832+04	3	2012-10-19 14:16:47.100832+04
44	2012-10-19 09:51:24.918391+04	3	2012-10-19 10:05:35.625708+04	3	2012-10-19 10:05:35.625708+04
60	2012-10-20 13:38:26.140923+04	3	\N	\N	2012-10-20 13:38:26.140923+04
61	2012-10-20 13:44:04.829215+04	3	\N	\N	2012-10-20 13:44:04.829215+04
43	2012-10-19 09:50:10.826542+04	3	2012-10-20 13:45:06.569085+04	3	2012-10-20 13:45:06.569085+04
62	2012-10-20 13:45:13.551105+04	3	\N	\N	2012-10-20 13:45:13.551105+04
47	2012-10-19 10:14:17.846993+04	3	2012-10-19 10:16:59.447828+04	3	2012-10-19 10:16:59.447828+04
39	2012-10-19 09:30:21.580804+04	3	2012-10-19 10:17:45.894166+04	3	2012-10-19 10:17:45.894166+04
63	2012-10-20 13:46:36.940541+04	3	\N	\N	2012-10-20 13:46:36.940541+04
49	2012-10-19 13:40:45.395591+04	3	\N	\N	2012-10-19 13:40:45.395591+04
52	2012-10-19 13:45:37.147831+04	3	2012-10-19 13:45:41.110311+04	3	2012-10-19 13:45:41.110311+04
51	2012-10-19 13:44:18.268274+04	3	2012-10-19 13:45:52.156387+04	3	2012-10-19 13:45:52.156387+04
54	2012-10-19 13:50:00.940317+04	3	\N	\N	2012-10-19 13:50:00.940317+04
53	2012-10-19 13:48:10.324401+04	3	2012-10-19 13:50:21.601729+04	3	2012-10-19 13:50:21.601729+04
50	2012-10-19 13:41:06.383877+04	3	2012-10-19 13:50:55.687647+04	3	2012-10-19 13:50:55.687647+04
56	2012-10-19 13:59:40.928186+04	3	2012-10-19 13:59:45.464786+04	3	2012-10-19 13:59:45.464786+04
57	2012-10-19 14:01:52.498436+04	3	\N	\N	2012-10-19 14:01:52.498436+04
59	2012-10-19 21:24:40.268723+04	3	2012-10-19 21:24:44.694828+04	3	2012-10-19 21:24:44.694828+04
55	2012-10-19 13:56:11.304678+04	3	2012-10-20 14:28:41.680375+04	3	2012-10-20 14:28:41.680375+04
48	2012-10-19 13:30:56.929175+04	3	2012-10-19 21:40:20.432536+04	3	2012-10-19 21:40:20.432536+04
\.


--
-- Data for Name: estatebase_interior; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_interior (id, name) FROM stdin;
1	без отделки
2	ветхое
3	евроремонт
4	жилое
5	капитальный ремонт
6	косметический ремонт
7	отличное
8	предчистовая отделка
9	ремонт
10	удовлетворительное
11	хорошее
\.


--
-- Data for Name: estatebase_internet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_internet (id, name) FROM stdin;
1	Есть возможность
2	Нет
3	Подключено
\.


--
-- Data for Name: estatebase_landtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_landtype (id, name) FROM stdin;
1	Населенных пунктов
2	Особо охраняемых территорий
3	Промышленности
4	Сельскохозяйственного назначения
\.


--
-- Data for Name: estatebase_layout; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_layout (id, level_id, layout_type_id, area, furniture_id, layout_feature_id, note, interior_id) FROM stdin;
7	5	3	12.00	3	2		2
6	4	5	8.00	1	2		3
5	4	6	77.00	\N	\N		\N
4	4	14	12.00	\N	\N		\N
8	6	3	12.00	1	\N		\N
9	7	3	12.00	1	1	44	4
10	8	5	23.00	2	1	333	3
12	9	7	20.00	1	4		7
11	9	14	10.00	1	4		7
13	9	23	10.00	1	1		7
14	10	1	\N	\N	\N		\N
17	11	7	\N	\N	1		\N
16	11	11	\N	\N	1		\N
15	11	14	10.00	3	1		4
18	11	21	\N	\N	5		\N
19	11	23	\N	\N	1		\N
25	14	6	\N	\N	\N		\N
23	13	2	20.00	1	1		\N
24	13	5	30.00	2	\N		1
26	15	7	\N	\N	\N		\N
27	16	2	20.00	1	4	жилая	3
28	16	4	14.00	1	1	сантехника	7
\.


--
-- Data for Name: estatebase_layoutfeature; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_layoutfeature (id, name) FROM stdin;
1	Изолированная
2	Остекление
3	Раздельный
4	Смежная
5	Совмещенный
\.


--
-- Data for Name: estatebase_layouttype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_layouttype (id, name) FROM stdin;
1	Балкон
2	Баня
3	Бойлерная
4	Ванная комната
5	Гараж
6	Гардеробная
7	Гостиная
8	Зимний сад
9	Кабинет
10	Кладовая
11	Комната
12	Комната отдыха
13	Коридор
14	Кухня
15	Лоджия
16	Номер
17	Подвал
18	Помещение
19	Постирочная
20	Прихожая
21	Санузел
22	Сауна
23	Спальная комната
24	Спортзал
25	Терраса
26	Хозяйственная комната
27	Холл
\.


--
-- Data for Name: estatebase_level; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_level (id, level_name_id, bidg_id) FROM stdin;
5	6	27
4	1	29
6	1	37
7	2	29
8	1	28
9	1	45
10	1	46
11	1	50
14	2	48
13	1	48
15	2	46
16	1	56
\.


--
-- Data for Name: estatebase_levelname; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_levelname (id, name) FROM stdin;
1	1-й
2	2-й
3	3-й
4	4-й
5	5-й
6	Мансарда
7	Подвал
8	Цокольный
\.


--
-- Data for Name: estatebase_locality; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_locality (id, name, region_id) FROM stdin;
1	Абрау-Дюрсо	3
2	Адербиевка	2
3	Анапа	1
4	Анапская	1
5	Артющенко	4
7	Афонка	2
6	Архипо-Осиповка	2
8	Ахтанизовская	4
9	Батарейка	4
10	Белый	4
11	Береговое	2
12	Береговой	4
13	Бетта	2
14	Благовещенская	1
15	Большие Хутора	3
16	Борисовка	3
17	Бужор	1
18	Варваровка	1
19	Васильевка	3
20	Верхнебаканский	3
21	Верхнее Джемете	1
22	Верхний Ханчакрак	1
23	Верхний Чекон	1
24	Веселая горка	1
25	Веселовка (Янтарь)	4
26	Вестник	1
27	Виноградное	2
28	Виноградный	1
29	Виноградный	4
30	Витязево	1
31	Владимировка	3
32	Возрождение	2
33	Волна Революции	4
34	Волна	4
35	Воскресенский	1
36	Вышестеблиевская	4
37	Гайдук	3
38	Гайкодзор	1
39	Гаркуша	4
40	Геленджик	2
41	Глебовское	3
42	Голубицкая	4
43	Горный	3
44	Гостагаевская	1
45	Джанхот	2
46	Джемете	1
47	Джигинка	1
48	Дивноморское	2
49	Дюрсо	3
50	За Родину	4
51	Запорожская	4
52	Заря	1
53	Иваново	1
54	Ильич	4
55	Кабардинка	2
56	Капустино	1
57	Киблерово	1
58	Кирилловка	3
59	Красная Горка	1
60	Красная Скала	1
61	Красноармейский	4
62	Красный Курган	1
63	Красный Октябрь	4
64	Красный	1
65	Криница	2
66	Куматырь	1
67	Курбацкий	1
68	Курчанская	4
69	Кучугуры	4
70	Ленинский Путь	3
71	Лесничество Абрау-Дюрсо	3
72	Лиманный	1
73	Малый Разнокол	1
74	Малый Чекон	1
75	Марьина Роща	2
76	Михайловский Перевал	2
77	Мысхако	3
78	Натухаевская	3
79	Нижняя Гостагайка	1
80	Новороссийск	3
81	Павловка	1
82	Пересыпь	4
83	Песчаный	1
84	Победа	3
85	Прасковеевка	2
86	Приазовский	4
87	Приморский	4
88	Прогресс	4
89	Просторный	1
90	Пшада	2
91	Пятихатки	1
92	Раевская	3
93	Разнокол	1
94	Рассвет	1
95	Светлый Путь	4
96	Светлый	2
97	Северная Озереевка	3
98	Семигорский	3
99	Сенной	4
100	Соленый	4
101	Старотитаровская	4
102	Стрелка	4
103	Суворово-Черкесский	1
104	Сукко	1
105	Супсех	1
106	Таманский	4
107	Тамань	4
108	Тарусино	1
109	Текос	2
110	Темрюк	4
111	Тешебс	2
112	Убых	3
113	Усатова Балка	1
114	Уташ	1
115	Утриш	1
116	Фадеево	1
117	Федотовка	3
118	Фонталовская	4
119	Цемдолина	3
120	Цыбанобалка	1
121	Чекон	1
122	Чембурка	1
123	Черный	1
124	Широкая Балка	3
125	Широкая Пшадская Щель	2
126	Широкая Щель	2
127	Юбилейный	4
128	Южная Озереевка	3
129	Юровка	1
\.


--
-- Data for Name: estatebase_microdistrict; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_microdistrict (id, name, locality_id) FROM stdin;
\.


--
-- Data for Name: estatebase_office; Type: TABLE DATA; Schema: public; Owner: realty
--

COPY estatebase_office (id, name, address) FROM stdin;
\.


--
-- Data for Name: estatebase_office_regions; Type: TABLE DATA; Schema: public; Owner: realty
--

COPY estatebase_office_regions (id, office_id, region_id) FROM stdin;
\.


--
-- Data for Name: estatebase_origin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_origin (id, name) FROM stdin;
1	avito
2	irr
3	krasnodar.life-realty
4	olx
5	rosrealt
6	slando
7	ваша удача
8	все для вас
9	из рук в руки
10	интернет
11	орбита
12	прямое обращение
13	с легкой руки
14	сайт
\.


--
-- Data for Name: estatebase_purpose; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_purpose (id, name) FROM stdin;
1	Для коммерческого использования
2	Для личного подсобного хозяйства
3	Для садоводства и огородничества
4	Для строительства жилого дома
5	Сельхозпроизводства
\.


--
-- Data for Name: estatebase_region; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_region (id, name, geo_group_id) FROM stdin;
1	Анапский	1
2	Геленджикский	2
3	Новороссийский	3
4	Темрюкский	4
\.


--
-- Data for Name: estatebase_roof; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_roof (id, name) FROM stdin;
1	металлопрофиль
2	металлочерепица
3	мягкая кровля
4	ондулин
5	оцинкованная сталь
6	черепица
7	шифер
\.


--
-- Data for Name: estatebase_sewerage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_sewerage (id, name) FROM stdin;
1	На расстоянии
2	По меже
3	Подведено
4	Подключение оплачено
5	Подключено
6	Технические условия
\.


--
-- Data for Name: estatebase_shape; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_shape (id, name) FROM stdin;
1	Г-образный
2	Квадратный
3	Многогранный
4	Прямоугольный
5	Трапециевидный
6	Треугольный
\.


--
-- Data for Name: estatebase_stead; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_stead (id, estate_id, total_area, face_area, shape_id, land_type_id, purpose_id, estate_type_id) FROM stdin;
7	25	100.00	100.00	1	1	2	15
9	26	122.00	111.00	1	\N	\N	15
10	27	\N	\N	\N	\N	\N	14
11	28	\N	\N	\N	\N	\N	15
12	29	\N	\N	\N	\N	\N	15
13	32	\N	\N	\N	\N	\N	15
14	33	8.00	20.00	2	1	4	15
16	35	3400.00	\N	2	\N	\N	15
15	34	\N	\N	2	\N	\N	15
17	36	\N	\N	\N	\N	\N	15
18	37	\N	\N	\N	\N	\N	15
19	38	\N	\N	\N	\N	\N	15
20	39	300.00	10.00	4	1	\N	15
21	30	10000.00	100.00	4	\N	\N	20
\.


--
-- Data for Name: estatebase_stead_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_stead_documents (id, stead_id, document_id) FROM stdin;
8	7	6
9	9	8
10	9	6
11	14	8
12	14	6
13	14	7
14	20	8
15	20	6
16	20	7
17	21	8
18	21	6
19	21	7
\.


--
-- Data for Name: estatebase_street; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_street (id, name, locality_id) FROM stdin;
\.


--
-- Data for Name: estatebase_telephony; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_telephony (id, name) FROM stdin;
1	Есть возможность
2	Нет
3	Подключено
\.


--
-- Data for Name: estatebase_userprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_userprofile (id, user_id, office_id) FROM stdin;
1	1	\N
2	3	\N
\.


--
-- Data for Name: estatebase_userprofile_geo_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_userprofile_geo_groups (id, userprofile_id, geogroup_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	2	1
6	2	2
7	2	3
8	2	4
\.


--
-- Data for Name: estatebase_wallconstrucion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_wallconstrucion (id, name) FROM stdin;
1	блок
2	газоблок
3	дерево
4	камень
5	каркас
6	кирпич
7	монолит
8	панель
9	саман
10	шлакоблок
\.


--
-- Data for Name: estatebase_wallfinish; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_wallfinish (id, name) FROM stdin;
1	без отделки
2	гипсокартон
3	дерево
4	деревянная вагонка
5	обои
6	окрашены
7	оштукатурены
8	пластик
9	побелены
\.


--
-- Data for Name: estatebase_watersupply; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_watersupply (id, name) FROM stdin;
1	Водопровод
2	Колодец
3	На расстоянии
4	По меже
5	Подведено
6	Подключение оплачено
7	Подключено
8	Скважина
9	Технические условия
\.


--
-- Data for Name: estatebase_windowtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_windowtype (id, name) FROM stdin;
1	алюминиевые
2	деревянные
3	евродерево
4	металлопластиковые
5	не остеклено
\.


--
-- Data for Name: sitetree_tree; Type: TABLE DATA; Schema: public; Owner: realty
--

COPY sitetree_tree (id, alias, title) FROM stdin;
1	maintree	Главное древо
\.


--
-- Data for Name: sitetree_treeitem; Type: TABLE DATA; Schema: public; Owner: realty
--

COPY sitetree_treeitem (id, title, hint, url, urlaspattern, tree_id, hidden, alias, description, inmenu, inbreadcrumbs, insitetree, parent_id, sort_order, access_restricted, access_perm_type, access_loggedin) FROM stdin;
1	Лоты		estate-list	t	1	f	\N		t	t	t	\N	1	f	1	f
2	Заказчики		client-list	t	1	f	\N		t	t	t	\N	2	f	1	f
3	Заявки		bid-list	t	1	f	\N		t	t	t	\N	3	f	1	f
4	Подборки		register-list	t	1	f	\N		t	t	t	\N	4	f	1	f
\.


--
-- Data for Name: sitetree_treeitem_access_permissions; Type: TABLE DATA; Schema: public; Owner: realty
--

COPY sitetree_treeitem_access_permissions (id, treeitem_id, permission_id) FROM stdin;
\.


--
-- Data for Name: south_migrationhistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
109	estatebase	0001_initial	2012-10-06 23:17:54.900177+04
110	estatebase	0002_auto__add_field_estate_broker	2012-10-06 23:17:55.038594+04
111	estatebase	0003_auto__del_field_estatetype_object_type__del_field_estatetype_template_	2012-10-06 23:17:55.381699+04
112	estatebase	0004_auto__add_field_estatetype_template	2012-10-06 23:17:55.584532+04
113	estatebase	0005_auto__add_field_estatetype_independent	2012-10-06 23:17:55.809257+04
114	estatebase	0006_auto__add_field_estatetypecategory_independent__del_field_estatetype_i	2012-10-06 23:17:55.998452+04
115	estatebase	0007_auto__del_field_estate_estate_type__add_field_estate_estate_category	2012-10-07 15:48:34.340645+04
116	estatebase	0008_auto__add_field_stead_estate_type__chg_field_estate_estate_category	2012-10-07 17:38:53.70012+04
117	estatebase	0009_auto__add_field_estate_com_status	2012-10-08 22:55:14.926288+04
118	estatebase	0010_auto__add_field_estatetypecategory_has_bidg__add_field_estatetypecateg	2012-10-11 21:47:47.548266+04
119	estatebase	0011_auto	2012-10-11 22:16:20.991431+04
120	estatebase	0012_auto	2012-10-11 22:20:17.57373+04
121	estatebase	0013_auto__add_field_layout_interior	2012-10-11 23:23:48.400054+04
122	estatebase	0014_auto__add_comstatus__del_field_estate_com_status	2012-10-13 15:01:56.79866+04
123	estatebase	0015_auto__add_field_estate_com_status	2012-10-13 15:02:16.830363+04
124	estatebase	0016_auto__add_field_comstatus_status	2012-10-13 15:08:52.223309+04
125	sitetree	0001_initial	2012-10-14 01:04:36.233723+04
126	sitetree	0002_auto__add_field_treeitem_access_restricted__add_field_treeitem_access_	2012-10-14 01:04:38.119207+04
127	sitetree	0003_auto__add_field_treeitem_access_loggedin	2012-10-14 01:04:39.072585+04
128	sitetree	0004_auto__add_field_tree_title	2012-10-14 01:04:39.243189+04
129	thumbnail	0001_initial	2012-10-14 11:31:32.66269+04
130	estatebase	0017_auto__add_office__add_field_userprofile_office	2012-10-16 22:12:48.302055+04
131	estatebase	0018_auto__chg_field_office_address	2012-10-16 22:12:48.535084+04
132	estatebase	0019_auto__del_field_office_region	2012-10-16 22:12:48.952221+04
\.


--
-- Data for Name: thumbnail_kvstore; Type: TABLE DATA; Schema: public; Owner: realty
--

COPY thumbnail_kvstore (key, value) FROM stdin;
sorl-thumbnail||image||ded94409faacc581f80def94087a3020	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/24/hubble-space-wallpaper-1920x1200-1010166.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||ff3f2a6da3bcdbe47bfebf53d2aec16a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/d0/6f/d06fa994fd82dd36d26f1f2d657d6e42.jpg", "size": [110, 80]}
sorl-thumbnail||thumbnails||aabe6dd38413c400d94e9dfe48442b7f	["6197501c21289b325662bb0b15a86ddc", "bbc46e88bf02e2c0b60cec2843c77a85", "f76e167b73322fc630682c42fc691044"]
sorl-thumbnail||image||18800f076a72a25b01f9c74e2acfd416	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/29/f2601-M31.JPG", "size": [2556, 1620]}
sorl-thumbnail||image||3805e6c7b26753458ea7a4c928d5590e	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/cf/ea/cfea47bd926a7e8e8e88003af72cdc6e.jpg", "size": [110, 80]}
sorl-thumbnail||thumbnails||ac32996a8c981936e93a7db369720915	["56fc3ab9c24d7fa999e859c4d2c1ac59", "befbb24a4b1c932db84a96a60157f0b0", "24f6f9edc66537835b1561b6744adcfc"]
sorl-thumbnail||image||fdeb3fbebf69c9d165330c8d816a7a8c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/28/milky_way_galaxy_1920x1200.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||1823238998cd69bd357a6ab1c7df091b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/2d/84/2d84835eada836a7efeeda7322053370.jpg", "size": [110, 80]}
sorl-thumbnail||image||3e09f0814fc1cc91560fa59a822c3b5a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/25/blue_stars_1_1920x1200.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||aabe6dd38413c400d94e9dfe48442b7f	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/27/blue_stars_1_1920x1200.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||6197501c21289b325662bb0b15a86ddc	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/02/ce/02ce21c813532f2de213a3cb4a1156f8.jpg", "size": [110, 80]}
sorl-thumbnail||image||051bd54cf1a89886d1b94cded4c3c874	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/3d/c8/3dc81fec78c4a04e1b06888ee63810d1.jpg", "size": [800, 600]}
sorl-thumbnail||image||bbc46e88bf02e2c0b60cec2843c77a85	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/ac/d1/acd1a3cdb1bfa3e85a587e3a90d1dd32.jpg", "size": [800, 600]}
sorl-thumbnail||image||975eeff70683fe74810eed4beee3419c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/26/hubble-space-wallpaper-1920x1200-1010166.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||98d061619a53d9837681e0bef61bdc51	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e0/69/e0699ee51d5180b53e886e6ea05b375f.jpg", "size": [110, 80]}
sorl-thumbnail||thumbnails||18800f076a72a25b01f9c74e2acfd416	["3805e6c7b26753458ea7a4c928d5590e", "810ee5e45e20b47f74fbc82741ae025e", "f9764316479f3d06662877134f51c253"]
sorl-thumbnail||image||8c7e87ecfca92d48f1b8e66e4d849254	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/1d/f5/1df5a8005d21cae2f003fd7e75733dc8.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||676e2c2983fab11425e2a8b9f2dd5335	["39121db2bab43671bf1303fc8ede6910", "fcafd2ec31e0994022444d60b9eea49b", "4f2a2593d0adda6ce9752aa094162268"]
sorl-thumbnail||image||676e2c2983fab11425e2a8b9f2dd5335	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/26/milky_way_galaxy_1920x1200.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||fcafd2ec31e0994022444d60b9eea49b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e2/87/e287d34b34612416e2221fe7a7de44b7.jpg", "size": [110, 80]}
sorl-thumbnail||image||4f2a2593d0adda6ce9752aa094162268	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e0/af/e0af453e209f8d6183356cb7dcb4d830.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||9cfb8508d7850fab4c5c77286a0632dc	["051bd54cf1a89886d1b94cded4c3c874", "cb707831173a06d75c421b623a49d367", "0e0e2f1c6662a5a2be55ec78cbd3dc57"]
sorl-thumbnail||image||9cfb8508d7850fab4c5c77286a0632dc	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/26/blue_stars_1_1920x1200.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||0e0e2f1c6662a5a2be55ec78cbd3dc57	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/52/91/5291b3985d6a875f965cfa82c2ceb591.jpg", "size": [110, 80]}
sorl-thumbnail||image||ac32996a8c981936e93a7db369720915	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/30/hubble-space-wallpaper-1920x1200-1010166.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||24f6f9edc66537835b1561b6744adcfc	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/74/0a/740a1c115f08e429830c30eff8b2fb7b.jpg", "size": [110, 80]}
sorl-thumbnail||image||cf2b6dd23676f0788d766d3ab4956b4d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/11/a6/11a61d5b79c1d772d41ec528331a308e.jpg", "size": [110, 80]}
sorl-thumbnail||image||befbb24a4b1c932db84a96a60157f0b0	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/28/0f/280f0d6b39968b78584c3b226aa12606.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||ded94409faacc581f80def94087a3020	["cf18b051e27052db1390592651baafee", "ff3f2a6da3bcdbe47bfebf53d2aec16a", "2c5b1f6289ee069aadeb93dc4d1a98b2"]
sorl-thumbnail||image||6f0d226c1413f8b3b3a440080f0ccc4a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/4d/71/4d7100915fc148726bffdd1703306efe.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||975eeff70683fe74810eed4beee3419c	["8c7e87ecfca92d48f1b8e66e4d849254", "84151f95132fc5fbdf2ecc29336214eb", "98d061619a53d9837681e0bef61bdc51"]
sorl-thumbnail||image||64b903c9cbb3c4fe131dcfa88de08d97	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/25/f2601-M31.JPG", "size": [2556, 1620]}
sorl-thumbnail||image||c3b1afd9d7f347ac885fa0e76e4dde33	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/c1/87/c18750330ac20d34a04bd10e87d14bf3.jpg", "size": [800, 600]}
sorl-thumbnail||image||64f0cf52c83f61aa88b830efb4b1fddb	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/2c/d5/2cd5b86e0729f3ad77536a7acd958648.jpg", "size": [110, 80]}
sorl-thumbnail||image||c7f125d6930900be4cc3e3be1dc87473	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e9/6f/e96f1eb905be8a5f787d145c71152c4a.jpg", "size": [800, 600]}
sorl-thumbnail||image||d00629409bff6694e1887c491dd1a99e	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/25/hubble-space-wallpaper-1920x1200-1010166.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||ed0780b771274a5b54dc810e2998767c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/8e/66/8e669809ecee8dc766ba3e0dd1420af9.jpg", "size": [110, 80]}
sorl-thumbnail||thumbnails||17c45fd8bd78325b4dae25d23648029d	["8fac4d855ed81d565a6565992fb34532", "4959e4c911e2f50c1665f4469fc54b0d", "da03c4634d04ea702f0510ffd50aea82"]
sorl-thumbnail||image||0871f3b197b5630d3dda90b2d7b6da0d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/0e/53/0e53fdbd9e7867a2c2fcc88d1700c053.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||7088519fc702daa2cfa82042725e0ff4	["3a5b7cdd64c690d6b3ba53b805f3d007", "035bfb15223d061182021ed8cb373221", "ea4d480bb7ef99ee1e88eab59048e389"]
sorl-thumbnail||image||7088519fc702daa2cfa82042725e0ff4	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/25/hubble_space_telescope_crab_bebula.jpg", "size": [1600, 1200]}
sorl-thumbnail||image||3a5b7cdd64c690d6b3ba53b805f3d007	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/1c/f6/1cf6f08a1c3f8f40f5882a27b72eb635.jpg", "size": [110, 80]}
sorl-thumbnail||image||035bfb15223d061182021ed8cb373221	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/51/29/51293ad00986989cacc20ccc231827e8.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||b505fc7df0e9c4587dbd559d17629831	["16755c28fcd09c9c948ea7da26d706e6", "da68599aba3927c4431a0600fad6bad7", "ac637980d77a827a45deb4b246b70675"]
sorl-thumbnail||image||5b7d76cda99edf8494de6104344ace64	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/25/milky_way_galaxy_1920x1200.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||685446a99910c4c5f5c78dd8d5b03e80	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/ca/d4/cad4e3965932fb5960fd491b7b22743b.jpg", "size": [110, 80]}
sorl-thumbnail||image||17c45fd8bd78325b4dae25d23648029d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/29/milky_way_galaxy_1920x1200.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||402520d6adb03c7e7e0237fa82f92621	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/81/28/8128e813acc92a6d58bac56479280cc6.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||02e6293d75851e7e26a18f33bb3cfe7b	["74461c5a925fc223484f6a699a787160", "13dd62ce9c24be7bd1151d2d09f0abee", "665498f5ef74ffbeefb9268abfb25c77"]
sorl-thumbnail||image||b505fc7df0e9c4587dbd559d17629831	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/25/space_galactic_super_winds_1600x1200.jpg", "size": [1600, 1200]}
sorl-thumbnail||image||16755c28fcd09c9c948ea7da26d706e6	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/ed/07/ed07016d6bee576a48dbf0924a1696aa.jpg", "size": [110, 80]}
sorl-thumbnail||image||da68599aba3927c4431a0600fad6bad7	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/69/08/69086b1b31ec799e436b8f205b0d6e70.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||036e06c42def6daae0ae9bdda50a3acc	["aa93dd277487aea97f54f2de4bcc9529", "723a97b8d599c2fe902abea03d7db284", "cddc15d7a33f2c3248d18fbf471dfda3"]
sorl-thumbnail||image||cf18b051e27052db1390592651baafee	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/0e/6e/0e6e9d07da26e5367215a70db7676a6e.jpg", "size": [800, 600]}
sorl-thumbnail||image||f9764316479f3d06662877134f51c253	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/34/83/348310b6c56286272b5941a317fb5afe.jpg", "size": [800, 600]}
sorl-thumbnail||image||02e6293d75851e7e26a18f33bb3cfe7b	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/29/hubble-space-wallpaper-1920x1200-1010166.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||74461c5a925fc223484f6a699a787160	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/75/94/7594d0dfcbbdbcade4c448833a53e2b9.jpg", "size": [110, 80]}
sorl-thumbnail||image||cddc15d7a33f2c3248d18fbf471dfda3	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/fc/06/fc067833e8786b85d6aaf38cbbf25551.jpg", "size": [800, 600]}
sorl-thumbnail||image||665498f5ef74ffbeefb9268abfb25c77	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/d9/ea/d9eae8a2f3847c8dbefd1044069c8b40.jpg", "size": [800, 600]}
sorl-thumbnail||image||8fac4d855ed81d565a6565992fb34532	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/89/06/8906d267d01bc40864ce7c97c47646a5.jpg", "size": [110, 80]}
sorl-thumbnail||image||4959e4c911e2f50c1665f4469fc54b0d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/72/ce/72cecadd5d085d95d4ae37f3f583f2a0.jpg", "size": [800, 600]}
sorl-thumbnail||image||036e06c42def6daae0ae9bdda50a3acc	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/29/space_galactic_super_winds_1600x1200.jpg", "size": [1600, 1200]}
sorl-thumbnail||image||723a97b8d599c2fe902abea03d7db284	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/46/4b/464bd1b633f3991e34f513dcbf4111c6.jpg", "size": [110, 80]}
sorl-thumbnail||thumbnails||fdeb3fbebf69c9d165330c8d816a7a8c	["6f0d226c1413f8b3b3a440080f0ccc4a", "1823238998cd69bd357a6ab1c7df091b", "eeb124af2020637f2a81a0516bc9b181"]
sorl-thumbnail||image||56fc3ab9c24d7fa999e859c4d2c1ac59	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/e5/a0/e5a0e9bd048b735d2e8f3bc36a7a4871.jpg", "size": [800, 600]}
sorl-thumbnail||image||eeb124af2020637f2a81a0516bc9b181	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/74/ae/74ae8763abe2ce6a7b56b7f2c4badda2.jpg", "size": [800, 600]}
sorl-thumbnail||image||2c5b1f6289ee069aadeb93dc4d1a98b2	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/f6/1d/f61dbe57ec7f170b68e70f167b1e63d8.jpg", "size": [800, 600]}
sorl-thumbnail||image||84151f95132fc5fbdf2ecc29336214eb	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/6d/d8/6dd87bef013288f5f951b0bcbf5c4c64.jpg", "size": [800, 600]}
sorl-thumbnail||image||39121db2bab43671bf1303fc8ede6910	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/09/f3/09f38aab94d496a3a9989a9f1ac40cd1.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||d00629409bff6694e1887c491dd1a99e	["9c1f64908c352301c4c442160e59d617", "ed0780b771274a5b54dc810e2998767c", "0871f3b197b5630d3dda90b2d7b6da0d"]
sorl-thumbnail||image||cb707831173a06d75c421b623a49d367	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/19/34/19345378318abc985a562cbd8c7269ee.jpg", "size": [800, 600]}
sorl-thumbnail||image||0018ca5a3857a35a9f094b159d5e8ac7	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/5c/8c/5c8c6bd61d34716ad4f70a1b2f0f5340.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||3e09f0814fc1cc91560fa59a822c3b5a	["0018ca5a3857a35a9f094b159d5e8ac7", "cf2b6dd23676f0788d766d3ab4956b4d", "c3b1afd9d7f347ac885fa0e76e4dde33"]
sorl-thumbnail||image||c16b8027380a7dffa8c512c60be27eb2	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/57/8b/578b9936135483d139605320cf843ba0.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||64b903c9cbb3c4fe131dcfa88de08d97	["c16b8027380a7dffa8c512c60be27eb2", "c7f125d6930900be4cc3e3be1dc87473", "64f0cf52c83f61aa88b830efb4b1fddb"]
sorl-thumbnail||image||9c1f64908c352301c4c442160e59d617	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/5b/ae/5baeaa7ffa0a37021379a6ed52ff26fe.jpg", "size": [800, 600]}
sorl-thumbnail||image||ea4d480bb7ef99ee1e88eab59048e389	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/7a/33/7a33d12295247f9bb05542a684709005.jpg", "size": [800, 600]}
sorl-thumbnail||image||caae1d6ceaa408597287dfa618cf6689	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/49/e2/49e201f2986e1e225413fc51d6e52542.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||5b7d76cda99edf8494de6104344ace64	["402520d6adb03c7e7e0237fa82f92621", "685446a99910c4c5f5c78dd8d5b03e80", "caae1d6ceaa408597287dfa618cf6689"]
sorl-thumbnail||image||ac637980d77a827a45deb4b246b70675	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/c0/a3/c0a3827b0cda04073b201fdc52dbde9b.jpg", "size": [800, 600]}
sorl-thumbnail||image||810ee5e45e20b47f74fbc82741ae025e	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/9b/75/9b7549de48582d7b468d8f2c9482de39.jpg", "size": [800, 600]}
sorl-thumbnail||image||13dd62ce9c24be7bd1151d2d09f0abee	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/82/ba/82ba7d8359fc85a846473b69e8386982.jpg", "size": [800, 600]}
sorl-thumbnail||image||da03c4634d04ea702f0510ffd50aea82	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/be/96/be96ea7e03b6a9dd9819fa649dc2719e.jpg", "size": [800, 600]}
sorl-thumbnail||image||aa93dd277487aea97f54f2de4bcc9529	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/28/92/2892ae12d01a1e3f889e31ad9d5a1401.jpg", "size": [800, 600]}
sorl-thumbnail||image||f76e167b73322fc630682c42fc691044	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/a0/65/a0653f729ae4bd28f63885c15b413137.jpg", "size": [800, 600]}
sorl-thumbnail||image||ae2f89cc66cdb382bc5a6e171144ab70	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/27/hubble-space-wallpaper-1920x1200-1010166.jpg", "size": [1920, 1200]}
sorl-thumbnail||image||99e705e7bbc868febce0e2a3a002186c	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/ac/fb/acfb195a1dcec18abfbe32873accb881.jpg", "size": [110, 80]}
sorl-thumbnail||image||5f1e430f0515d5b8e5634f3673527fda	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/61/4e/614ec2ab5a86ec1b81e6ff9787fcdecc.jpg", "size": [110, 80]}
sorl-thumbnail||image||9490d4d029357996e69692d3e3402035	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/19/37/19376d15eca8235009d9ca9ca2eaffe7.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||ae2f89cc66cdb382bc5a6e171144ab70	["9490d4d029357996e69692d3e3402035", "99e705e7bbc868febce0e2a3a002186c"]
sorl-thumbnail||image||e5c44a8cae036ec80c0f180801396020	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/30/DSC06437.JPG", "size": [640, 480]}
sorl-thumbnail||image||48a2758fdcc64422bba79998d299b874	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/33/d9/33d9a9b1b0881b159f72a0e8d9a5077c.jpg", "size": [110, 80]}
sorl-thumbnail||image||709b88390cf5f3adece1d9e4a370d07a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/83/75/8375fa4a9cd16cfbd77596996b2a1322.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||e5c44a8cae036ec80c0f180801396020	["48a2758fdcc64422bba79998d299b874", "709b88390cf5f3adece1d9e4a370d07a"]
sorl-thumbnail||image||093abf88e3955c5a74b984efe68facc8	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/30/DSC06439.JPG", "size": [640, 480]}
sorl-thumbnail||thumbnails||1ecce9d94c3027da2fa989000df6a67a	["e2d1a95b3d6e30b5091b7c2ac2fe4c61", "a1b4490343aa6894c4bc8c897cc93e7d"]
sorl-thumbnail||image||26af7456ec0fa0de858e6e8c98369122	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/a7/e5/a7e5d8e8572c0a824b6867f3cd6ec066.jpg", "size": [800, 600]}
sorl-thumbnail||thumbnails||093abf88e3955c5a74b984efe68facc8	["26af7456ec0fa0de858e6e8c98369122", "5f1e430f0515d5b8e5634f3673527fda"]
sorl-thumbnail||image||1ecce9d94c3027da2fa989000df6a67a	{"storage": "django.core.files.storage.FileSystemStorage", "name": "photos/30/DSC06441.JPG", "size": [640, 480]}
sorl-thumbnail||image||e2d1a95b3d6e30b5091b7c2ac2fe4c61	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/27/6e/276e68e9c7a030eda33039d4ad258356.jpg", "size": [110, 80]}
sorl-thumbnail||image||a1b4490343aa6894c4bc8c897cc93e7d	{"storage": "django.core.files.storage.FileSystemStorage", "name": "cache/2e/a6/2ea6dc82d63f0e2a317278a2dd5eb33c.jpg", "size": [800, 600]}
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_model_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: estatebase_beside_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_beside
    ADD CONSTRAINT estatebase_beside_name_key UNIQUE (name);


--
-- Name: estatebase_beside_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_beside
    ADD CONSTRAINT estatebase_beside_pkey PRIMARY KEY (id);


--
-- Name: estatebase_bid_estate_types_bid_id_79ac0541_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid_estate_types
    ADD CONSTRAINT estatebase_bid_estate_types_bid_id_79ac0541_uniq UNIQUE (bid_id, estatetype_id);


--
-- Name: estatebase_bid_estate_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid_estate_types
    ADD CONSTRAINT estatebase_bid_estate_types_pkey PRIMARY KEY (id);


--
-- Name: estatebase_bid_estates_bid_id_31aaf80d_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid_estates
    ADD CONSTRAINT estatebase_bid_estates_bid_id_31aaf80d_uniq UNIQUE (bid_id, estate_id);


--
-- Name: estatebase_bid_estates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid_estates
    ADD CONSTRAINT estatebase_bid_estates_pkey PRIMARY KEY (id);


--
-- Name: estatebase_bid_history_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid
    ADD CONSTRAINT estatebase_bid_history_id_key UNIQUE (history_id);


--
-- Name: estatebase_bid_localities_bid_id_774bd6ff_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid_localities
    ADD CONSTRAINT estatebase_bid_localities_bid_id_774bd6ff_uniq UNIQUE (bid_id, locality_id);


--
-- Name: estatebase_bid_localities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid_localities
    ADD CONSTRAINT estatebase_bid_localities_pkey PRIMARY KEY (id);


--
-- Name: estatebase_bid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid
    ADD CONSTRAINT estatebase_bid_pkey PRIMARY KEY (id);


--
-- Name: estatebase_bid_regions_bid_id_29579179_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid_regions
    ADD CONSTRAINT estatebase_bid_regions_bid_id_29579179_uniq UNIQUE (bid_id, region_id);


--
-- Name: estatebase_bid_regions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bid_regions
    ADD CONSTRAINT estatebase_bid_regions_pkey PRIMARY KEY (id);


--
-- Name: estatebase_bidg_documents_bidg_id_34a07477_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bidg_documents
    ADD CONSTRAINT estatebase_bidg_documents_bidg_id_34a07477_uniq UNIQUE (bidg_id, document_id);


--
-- Name: estatebase_bidg_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bidg_documents
    ADD CONSTRAINT estatebase_bidg_documents_pkey PRIMARY KEY (id);


--
-- Name: estatebase_bidg_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT estatebase_bidg_pkey PRIMARY KEY (id);


--
-- Name: estatebase_ceiling_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_ceiling
    ADD CONSTRAINT estatebase_ceiling_name_key UNIQUE (name);


--
-- Name: estatebase_ceiling_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_ceiling
    ADD CONSTRAINT estatebase_ceiling_pkey PRIMARY KEY (id);


--
-- Name: estatebase_client_history_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_client
    ADD CONSTRAINT estatebase_client_history_id_key UNIQUE (history_id);


--
-- Name: estatebase_client_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_client
    ADD CONSTRAINT estatebase_client_pkey PRIMARY KEY (id);


--
-- Name: estatebase_clienttype_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_clienttype
    ADD CONSTRAINT estatebase_clienttype_name_key UNIQUE (name);


--
-- Name: estatebase_clienttype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_clienttype
    ADD CONSTRAINT estatebase_clienttype_pkey PRIMARY KEY (id);


--
-- Name: estatebase_comstatus_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_comstatus
    ADD CONSTRAINT estatebase_comstatus_name_key UNIQUE (name);


--
-- Name: estatebase_comstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_comstatus
    ADD CONSTRAINT estatebase_comstatus_pkey PRIMARY KEY (id);


--
-- Name: estatebase_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_contact
    ADD CONSTRAINT estatebase_contact_pkey PRIMARY KEY (id);


--
-- Name: estatebase_contacthistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_contacthistory
    ADD CONSTRAINT estatebase_contacthistory_pkey PRIMARY KEY (id);


--
-- Name: estatebase_contactstate_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_contactstate
    ADD CONSTRAINT estatebase_contactstate_name_key UNIQUE (name);


--
-- Name: estatebase_contactstate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_contactstate
    ADD CONSTRAINT estatebase_contactstate_pkey PRIMARY KEY (id);


--
-- Name: estatebase_contacttype_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_contacttype
    ADD CONSTRAINT estatebase_contacttype_name_key UNIQUE (name);


--
-- Name: estatebase_contacttype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_contacttype
    ADD CONSTRAINT estatebase_contacttype_pkey PRIMARY KEY (id);


--
-- Name: estatebase_document_estate_type_categ_document_id_4877af75_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_document_estate_type_category
    ADD CONSTRAINT estatebase_document_estate_type_categ_document_id_4877af75_uniq UNIQUE (document_id, estatetypecategory_id);


--
-- Name: estatebase_document_estate_type_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_document_estate_type_category
    ADD CONSTRAINT estatebase_document_estate_type_category_pkey PRIMARY KEY (id);


--
-- Name: estatebase_document_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_document
    ADD CONSTRAINT estatebase_document_name_key UNIQUE (name);


--
-- Name: estatebase_document_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_document
    ADD CONSTRAINT estatebase_document_pkey PRIMARY KEY (id);


--
-- Name: estatebase_driveway_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_driveway
    ADD CONSTRAINT estatebase_driveway_name_key UNIQUE (name);


--
-- Name: estatebase_driveway_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_driveway
    ADD CONSTRAINT estatebase_driveway_pkey PRIMARY KEY (id);


--
-- Name: estatebase_electricity_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_electricity
    ADD CONSTRAINT estatebase_electricity_name_key UNIQUE (name);


--
-- Name: estatebase_electricity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_electricity
    ADD CONSTRAINT estatebase_electricity_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estate_estate_params_estate_id_64deb71d_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estate_estate_params
    ADD CONSTRAINT estatebase_estate_estate_params_estate_id_64deb71d_uniq UNIQUE (estate_id, estateparam_id);


--
-- Name: estatebase_estate_estate_params_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estate_estate_params
    ADD CONSTRAINT estatebase_estate_estate_params_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estate_history_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT estatebase_estate_history_id_key UNIQUE (history_id);


--
-- Name: estatebase_estate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT estatebase_estate_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estateclient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateclient
    ADD CONSTRAINT estatebase_estateclient_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estateclientstatus_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateclientstatus
    ADD CONSTRAINT estatebase_estateclientstatus_name_key UNIQUE (name);


--
-- Name: estatebase_estateclientstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateclientstatus
    ADD CONSTRAINT estatebase_estateclientstatus_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estateparam_order_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateparam
    ADD CONSTRAINT estatebase_estateparam_order_key UNIQUE ("order");


--
-- Name: estatebase_estateparam_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateparam
    ADD CONSTRAINT estatebase_estateparam_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estatephoto_order_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estatephoto
    ADD CONSTRAINT estatebase_estatephoto_order_key UNIQUE ("order");


--
-- Name: estatebase_estatephoto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estatephoto
    ADD CONSTRAINT estatebase_estatephoto_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estateregister_bids_estateregister_id_6c268d5_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateregister_bids
    ADD CONSTRAINT estatebase_estateregister_bids_estateregister_id_6c268d5_uniq UNIQUE (estateregister_id, bid_id);


--
-- Name: estatebase_estateregister_bids_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateregister_bids
    ADD CONSTRAINT estatebase_estateregister_bids_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estateregister_estat_estateregister_id_6b338789_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateregister_estates
    ADD CONSTRAINT estatebase_estateregister_estat_estateregister_id_6b338789_uniq UNIQUE (estateregister_id, estate_id);


--
-- Name: estatebase_estateregister_estates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateregister_estates
    ADD CONSTRAINT estatebase_estateregister_estates_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estateregister_history_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateregister
    ADD CONSTRAINT estatebase_estateregister_history_id_key UNIQUE (history_id);


--
-- Name: estatebase_estateregister_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estateregister
    ADD CONSTRAINT estatebase_estateregister_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estatestatus_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estatestatus
    ADD CONSTRAINT estatebase_estatestatus_name_key UNIQUE (name);


--
-- Name: estatebase_estatestatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estatestatus
    ADD CONSTRAINT estatebase_estatestatus_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estatetype_order_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estatetype
    ADD CONSTRAINT estatebase_estatetype_order_key UNIQUE ("order");


--
-- Name: estatebase_estatetype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estatetype
    ADD CONSTRAINT estatebase_estatetype_pkey PRIMARY KEY (id);


--
-- Name: estatebase_estatetypecategory_order_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estatetypecategory
    ADD CONSTRAINT estatebase_estatetypecategory_order_key UNIQUE ("order");


--
-- Name: estatebase_estatetypecategory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_estatetypecategory
    ADD CONSTRAINT estatebase_estatetypecategory_pkey PRIMARY KEY (id);


--
-- Name: estatebase_exteriorfinish_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_exteriorfinish
    ADD CONSTRAINT estatebase_exteriorfinish_name_key UNIQUE (name);


--
-- Name: estatebase_exteriorfinish_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_exteriorfinish
    ADD CONSTRAINT estatebase_exteriorfinish_pkey PRIMARY KEY (id);


--
-- Name: estatebase_flooring_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_flooring
    ADD CONSTRAINT estatebase_flooring_name_key UNIQUE (name);


--
-- Name: estatebase_flooring_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_flooring
    ADD CONSTRAINT estatebase_flooring_pkey PRIMARY KEY (id);


--
-- Name: estatebase_furniture_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_furniture
    ADD CONSTRAINT estatebase_furniture_name_key UNIQUE (name);


--
-- Name: estatebase_furniture_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_furniture
    ADD CONSTRAINT estatebase_furniture_pkey PRIMARY KEY (id);


--
-- Name: estatebase_gassupply_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_gassupply
    ADD CONSTRAINT estatebase_gassupply_name_key UNIQUE (name);


--
-- Name: estatebase_gassupply_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_gassupply
    ADD CONSTRAINT estatebase_gassupply_pkey PRIMARY KEY (id);


--
-- Name: estatebase_geogroup_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_geogroup
    ADD CONSTRAINT estatebase_geogroup_name_key UNIQUE (name);


--
-- Name: estatebase_geogroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_geogroup
    ADD CONSTRAINT estatebase_geogroup_pkey PRIMARY KEY (id);


--
-- Name: estatebase_heating_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_heating
    ADD CONSTRAINT estatebase_heating_name_key UNIQUE (name);


--
-- Name: estatebase_heating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_heating
    ADD CONSTRAINT estatebase_heating_pkey PRIMARY KEY (id);


--
-- Name: estatebase_historymeta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_historymeta
    ADD CONSTRAINT estatebase_historymeta_pkey PRIMARY KEY (id);


--
-- Name: estatebase_interior_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_interior
    ADD CONSTRAINT estatebase_interior_name_key UNIQUE (name);


--
-- Name: estatebase_interior_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_interior
    ADD CONSTRAINT estatebase_interior_pkey PRIMARY KEY (id);


--
-- Name: estatebase_internet_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_internet
    ADD CONSTRAINT estatebase_internet_name_key UNIQUE (name);


--
-- Name: estatebase_internet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_internet
    ADD CONSTRAINT estatebase_internet_pkey PRIMARY KEY (id);


--
-- Name: estatebase_landtype_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_landtype
    ADD CONSTRAINT estatebase_landtype_name_key UNIQUE (name);


--
-- Name: estatebase_landtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_landtype
    ADD CONSTRAINT estatebase_landtype_pkey PRIMARY KEY (id);


--
-- Name: estatebase_layout_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_layout
    ADD CONSTRAINT estatebase_layout_pkey PRIMARY KEY (id);


--
-- Name: estatebase_layoutfeature_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_layoutfeature
    ADD CONSTRAINT estatebase_layoutfeature_name_key UNIQUE (name);


--
-- Name: estatebase_layoutfeature_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_layoutfeature
    ADD CONSTRAINT estatebase_layoutfeature_pkey PRIMARY KEY (id);


--
-- Name: estatebase_layouttype_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_layouttype
    ADD CONSTRAINT estatebase_layouttype_name_key UNIQUE (name);


--
-- Name: estatebase_layouttype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_layouttype
    ADD CONSTRAINT estatebase_layouttype_pkey PRIMARY KEY (id);


--
-- Name: estatebase_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_level
    ADD CONSTRAINT estatebase_level_pkey PRIMARY KEY (id);


--
-- Name: estatebase_levelname_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_levelname
    ADD CONSTRAINT estatebase_levelname_name_key UNIQUE (name);


--
-- Name: estatebase_levelname_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_levelname
    ADD CONSTRAINT estatebase_levelname_pkey PRIMARY KEY (id);


--
-- Name: estatebase_locality_name_4d984da0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_locality
    ADD CONSTRAINT estatebase_locality_name_4d984da0_uniq UNIQUE (name, region_id);


--
-- Name: estatebase_locality_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_locality
    ADD CONSTRAINT estatebase_locality_pkey PRIMARY KEY (id);


--
-- Name: estatebase_microdistrict_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_microdistrict
    ADD CONSTRAINT estatebase_microdistrict_name_key UNIQUE (name);


--
-- Name: estatebase_microdistrict_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_microdistrict
    ADD CONSTRAINT estatebase_microdistrict_pkey PRIMARY KEY (id);


--
-- Name: estatebase_office_name_key; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY estatebase_office
    ADD CONSTRAINT estatebase_office_name_key UNIQUE (name);


--
-- Name: estatebase_office_pkey; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY estatebase_office
    ADD CONSTRAINT estatebase_office_pkey PRIMARY KEY (id);


--
-- Name: estatebase_office_regions_office_id_168c25a16abbf535_uniq; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY estatebase_office_regions
    ADD CONSTRAINT estatebase_office_regions_office_id_168c25a16abbf535_uniq UNIQUE (office_id, region_id);


--
-- Name: estatebase_office_regions_pkey; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY estatebase_office_regions
    ADD CONSTRAINT estatebase_office_regions_pkey PRIMARY KEY (id);


--
-- Name: estatebase_origin_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_origin
    ADD CONSTRAINT estatebase_origin_name_key UNIQUE (name);


--
-- Name: estatebase_origin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_origin
    ADD CONSTRAINT estatebase_origin_pkey PRIMARY KEY (id);


--
-- Name: estatebase_purpose_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_purpose
    ADD CONSTRAINT estatebase_purpose_name_key UNIQUE (name);


--
-- Name: estatebase_purpose_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_purpose
    ADD CONSTRAINT estatebase_purpose_pkey PRIMARY KEY (id);


--
-- Name: estatebase_region_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_region
    ADD CONSTRAINT estatebase_region_name_key UNIQUE (name);


--
-- Name: estatebase_region_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_region
    ADD CONSTRAINT estatebase_region_pkey PRIMARY KEY (id);


--
-- Name: estatebase_roof_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_roof
    ADD CONSTRAINT estatebase_roof_name_key UNIQUE (name);


--
-- Name: estatebase_roof_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_roof
    ADD CONSTRAINT estatebase_roof_pkey PRIMARY KEY (id);


--
-- Name: estatebase_sewerage_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_sewerage
    ADD CONSTRAINT estatebase_sewerage_name_key UNIQUE (name);


--
-- Name: estatebase_sewerage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_sewerage
    ADD CONSTRAINT estatebase_sewerage_pkey PRIMARY KEY (id);


--
-- Name: estatebase_shape_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_shape
    ADD CONSTRAINT estatebase_shape_name_key UNIQUE (name);


--
-- Name: estatebase_shape_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_shape
    ADD CONSTRAINT estatebase_shape_pkey PRIMARY KEY (id);


--
-- Name: estatebase_stead_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_stead_documents
    ADD CONSTRAINT estatebase_stead_documents_pkey PRIMARY KEY (id);


--
-- Name: estatebase_stead_documents_stead_id_74fba25_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_stead_documents
    ADD CONSTRAINT estatebase_stead_documents_stead_id_74fba25_uniq UNIQUE (stead_id, document_id);


--
-- Name: estatebase_stead_estate_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_stead
    ADD CONSTRAINT estatebase_stead_estate_id_key UNIQUE (estate_id);


--
-- Name: estatebase_stead_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_stead
    ADD CONSTRAINT estatebase_stead_pkey PRIMARY KEY (id);


--
-- Name: estatebase_street_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_street
    ADD CONSTRAINT estatebase_street_name_key UNIQUE (name);


--
-- Name: estatebase_street_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_street
    ADD CONSTRAINT estatebase_street_pkey PRIMARY KEY (id);


--
-- Name: estatebase_telephony_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_telephony
    ADD CONSTRAINT estatebase_telephony_name_key UNIQUE (name);


--
-- Name: estatebase_telephony_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_telephony
    ADD CONSTRAINT estatebase_telephony_pkey PRIMARY KEY (id);


--
-- Name: estatebase_userprofile_geo_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_userprofile_geo_groups
    ADD CONSTRAINT estatebase_userprofile_geo_groups_pkey PRIMARY KEY (id);


--
-- Name: estatebase_userprofile_geo_groups_userprofile_id_2c855569_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_userprofile_geo_groups
    ADD CONSTRAINT estatebase_userprofile_geo_groups_userprofile_id_2c855569_uniq UNIQUE (userprofile_id, geogroup_id);


--
-- Name: estatebase_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_userprofile
    ADD CONSTRAINT estatebase_userprofile_pkey PRIMARY KEY (id);


--
-- Name: estatebase_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_userprofile
    ADD CONSTRAINT estatebase_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: estatebase_wallconstrucion_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_wallconstrucion
    ADD CONSTRAINT estatebase_wallconstrucion_name_key UNIQUE (name);


--
-- Name: estatebase_wallconstrucion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_wallconstrucion
    ADD CONSTRAINT estatebase_wallconstrucion_pkey PRIMARY KEY (id);


--
-- Name: estatebase_wallfinish_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_wallfinish
    ADD CONSTRAINT estatebase_wallfinish_name_key UNIQUE (name);


--
-- Name: estatebase_wallfinish_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_wallfinish
    ADD CONSTRAINT estatebase_wallfinish_pkey PRIMARY KEY (id);


--
-- Name: estatebase_watersupply_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_watersupply
    ADD CONSTRAINT estatebase_watersupply_name_key UNIQUE (name);


--
-- Name: estatebase_watersupply_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_watersupply
    ADD CONSTRAINT estatebase_watersupply_pkey PRIMARY KEY (id);


--
-- Name: estatebase_windowtype_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_windowtype
    ADD CONSTRAINT estatebase_windowtype_name_key UNIQUE (name);


--
-- Name: estatebase_windowtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY estatebase_windowtype
    ADD CONSTRAINT estatebase_windowtype_pkey PRIMARY KEY (id);


--
-- Name: sitetree_tree_alias_key; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY sitetree_tree
    ADD CONSTRAINT sitetree_tree_alias_key UNIQUE (alias);


--
-- Name: sitetree_tree_pkey; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY sitetree_tree
    ADD CONSTRAINT sitetree_tree_pkey PRIMARY KEY (id);


--
-- Name: sitetree_treeitem_access_perm_treeitem_id_46bb71549d2f7033_uniq; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY sitetree_treeitem_access_permissions
    ADD CONSTRAINT sitetree_treeitem_access_perm_treeitem_id_46bb71549d2f7033_uniq UNIQUE (treeitem_id, permission_id);


--
-- Name: sitetree_treeitem_access_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY sitetree_treeitem_access_permissions
    ADD CONSTRAINT sitetree_treeitem_access_permissions_pkey PRIMARY KEY (id);


--
-- Name: sitetree_treeitem_pkey; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY sitetree_treeitem
    ADD CONSTRAINT sitetree_treeitem_pkey PRIMARY KEY (id);


--
-- Name: sitetree_treeitem_tree_id_3a9ea9d515363010_uniq; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY sitetree_treeitem
    ADD CONSTRAINT sitetree_treeitem_tree_id_3a9ea9d515363010_uniq UNIQUE (tree_id, alias);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: thumbnail_kvstore_pkey; Type: CONSTRAINT; Schema: public; Owner: realty; Tablespace: 
--

ALTER TABLE ONLY thumbnail_kvstore
    ADD CONSTRAINT thumbnail_kvstore_pkey PRIMARY KEY (key);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: estatebase_bid_broker_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_broker_id ON estatebase_bid USING btree (broker_id);


--
-- Name: estatebase_bid_client_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_client_id ON estatebase_bid USING btree (client_id);


--
-- Name: estatebase_bid_estate_types_bid_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_estate_types_bid_id ON estatebase_bid_estate_types USING btree (bid_id);


--
-- Name: estatebase_bid_estate_types_estatetype_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_estate_types_estatetype_id ON estatebase_bid_estate_types USING btree (estatetype_id);


--
-- Name: estatebase_bid_estates_bid_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_estates_bid_id ON estatebase_bid_estates USING btree (bid_id);


--
-- Name: estatebase_bid_estates_estate_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_estates_estate_id ON estatebase_bid_estates USING btree (estate_id);


--
-- Name: estatebase_bid_localities_bid_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_localities_bid_id ON estatebase_bid_localities USING btree (bid_id);


--
-- Name: estatebase_bid_localities_locality_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_localities_locality_id ON estatebase_bid_localities USING btree (locality_id);


--
-- Name: estatebase_bid_regions_bid_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_regions_bid_id ON estatebase_bid_regions USING btree (bid_id);


--
-- Name: estatebase_bid_regions_region_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bid_regions_region_id ON estatebase_bid_regions USING btree (region_id);


--
-- Name: estatebase_bidg_ceiling_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_ceiling_id ON estatebase_bidg USING btree (ceiling_id);


--
-- Name: estatebase_bidg_documents_bidg_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_documents_bidg_id ON estatebase_bidg_documents USING btree (bidg_id);


--
-- Name: estatebase_bidg_documents_document_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_documents_document_id ON estatebase_bidg_documents USING btree (document_id);


--
-- Name: estatebase_bidg_estate_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_estate_id ON estatebase_bidg USING btree (estate_id);


--
-- Name: estatebase_bidg_estate_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_estate_type_id ON estatebase_bidg USING btree (estate_type_id);


--
-- Name: estatebase_bidg_exterior_finish_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_exterior_finish_id ON estatebase_bidg USING btree (exterior_finish_id);


--
-- Name: estatebase_bidg_flooring_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_flooring_id ON estatebase_bidg USING btree (flooring_id);


--
-- Name: estatebase_bidg_heating_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_heating_id ON estatebase_bidg USING btree (heating_id);


--
-- Name: estatebase_bidg_interior_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_interior_id ON estatebase_bidg USING btree (interior_id);


--
-- Name: estatebase_bidg_roof_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_roof_id ON estatebase_bidg USING btree (roof_id);


--
-- Name: estatebase_bidg_wall_construcion_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_wall_construcion_id ON estatebase_bidg USING btree (wall_construcion_id);


--
-- Name: estatebase_bidg_wall_finish_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_wall_finish_id ON estatebase_bidg USING btree (wall_finish_id);


--
-- Name: estatebase_bidg_window_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_bidg_window_type_id ON estatebase_bidg USING btree (window_type_id);


--
-- Name: estatebase_client_broker_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_client_broker_id ON estatebase_client USING btree (broker_id);


--
-- Name: estatebase_client_client_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_client_client_type_id ON estatebase_client USING btree (client_type_id);


--
-- Name: estatebase_client_origin_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_client_origin_id ON estatebase_client USING btree (origin_id);


--
-- Name: estatebase_contact_client_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_contact_client_id ON estatebase_contact USING btree (client_id);


--
-- Name: estatebase_contact_contact; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_contact_contact ON estatebase_contact USING btree (contact);


--
-- Name: estatebase_contact_contact_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_contact_contact_like ON estatebase_contact USING btree (contact varchar_pattern_ops);


--
-- Name: estatebase_contact_contact_state_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_contact_contact_state_id ON estatebase_contact USING btree (contact_state_id);


--
-- Name: estatebase_contact_contact_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_contact_contact_type_id ON estatebase_contact USING btree (contact_type_id);


--
-- Name: estatebase_contacthistory_contact_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_contacthistory_contact_id ON estatebase_contacthistory USING btree (contact_id);


--
-- Name: estatebase_contacthistory_contact_state_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_contacthistory_contact_state_id ON estatebase_contacthistory USING btree (contact_state_id);


--
-- Name: estatebase_contacthistory_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_contacthistory_user_id ON estatebase_contacthistory USING btree (user_id);


--
-- Name: estatebase_document_estate_type_category_document_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_document_estate_type_category_document_id ON estatebase_document_estate_type_category USING btree (document_id);


--
-- Name: estatebase_document_estate_type_category_estatetypecategory_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_document_estate_type_category_estatetypecategory_id ON estatebase_document_estate_type_category USING btree (estatetypecategory_id);


--
-- Name: estatebase_estate_beside_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_beside_id ON estatebase_estate USING btree (beside_id);


--
-- Name: estatebase_estate_broker_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_broker_id ON estatebase_estate USING btree (broker_id);


--
-- Name: estatebase_estate_com_status_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_com_status_id ON estatebase_estate USING btree (com_status_id);


--
-- Name: estatebase_estate_contact_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_contact_id ON estatebase_estate USING btree (contact_id);


--
-- Name: estatebase_estate_driveway_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_driveway_id ON estatebase_estate USING btree (driveway_id);


--
-- Name: estatebase_estate_electricity_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_electricity_id ON estatebase_estate USING btree (electricity_id);


--
-- Name: estatebase_estate_estate_category_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_estate_category_id ON estatebase_estate USING btree (estate_category_id);


--
-- Name: estatebase_estate_estate_params_estate_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_estate_params_estate_id ON estatebase_estate_estate_params USING btree (estate_id);


--
-- Name: estatebase_estate_estate_params_estateparam_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_estate_params_estateparam_id ON estatebase_estate_estate_params USING btree (estateparam_id);


--
-- Name: estatebase_estate_estate_status_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_estate_status_id ON estatebase_estate USING btree (estate_status_id);


--
-- Name: estatebase_estate_gassupply_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_gassupply_id ON estatebase_estate USING btree (gassupply_id);


--
-- Name: estatebase_estate_internet_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_internet_id ON estatebase_estate USING btree (internet_id);


--
-- Name: estatebase_estate_locality_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_locality_id ON estatebase_estate USING btree (locality_id);


--
-- Name: estatebase_estate_microdistrict_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_microdistrict_id ON estatebase_estate USING btree (microdistrict_id);


--
-- Name: estatebase_estate_origin_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_origin_id ON estatebase_estate USING btree (origin_id);


--
-- Name: estatebase_estate_region_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_region_id ON estatebase_estate USING btree (region_id);


--
-- Name: estatebase_estate_sewerage_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_sewerage_id ON estatebase_estate USING btree (sewerage_id);


--
-- Name: estatebase_estate_street_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_street_id ON estatebase_estate USING btree (street_id);


--
-- Name: estatebase_estate_telephony_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_telephony_id ON estatebase_estate USING btree (telephony_id);


--
-- Name: estatebase_estate_watersupply_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estate_watersupply_id ON estatebase_estate USING btree (watersupply_id);


--
-- Name: estatebase_estateclient_client_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateclient_client_id ON estatebase_estateclient USING btree (client_id);


--
-- Name: estatebase_estateclient_estate_client_status_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateclient_estate_client_status_id ON estatebase_estateclient USING btree (estate_client_status_id);


--
-- Name: estatebase_estateclient_estate_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateclient_estate_id ON estatebase_estateclient USING btree (estate_id);


--
-- Name: estatebase_estatephoto_estate_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estatephoto_estate_id ON estatebase_estatephoto USING btree (estate_id);


--
-- Name: estatebase_estateregister_bids_bid_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateregister_bids_bid_id ON estatebase_estateregister_bids USING btree (bid_id);


--
-- Name: estatebase_estateregister_bids_estateregister_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateregister_bids_estateregister_id ON estatebase_estateregister_bids USING btree (estateregister_id);


--
-- Name: estatebase_estateregister_broker_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateregister_broker_id ON estatebase_estateregister USING btree (broker_id);


--
-- Name: estatebase_estateregister_estates_estate_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateregister_estates_estate_id ON estatebase_estateregister_estates USING btree (estate_id);


--
-- Name: estatebase_estateregister_estates_estateregister_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateregister_estates_estateregister_id ON estatebase_estateregister_estates USING btree (estateregister_id);


--
-- Name: estatebase_estateregister_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateregister_name ON estatebase_estateregister USING btree (name);


--
-- Name: estatebase_estateregister_name_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estateregister_name_like ON estatebase_estateregister USING btree (name varchar_pattern_ops);


--
-- Name: estatebase_estatetype_estate_type_category_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_estatetype_estate_type_category_id ON estatebase_estatetype USING btree (estate_type_category_id);


--
-- Name: estatebase_historymeta_created_by_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_historymeta_created_by_id ON estatebase_historymeta USING btree (created_by_id);


--
-- Name: estatebase_historymeta_updated_by_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_historymeta_updated_by_id ON estatebase_historymeta USING btree (updated_by_id);


--
-- Name: estatebase_layout_furniture_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_layout_furniture_id ON estatebase_layout USING btree (furniture_id);


--
-- Name: estatebase_layout_interior_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_layout_interior_id ON estatebase_layout USING btree (interior_id);


--
-- Name: estatebase_layout_layout_feature_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_layout_layout_feature_id ON estatebase_layout USING btree (layout_feature_id);


--
-- Name: estatebase_layout_layout_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_layout_layout_type_id ON estatebase_layout USING btree (layout_type_id);


--
-- Name: estatebase_layout_level_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_layout_level_id ON estatebase_layout USING btree (level_id);


--
-- Name: estatebase_level_bidg_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_level_bidg_id ON estatebase_level USING btree (bidg_id);


--
-- Name: estatebase_level_level_name_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_level_level_name_id ON estatebase_level USING btree (level_name_id);


--
-- Name: estatebase_locality_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_locality_name ON estatebase_locality USING btree (name);


--
-- Name: estatebase_locality_name_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_locality_name_like ON estatebase_locality USING btree (name varchar_pattern_ops);


--
-- Name: estatebase_locality_region_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_locality_region_id ON estatebase_locality USING btree (region_id);


--
-- Name: estatebase_microdistrict_locality_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_microdistrict_locality_id ON estatebase_microdistrict USING btree (locality_id);


--
-- Name: estatebase_office_regions_office_id; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX estatebase_office_regions_office_id ON estatebase_office_regions USING btree (office_id);


--
-- Name: estatebase_office_regions_region_id; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX estatebase_office_regions_region_id ON estatebase_office_regions USING btree (region_id);


--
-- Name: estatebase_region_geo_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_region_geo_group_id ON estatebase_region USING btree (geo_group_id);


--
-- Name: estatebase_stead_documents_document_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_stead_documents_document_id ON estatebase_stead_documents USING btree (document_id);


--
-- Name: estatebase_stead_documents_stead_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_stead_documents_stead_id ON estatebase_stead_documents USING btree (stead_id);


--
-- Name: estatebase_stead_estate_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_stead_estate_type_id ON estatebase_stead USING btree (estate_type_id);


--
-- Name: estatebase_stead_land_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_stead_land_type_id ON estatebase_stead USING btree (land_type_id);


--
-- Name: estatebase_stead_purpose_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_stead_purpose_id ON estatebase_stead USING btree (purpose_id);


--
-- Name: estatebase_stead_shape_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_stead_shape_id ON estatebase_stead USING btree (shape_id);


--
-- Name: estatebase_street_locality_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_street_locality_id ON estatebase_street USING btree (locality_id);


--
-- Name: estatebase_userprofile_geo_groups_geogroup_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_userprofile_geo_groups_geogroup_id ON estatebase_userprofile_geo_groups USING btree (geogroup_id);


--
-- Name: estatebase_userprofile_geo_groups_userprofile_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_userprofile_geo_groups_userprofile_id ON estatebase_userprofile_geo_groups USING btree (userprofile_id);


--
-- Name: estatebase_userprofile_office_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX estatebase_userprofile_office_id ON estatebase_userprofile USING btree (office_id);


--
-- Name: sitetree_treeitem_access_loggedin; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_access_loggedin ON sitetree_treeitem USING btree (access_loggedin);


--
-- Name: sitetree_treeitem_access_permissions_permission_id; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_access_permissions_permission_id ON sitetree_treeitem_access_permissions USING btree (permission_id);


--
-- Name: sitetree_treeitem_access_permissions_treeitem_id; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_access_permissions_treeitem_id ON sitetree_treeitem_access_permissions USING btree (treeitem_id);


--
-- Name: sitetree_treeitem_access_restricted; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_access_restricted ON sitetree_treeitem USING btree (access_restricted);


--
-- Name: sitetree_treeitem_alias; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_alias ON sitetree_treeitem USING btree (alias);


--
-- Name: sitetree_treeitem_alias_like; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_alias_like ON sitetree_treeitem USING btree (alias varchar_pattern_ops);


--
-- Name: sitetree_treeitem_hidden; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_hidden ON sitetree_treeitem USING btree (hidden);


--
-- Name: sitetree_treeitem_inbreadcrumbs; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_inbreadcrumbs ON sitetree_treeitem USING btree (inbreadcrumbs);


--
-- Name: sitetree_treeitem_inmenu; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_inmenu ON sitetree_treeitem USING btree (inmenu);


--
-- Name: sitetree_treeitem_insitetree; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_insitetree ON sitetree_treeitem USING btree (insitetree);


--
-- Name: sitetree_treeitem_parent_id; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_parent_id ON sitetree_treeitem USING btree (parent_id);


--
-- Name: sitetree_treeitem_sort_order; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_sort_order ON sitetree_treeitem USING btree (sort_order);


--
-- Name: sitetree_treeitem_tree_id; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_tree_id ON sitetree_treeitem USING btree (tree_id);


--
-- Name: sitetree_treeitem_url; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_url ON sitetree_treeitem USING btree (url);


--
-- Name: sitetree_treeitem_url_like; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_url_like ON sitetree_treeitem USING btree (url varchar_pattern_ops);


--
-- Name: sitetree_treeitem_urlaspattern; Type: INDEX; Schema: public; Owner: realty; Tablespace: 
--

CREATE INDEX sitetree_treeitem_urlaspattern ON sitetree_treeitem USING btree (urlaspattern);


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: beside_id_refs_id_305f4f5f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT beside_id_refs_id_305f4f5f FOREIGN KEY (beside_id) REFERENCES estatebase_beside(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bid_id_refs_id_196d4bf0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_localities
    ADD CONSTRAINT bid_id_refs_id_196d4bf0 FOREIGN KEY (bid_id) REFERENCES estatebase_bid(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bid_id_refs_id_1e98cf0f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_regions
    ADD CONSTRAINT bid_id_refs_id_1e98cf0f FOREIGN KEY (bid_id) REFERENCES estatebase_bid(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bid_id_refs_id_30a8520f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_estate_types
    ADD CONSTRAINT bid_id_refs_id_30a8520f FOREIGN KEY (bid_id) REFERENCES estatebase_bid(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bid_id_refs_id_4949b119; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_estates
    ADD CONSTRAINT bid_id_refs_id_4949b119 FOREIGN KEY (bid_id) REFERENCES estatebase_bid(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bid_id_refs_id_5383483a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister_bids
    ADD CONSTRAINT bid_id_refs_id_5383483a FOREIGN KEY (bid_id) REFERENCES estatebase_bid(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bidg_id_refs_id_38fdde70; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg_documents
    ADD CONSTRAINT bidg_id_refs_id_38fdde70 FOREIGN KEY (bidg_id) REFERENCES estatebase_bidg(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bidg_id_refs_id_5d9a5014; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_level
    ADD CONSTRAINT bidg_id_refs_id_5d9a5014 FOREIGN KEY (bidg_id) REFERENCES estatebase_bidg(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: broker_id_refs_id_12b064ca; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_client
    ADD CONSTRAINT broker_id_refs_id_12b064ca FOREIGN KEY (broker_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: broker_id_refs_id_1e326858; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister
    ADD CONSTRAINT broker_id_refs_id_1e326858 FOREIGN KEY (broker_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: broker_id_refs_id_43c7709f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT broker_id_refs_id_43c7709f FOREIGN KEY (broker_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: broker_id_refs_id_7da813d7; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid
    ADD CONSTRAINT broker_id_refs_id_7da813d7 FOREIGN KEY (broker_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ceiling_id_refs_id_297a778f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT ceiling_id_refs_id_297a778f FOREIGN KEY (ceiling_id) REFERENCES estatebase_ceiling(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: client_id_refs_id_588444b1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contact
    ADD CONSTRAINT client_id_refs_id_588444b1 FOREIGN KEY (client_id) REFERENCES estatebase_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: client_id_refs_id_612d1678; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid
    ADD CONSTRAINT client_id_refs_id_612d1678 FOREIGN KEY (client_id) REFERENCES estatebase_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: client_id_refs_id_ffeb97b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateclient
    ADD CONSTRAINT client_id_refs_id_ffeb97b FOREIGN KEY (client_id) REFERENCES estatebase_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: client_type_id_refs_id_380a7bab; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_client
    ADD CONSTRAINT client_type_id_refs_id_380a7bab FOREIGN KEY (client_type_id) REFERENCES estatebase_clienttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: com_status_id_refs_id_41394a9d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT com_status_id_refs_id_41394a9d FOREIGN KEY (com_status_id) REFERENCES estatebase_comstatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_id_refs_id_746e8d28; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contacthistory
    ADD CONSTRAINT contact_id_refs_id_746e8d28 FOREIGN KEY (contact_id) REFERENCES estatebase_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_id_refs_id_785a36e4; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT contact_id_refs_id_785a36e4 FOREIGN KEY (contact_id) REFERENCES estatebase_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_state_id_refs_id_31124a9; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contact
    ADD CONSTRAINT contact_state_id_refs_id_31124a9 FOREIGN KEY (contact_state_id) REFERENCES estatebase_contactstate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_state_id_refs_id_491b6e72; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contacthistory
    ADD CONSTRAINT contact_state_id_refs_id_491b6e72 FOREIGN KEY (contact_state_id) REFERENCES estatebase_contactstate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_type_id_refs_id_cff0cb9; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contact
    ADD CONSTRAINT contact_type_id_refs_id_cff0cb9 FOREIGN KEY (contact_type_id) REFERENCES estatebase_contacttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: created_by_id_refs_id_10fb35e7; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_historymeta
    ADD CONSTRAINT created_by_id_refs_id_10fb35e7 FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_id_refs_id_23cb2885; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead_documents
    ADD CONSTRAINT document_id_refs_id_23cb2885 FOREIGN KEY (document_id) REFERENCES estatebase_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_id_refs_id_28c71d9d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_document_estate_type_category
    ADD CONSTRAINT document_id_refs_id_28c71d9d FOREIGN KEY (document_id) REFERENCES estatebase_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: document_id_refs_id_7d31c443; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg_documents
    ADD CONSTRAINT document_id_refs_id_7d31c443 FOREIGN KEY (document_id) REFERENCES estatebase_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: driveway_id_refs_id_6047ff3c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT driveway_id_refs_id_6047ff3c FOREIGN KEY (driveway_id) REFERENCES estatebase_driveway(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: electricity_id_refs_id_413cb65f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT electricity_id_refs_id_413cb65f FOREIGN KEY (electricity_id) REFERENCES estatebase_electricity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_category_id_refs_id_576e20d1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT estate_category_id_refs_id_576e20d1 FOREIGN KEY (estate_category_id) REFERENCES estatebase_estatetypecategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_client_status_id_refs_id_5e04ae85; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateclient
    ADD CONSTRAINT estate_client_status_id_refs_id_5e04ae85 FOREIGN KEY (estate_client_status_id) REFERENCES estatebase_estateclientstatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_id_refs_id_1e6cc8e7; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate_estate_params
    ADD CONSTRAINT estate_id_refs_id_1e6cc8e7 FOREIGN KEY (estate_id) REFERENCES estatebase_estate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_id_refs_id_220e89bf; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead
    ADD CONSTRAINT estate_id_refs_id_220e89bf FOREIGN KEY (estate_id) REFERENCES estatebase_estate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_id_refs_id_4bca5f06; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateclient
    ADD CONSTRAINT estate_id_refs_id_4bca5f06 FOREIGN KEY (estate_id) REFERENCES estatebase_estate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_id_refs_id_59e8f78c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister_estates
    ADD CONSTRAINT estate_id_refs_id_59e8f78c FOREIGN KEY (estate_id) REFERENCES estatebase_estate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_id_refs_id_64e1186; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estatephoto
    ADD CONSTRAINT estate_id_refs_id_64e1186 FOREIGN KEY (estate_id) REFERENCES estatebase_estate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_id_refs_id_6c1ab939; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT estate_id_refs_id_6c1ab939 FOREIGN KEY (estate_id) REFERENCES estatebase_estate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_id_refs_id_7373ac9; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_estates
    ADD CONSTRAINT estate_id_refs_id_7373ac9 FOREIGN KEY (estate_id) REFERENCES estatebase_estate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_status_id_refs_id_2a7eb4a1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT estate_status_id_refs_id_2a7eb4a1 FOREIGN KEY (estate_status_id) REFERENCES estatebase_estatestatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_type_category_id_refs_id_35be70db; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estatetype
    ADD CONSTRAINT estate_type_category_id_refs_id_35be70db FOREIGN KEY (estate_type_category_id) REFERENCES estatebase_estatetypecategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_type_id_refs_id_160f79bd; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT estate_type_id_refs_id_160f79bd FOREIGN KEY (estate_type_id) REFERENCES estatebase_estatetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estate_type_id_refs_id_5f7370c3; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead
    ADD CONSTRAINT estate_type_id_refs_id_5f7370c3 FOREIGN KEY (estate_type_id) REFERENCES estatebase_estatetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estateparam_id_refs_id_3f868ed7; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate_estate_params
    ADD CONSTRAINT estateparam_id_refs_id_3f868ed7 FOREIGN KEY (estateparam_id) REFERENCES estatebase_estateparam(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estateregister_id_refs_id_12faec37; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister_bids
    ADD CONSTRAINT estateregister_id_refs_id_12faec37 FOREIGN KEY (estateregister_id) REFERENCES estatebase_estateregister(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estateregister_id_refs_id_1e832d3b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister_estates
    ADD CONSTRAINT estateregister_id_refs_id_1e832d3b FOREIGN KEY (estateregister_id) REFERENCES estatebase_estateregister(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estatetype_id_refs_id_38c3cc63; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_estate_types
    ADD CONSTRAINT estatetype_id_refs_id_38c3cc63 FOREIGN KEY (estatetype_id) REFERENCES estatebase_estatetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: estatetypecategory_id_refs_id_6480c810; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_document_estate_type_category
    ADD CONSTRAINT estatetypecategory_id_refs_id_6480c810 FOREIGN KEY (estatetypecategory_id) REFERENCES estatebase_estatetypecategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exterior_finish_id_refs_id_551914c2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT exterior_finish_id_refs_id_551914c2 FOREIGN KEY (exterior_finish_id) REFERENCES estatebase_exteriorfinish(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: flooring_id_refs_id_5dd2c2b5; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT flooring_id_refs_id_5dd2c2b5 FOREIGN KEY (flooring_id) REFERENCES estatebase_flooring(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: furniture_id_refs_id_13c674b6; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_layout
    ADD CONSTRAINT furniture_id_refs_id_13c674b6 FOREIGN KEY (furniture_id) REFERENCES estatebase_furniture(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gassupply_id_refs_id_45fea0f4; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT gassupply_id_refs_id_45fea0f4 FOREIGN KEY (gassupply_id) REFERENCES estatebase_gassupply(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: geo_group_id_refs_id_7ee17191; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_region
    ADD CONSTRAINT geo_group_id_refs_id_7ee17191 FOREIGN KEY (geo_group_id) REFERENCES estatebase_geogroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: geogroup_id_refs_id_7f93c226; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_userprofile_geo_groups
    ADD CONSTRAINT geogroup_id_refs_id_7f93c226 FOREIGN KEY (geogroup_id) REFERENCES estatebase_geogroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: heating_id_refs_id_18737590; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT heating_id_refs_id_18737590 FOREIGN KEY (heating_id) REFERENCES estatebase_heating(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_id_refs_id_37cfc09a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estateregister
    ADD CONSTRAINT history_id_refs_id_37cfc09a FOREIGN KEY (history_id) REFERENCES estatebase_historymeta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_id_refs_id_580b4414; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_client
    ADD CONSTRAINT history_id_refs_id_580b4414 FOREIGN KEY (history_id) REFERENCES estatebase_historymeta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_id_refs_id_675346cb; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT history_id_refs_id_675346cb FOREIGN KEY (history_id) REFERENCES estatebase_historymeta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_id_refs_id_d7e1e55; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid
    ADD CONSTRAINT history_id_refs_id_d7e1e55 FOREIGN KEY (history_id) REFERENCES estatebase_historymeta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: interior_id_refs_id_15081653; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_layout
    ADD CONSTRAINT interior_id_refs_id_15081653 FOREIGN KEY (interior_id) REFERENCES estatebase_interior(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: interior_id_refs_id_5df8b1b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT interior_id_refs_id_5df8b1b FOREIGN KEY (interior_id) REFERENCES estatebase_interior(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: internet_id_refs_id_34c21156; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT internet_id_refs_id_34c21156 FOREIGN KEY (internet_id) REFERENCES estatebase_internet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: land_type_id_refs_id_2e7a32b6; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead
    ADD CONSTRAINT land_type_id_refs_id_2e7a32b6 FOREIGN KEY (land_type_id) REFERENCES estatebase_landtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: layout_feature_id_refs_id_5313add0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_layout
    ADD CONSTRAINT layout_feature_id_refs_id_5313add0 FOREIGN KEY (layout_feature_id) REFERENCES estatebase_layoutfeature(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: layout_type_id_refs_id_1004a4e9; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_layout
    ADD CONSTRAINT layout_type_id_refs_id_1004a4e9 FOREIGN KEY (layout_type_id) REFERENCES estatebase_layouttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: level_id_refs_id_5fe92d36; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_layout
    ADD CONSTRAINT level_id_refs_id_5fe92d36 FOREIGN KEY (level_id) REFERENCES estatebase_level(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: level_name_id_refs_id_340d337c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_level
    ADD CONSTRAINT level_name_id_refs_id_340d337c FOREIGN KEY (level_name_id) REFERENCES estatebase_levelname(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locality_id_refs_id_2fb108d6; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT locality_id_refs_id_2fb108d6 FOREIGN KEY (locality_id) REFERENCES estatebase_locality(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locality_id_refs_id_567a11f3; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_street
    ADD CONSTRAINT locality_id_refs_id_567a11f3 FOREIGN KEY (locality_id) REFERENCES estatebase_locality(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locality_id_refs_id_5b7acc1b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_microdistrict
    ADD CONSTRAINT locality_id_refs_id_5b7acc1b FOREIGN KEY (locality_id) REFERENCES estatebase_locality(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locality_id_refs_id_715c5e11; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_localities
    ADD CONSTRAINT locality_id_refs_id_715c5e11 FOREIGN KEY (locality_id) REFERENCES estatebase_locality(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: microdistrict_id_refs_id_46b38cc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT microdistrict_id_refs_id_46b38cc FOREIGN KEY (microdistrict_id) REFERENCES estatebase_microdistrict(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: office_id_refs_id_1b514ec3b9281295; Type: FK CONSTRAINT; Schema: public; Owner: realty
--

ALTER TABLE ONLY estatebase_office_regions
    ADD CONSTRAINT office_id_refs_id_1b514ec3b9281295 FOREIGN KEY (office_id) REFERENCES estatebase_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: office_id_refs_id_8b102e858a518ce; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_userprofile
    ADD CONSTRAINT office_id_refs_id_8b102e858a518ce FOREIGN KEY (office_id) REFERENCES estatebase_office(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: origin_id_refs_id_554a7e2f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT origin_id_refs_id_554a7e2f FOREIGN KEY (origin_id) REFERENCES estatebase_origin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: origin_id_refs_id_63903266; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_client
    ADD CONSTRAINT origin_id_refs_id_63903266 FOREIGN KEY (origin_id) REFERENCES estatebase_origin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parent_id_refs_id_544cc1c8d31ebb6b; Type: FK CONSTRAINT; Schema: public; Owner: realty
--

ALTER TABLE ONLY sitetree_treeitem
    ADD CONSTRAINT parent_id_refs_id_544cc1c8d31ebb6b FOREIGN KEY (parent_id) REFERENCES sitetree_treeitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: permission_id_refs_id_7eab21ef0fe20fd9; Type: FK CONSTRAINT; Schema: public; Owner: realty
--

ALTER TABLE ONLY sitetree_treeitem_access_permissions
    ADD CONSTRAINT permission_id_refs_id_7eab21ef0fe20fd9 FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: purpose_id_refs_id_75ffecde; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead
    ADD CONSTRAINT purpose_id_refs_id_75ffecde FOREIGN KEY (purpose_id) REFERENCES estatebase_purpose(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: region_id_refs_id_3b60888b; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT region_id_refs_id_3b60888b FOREIGN KEY (region_id) REFERENCES estatebase_region(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: region_id_refs_id_42a82440acbb39df; Type: FK CONSTRAINT; Schema: public; Owner: realty
--

ALTER TABLE ONLY estatebase_office_regions
    ADD CONSTRAINT region_id_refs_id_42a82440acbb39df FOREIGN KEY (region_id) REFERENCES estatebase_region(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: region_id_refs_id_78db2757; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bid_regions
    ADD CONSTRAINT region_id_refs_id_78db2757 FOREIGN KEY (region_id) REFERENCES estatebase_region(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: region_id_refs_id_7e7967e0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_locality
    ADD CONSTRAINT region_id_refs_id_7e7967e0 FOREIGN KEY (region_id) REFERENCES estatebase_region(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: roof_id_refs_id_2d72593; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT roof_id_refs_id_2d72593 FOREIGN KEY (roof_id) REFERENCES estatebase_roof(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sewerage_id_refs_id_2aee44b6; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT sewerage_id_refs_id_2aee44b6 FOREIGN KEY (sewerage_id) REFERENCES estatebase_sewerage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shape_id_refs_id_5c2b89b5; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead
    ADD CONSTRAINT shape_id_refs_id_5c2b89b5 FOREIGN KEY (shape_id) REFERENCES estatebase_shape(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: stead_id_refs_id_6586dc80; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_stead_documents
    ADD CONSTRAINT stead_id_refs_id_6586dc80 FOREIGN KEY (stead_id) REFERENCES estatebase_stead(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: street_id_refs_id_3d1ec08e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT street_id_refs_id_3d1ec08e FOREIGN KEY (street_id) REFERENCES estatebase_street(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: telephony_id_refs_id_24b78596; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT telephony_id_refs_id_24b78596 FOREIGN KEY (telephony_id) REFERENCES estatebase_telephony(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tree_id_refs_id_71c13f09dc469310; Type: FK CONSTRAINT; Schema: public; Owner: realty
--

ALTER TABLE ONLY sitetree_treeitem
    ADD CONSTRAINT tree_id_refs_id_71c13f09dc469310 FOREIGN KEY (tree_id) REFERENCES sitetree_tree(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: treeitem_id_refs_id_2972dd2a606a90e8; Type: FK CONSTRAINT; Schema: public; Owner: realty
--

ALTER TABLE ONLY sitetree_treeitem_access_permissions
    ADD CONSTRAINT treeitem_id_refs_id_2972dd2a606a90e8 FOREIGN KEY (treeitem_id) REFERENCES sitetree_treeitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: updated_by_id_refs_id_10fb35e7; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_historymeta
    ADD CONSTRAINT updated_by_id_refs_id_10fb35e7 FOREIGN KEY (updated_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_507ba855; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_contacthistory
    ADD CONSTRAINT user_id_refs_id_507ba855 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_727dfc58; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_userprofile
    ADD CONSTRAINT user_id_refs_id_727dfc58 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_7ceef80f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_7ceef80f FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_dfbab7d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_dfbab7d FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: userprofile_id_refs_id_79195f9d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_userprofile_geo_groups
    ADD CONSTRAINT userprofile_id_refs_id_79195f9d FOREIGN KEY (userprofile_id) REFERENCES estatebase_userprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: wall_construcion_id_refs_id_6f87afc5; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT wall_construcion_id_refs_id_6f87afc5 FOREIGN KEY (wall_construcion_id) REFERENCES estatebase_wallconstrucion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: wall_finish_id_refs_id_6df5dfd4; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT wall_finish_id_refs_id_6df5dfd4 FOREIGN KEY (wall_finish_id) REFERENCES estatebase_wallfinish(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: watersupply_id_refs_id_6007b4a4; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_estate
    ADD CONSTRAINT watersupply_id_refs_id_6007b4a4 FOREIGN KEY (watersupply_id) REFERENCES estatebase_watersupply(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: window_type_id_refs_id_2c97217d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY estatebase_bidg
    ADD CONSTRAINT window_type_id_refs_id_2c97217d FOREIGN KEY (window_type_id) REFERENCES estatebase_windowtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

