--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
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
-- Name: categories; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE categories (
    category_id integer NOT NULL,
    category character varying(64) NOT NULL,
    alias character varying(64) NOT NULL
);


ALTER TABLE public.categories OWNER TO "user";

--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE categories_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_category_id_seq OWNER TO "user";

--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE categories_category_id_seq OWNED BY categories.category_id;


--
-- Name: favorites; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE favorites (
    favorite_id integer NOT NULL,
    restaurant_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.favorites OWNER TO "user";

--
-- Name: favorites_favorite_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE favorites_favorite_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.favorites_favorite_id_seq OWNER TO "user";

--
-- Name: favorites_favorite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE favorites_favorite_id_seq OWNED BY favorites.favorite_id;


--
-- Name: restaurant_categories; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE restaurant_categories (
    restaurant_category_id integer NOT NULL,
    restaurant_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.restaurant_categories OWNER TO "user";

--
-- Name: restaurant_categories_restaurant_category_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE restaurant_categories_restaurant_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.restaurant_categories_restaurant_category_id_seq OWNER TO "user";

--
-- Name: restaurant_categories_restaurant_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE restaurant_categories_restaurant_category_id_seq OWNED BY restaurant_categories.restaurant_category_id;


--
-- Name: restaurants; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE restaurants (
    restaurant_id integer NOT NULL,
    name character varying(100) NOT NULL,
    address character varying(100) NOT NULL,
    phone character varying(14) NOT NULL,
    yelp_phone character varying(12) NOT NULL,
    yelp_id character varying(100) NOT NULL,
    yelp_url character varying(200) NOT NULL,
    yelp_img_url character varying(200) NOT NULL,
    yelp_rating double precision NOT NULL,
    yelp_rating_img character varying(200) NOT NULL,
    yelp_review_count integer,
    lat double precision NOT NULL,
    lng double precision NOT NULL
);


ALTER TABLE public.restaurants OWNER TO "user";

--
-- Name: restaurants_restaurant_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE restaurants_restaurant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.restaurants_restaurant_id_seq OWNER TO "user";

--
-- Name: restaurants_restaurant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE restaurants_restaurant_id_seq OWNED BY restaurants.restaurant_id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE reviews (
    review_id integer NOT NULL,
    restaurant_id integer NOT NULL,
    user_id integer NOT NULL,
    rating double precision NOT NULL,
    body character varying(2000) NOT NULL
);


ALTER TABLE public.reviews OWNER TO "user";

--
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE reviews_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_review_id_seq OWNER TO "user";

--
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE reviews_review_id_seq OWNED BY reviews.review_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    username character varying(64) NOT NULL,
    password character varying(64) NOT NULL,
    fname character varying(64) NOT NULL,
    lname character varying(64) NOT NULL
);


ALTER TABLE public.users OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: yelp_reviews; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE yelp_reviews (
    yelp_review_id integer NOT NULL,
    yelp_id character varying(100),
    body character varying(2000) NOT NULL
);


ALTER TABLE public.yelp_reviews OWNER TO "user";

--
-- Name: yelp_reviews_yelp_review_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE yelp_reviews_yelp_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.yelp_reviews_yelp_review_id_seq OWNER TO "user";

--
-- Name: yelp_reviews_yelp_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE yelp_reviews_yelp_review_id_seq OWNED BY yelp_reviews.yelp_review_id;


--
-- Name: category_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY categories ALTER COLUMN category_id SET DEFAULT nextval('categories_category_id_seq'::regclass);


--
-- Name: favorite_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY favorites ALTER COLUMN favorite_id SET DEFAULT nextval('favorites_favorite_id_seq'::regclass);


--
-- Name: restaurant_category_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY restaurant_categories ALTER COLUMN restaurant_category_id SET DEFAULT nextval('restaurant_categories_restaurant_category_id_seq'::regclass);


--
-- Name: restaurant_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY restaurants ALTER COLUMN restaurant_id SET DEFAULT nextval('restaurants_restaurant_id_seq'::regclass);


--
-- Name: review_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY reviews ALTER COLUMN review_id SET DEFAULT nextval('reviews_review_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Name: yelp_review_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY yelp_reviews ALTER COLUMN yelp_review_id SET DEFAULT nextval('yelp_reviews_yelp_review_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: user
--

COPY categories (category_id, category, alias) FROM stdin;
1	Caribbean	caribbean
2	Dance Clubs	danceclubs
3	Lounges	lounges
4	American (New)	newamerican
5	Tapas/Small Plates	tapasmallplates
6	Donuts	donuts
7	French	french
8	Gluten-Free	gluten_free
9	Butcher	butcher
10	Breakfast & Brunch	breakfast_brunch
11	Indian	indpak
12	Sandwiches	sandwiches
13	Latin American	latin
14	Korean	korean
15	Argentine	argentine
16	Pizza	pizza
17	Indonesian	indonesian
18	Tea Rooms	tea
19	Filipino	filipino
20	Hawaiian	hawaiian
21	Desserts	desserts
22	Coffee & Tea	coffee
23	Beer, Wine & Spirits	beer_and_wine
24	Cheesesteaks	cheesesteaks
25	Southern	southern
26	Vegan	vegan
27	Dive Bars	divebars
28	Diners	diners
29	Sports Bars	sportsbars
30	Russian	russian
31	Juice Bars & Smoothies	juicebars
32	Gastropubs	gastropubs
33	Barbeque	bbq
34	Ramen	ramen
35	Vegetarian	vegetarian
36	Venues & Event Spaces	venues
37	Bakeries	bakeries
38	Cajun/Creole	cajun
39	Wine Bars	wine_bars
40	Salad	salad
41	Seafood	seafood
42	Cafes	cafes
43	Steakhouses	steak
44	Middle Eastern	mideastern
45	Burgers	burgers
46	Bowling	bowling
47	Jazz & Blues	jazzandblues
48	Cocktail Bars	cocktailbars
49	Comfort Food	comfortfood
50	Thai	thai
51	Italian	italian
52	Portuguese	portuguese
53	Bars	bars
54	Mexican	mexican
55	Soup	soup
56	American (Traditional)	tradamerican
57	Mediterranean	mediterranean
58	Japanese	japanese
59	Food Trucks	foodtrucks
60	Asian Fusion	asianfusion
61	Delis	delis
62	Halal	halal
63	Hot Dogs	hotdog
64	Polish	polish
65	Soul Food	soulfood
\.


--
-- Name: categories_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('categories_category_id_seq', 65, true);


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: user
--

COPY favorites (favorite_id, restaurant_id, user_id) FROM stdin;
1	68	1
2	92	1
\.


--
-- Name: favorites_favorite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('favorites_favorite_id_seq', 2, true);


--
-- Data for Name: restaurant_categories; Type: TABLE DATA; Schema: public; Owner: user
--

COPY restaurant_categories (restaurant_category_id, restaurant_id, category_id) FROM stdin;
1	1	10
2	1	60
3	1	4
4	2	25
5	2	4
6	3	54
7	3	8
8	4	56
9	4	64
10	5	53
11	5	32
12	6	41
13	6	58
14	6	60
15	7	51
16	7	22
17	8	4
18	8	21
19	8	41
20	9	56
21	9	54
22	10	13
23	10	54
24	11	4
25	11	10
26	11	12
27	12	45
28	12	12
29	13	37
30	13	42
31	14	4
32	14	10
33	15	42
34	16	41
35	16	8
36	16	54
37	17	16
38	17	51
39	18	16
40	18	12
41	18	40
42	19	54
43	20	65
44	21	15
45	21	45
46	22	58
47	22	5
48	23	50
49	23	51
50	23	49
51	24	19
52	25	56
53	25	21
54	26	53
55	26	1
56	27	22
57	27	12
58	27	10
59	28	12
60	28	40
61	28	61
62	29	63
63	29	35
64	29	56
65	30	31
66	30	8
67	30	26
68	31	7
69	32	22
70	32	12
71	32	7
72	33	41
73	33	4
74	33	53
75	34	22
76	34	45
77	35	9
78	35	4
79	35	43
80	36	22
81	36	12
82	37	45
83	37	28
84	37	52
85	38	27
86	38	56
87	39	37
88	39	12
89	39	4
90	40	16
91	40	51
92	40	39
93	41	22
94	41	12
95	42	46
96	42	10
97	42	48
98	43	11
99	43	59
100	44	42
101	44	26
102	45	4
103	45	53
104	46	27
105	46	56
106	46	41
107	47	12
108	48	54
109	48	4
110	49	41
111	50	17
112	50	14
113	50	34
114	51	4
115	51	36
116	52	51
117	52	10
118	52	42
119	53	56
120	53	33
121	54	16
122	54	62
123	54	12
124	55	43
125	55	41
126	55	4
127	56	38
128	56	25
129	56	4
130	57	26
131	57	35
132	57	8
133	58	42
134	59	45
135	59	28
136	60	4
137	60	10
138	61	59
139	61	45
140	61	20
141	62	4
142	63	4
143	63	53
144	63	42
145	64	16
146	65	51
147	65	16
148	66	12
149	66	60
150	67	54
151	68	16
152	69	12
153	69	22
154	70	22
155	70	42
156	70	10
157	71	16
158	72	4
159	73	35
160	73	31
161	73	22
162	74	57
163	74	7
164	74	51
165	75	16
166	75	44
167	76	30
168	76	18
169	77	22
170	77	28
171	78	29
172	78	56
173	79	29
174	79	4
175	80	54
176	81	50
177	81	60
178	81	3
179	82	56
180	82	40
181	82	55
182	83	33
183	84	51
184	84	47
185	85	14
186	85	60
187	85	12
188	86	26
189	86	35
190	86	10
191	87	61
192	87	23
193	88	2
194	88	38
195	88	7
196	89	33
197	89	32
198	90	39
199	90	4
200	90	5
201	91	22
202	91	6
203	91	12
204	92	10
205	92	53
206	93	12
207	93	24
208	93	51
209	94	56
210	94	10
211	94	8
\.


--
-- Name: restaurant_categories_restaurant_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('restaurant_categories_restaurant_category_id_seq', 211, true);


--
-- Data for Name: restaurants; Type: TABLE DATA; Schema: public; Owner: user
--

COPY restaurants (restaurant_id, name, address, phone, yelp_phone, yelp_id, yelp_url, yelp_img_url, yelp_rating, yelp_rating_img, yelp_review_count, lat, lng) FROM stdin;
1	Kitchen Story	3499 16th St	(415) 525-4905	+14155254905	kitchen-story-san-francisco	http://www.yelp.com/biz/kitchen-story-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/f8Q9kkvApHfKyX4dcdeTEA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	1511	37.7643545000000032	-122.430867599999999
2	Hops & Hominy	1 Tillman Pl	(415) 373-6341	+14153736341	hops-and-hominy-san-francisco	http://www.yelp.com/biz/hops-and-hominy-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/YimILnyCQ8hgbwWgVptvhA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	1232	37.7892737258643976	-122.405591253967003
3	Nopalio	306 Broderick St	(415) 437-0303	+14154370303	nopalito-san-francisco	http://www.yelp.com/biz/nopalito-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/6EEKR45JrUk01e0fjJaHxQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	1447	37.7734353009900019	-122.438993048013998
4	Stuffed	2788 Mission St	(415) 642-1069	+14156421069	stuffed-san-francisco	http://www.yelp.com/biz/stuffed-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/y7wpm6IkqUOeAou9jO9HYw/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	158	37.7525270730257034	-122.418565526604993
5	The Monk's Kettle	3141 16th St	(415) 865-9523	+14158659523	the-monks-kettle-san-francisco	http://www.yelp.com/biz/the-monks-kettle-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/47kA45l9yNMMPg1P_qbCGw/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	1877	37.7647290879634028	-122.422974908840004
6	Skool	1725 Alameda St	(415) 255-8800	+14152558800	skool-san-francisco	http://www.yelp.com/biz/skool-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/47i057bRXAm_sIvA2obD5A/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	1122	37.7685096967036031	-122.402136325835997
7	Piccino	1001 Minnesota St	(415) 824-4224	+14158244224	piccino-san-francisco	http://www.yelp.com/biz/piccino-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/k1otgI61sT1quKq0WmYafQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	1037	37.7576219999999978	-122.389915000000002
8	Mason Pacific	1001 Minnesota St	(415) 374-7185	+14153747185	mason-pacific-san-francisco	http://www.yelp.com/biz/mason-pacific-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/VBrCdy0JkvPU8syAWNLlSw/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	281	37.7966610000000003	-122.411580999999998
9	Martita's Kitchen	2560 Marin St	(415) 282-1103	+14152821103	martitas-kitchen-san-francisco	http://www.yelp.com/biz/martitas-kitchen-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/XVtJHfK_sAORDJjWnDR-Kg/ms.jpg	5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/c7623205d5cd/ico/stars/v1/stars_small_5.png	9	37.7486014583115974	-122.403273010353004
10	Poc-Chuc	2886 16th St	(415) 558-1583	+14155581583	poc-chuc-san-francisco	http://www.yelp.com/biz/poc-chuc-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/8bl3apuKlLxnC2ejhar_DQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	454	37.7656429999999972	-122.417139000000006
11	Outerlands	4001 Judah St	(415) 661-6140	+14156616140	outerlands-san-francisco	http://www.yelp.com/biz/outerlands-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/dUHPpeIsICnTpq3BiUF0QQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	1586	37.76025390625	-122.505020141602003
12	Dusty Buns Bistro	11 Division St	(415) 895-2867	+14158952867	dusty-buns-bistro-san-francisco	http://www.yelp.com/biz/dusty-buns-bistro-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/ZLbbcpC-3FCMTixF6JX6_A/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	77	37.7697060460472969	-122.402419298886997
13	Craftsman and Wolves	746 Valencia St	(415) 913-7713	+14159137713	craftsman-and-wolves-san-francisco	http://www.yelp.com/biz/craftsman-and-wolves-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/GB43EslET15GLWccRLQroQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	946	37.7609695000000016	-122.421820600000004
14	Olea	1494 California St	(415) 202-8521	+14152028521	olea-san-francisco	http://www.yelp.com/biz/olea-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/xt4ZlKVeVBOhtwVgZqsc3w/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	762	37.790930000000003	-122.418931299999997
15	iCafe San Francisco	57 Walter U Lum Pl	(415) 392-2682	+14153922682	icafe-san-francisco-san-francisco-2	http://www.yelp.com/biz/icafe-san-francisco-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/zqDIPrS2s1OI2lvtIDgYGw/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	72	37.7950868294761975	-122.405393782912995
16	Pacific Catch	2027 Chestnut St	(415) 440-1950	+14154401950	pacific-catch-san-francisco	http://www.yelp.com/biz/pacific-catch-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/LUy6Q6DoPq7tKUPR9l7LWg/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	1305	37.8005700000000004	-122.436520000000002
17	Pizzeria Delfina	3611 18th St	(415) 437-6800	+14154376800	pizzeria-delfina-san-francisco	http://www.yelp.com/biz/pizzeria-delfina-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/4igaS1g28brlAeA3_pOFsQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	2045	37.7613600000000034	-122.424180000000007
18	All Good Pizza	1605 Jerrold Ave	(415) 933-9384	+14159339384	all-good-pizza-san-francisco	http://www.yelp.com/biz/all-good-pizza-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/xMwVf8glzvtwbemKrJsCYg/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	144	37.7390444999999985	-122.389750800000002
19	Tacolicious	741 Valencia St	(415) 649-6077	+14156496077	tacolicious-san-francisco-7	http://www.yelp.com/biz/tacolicious-san-francisco-7?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/VNYFLgm4zxHRRcenhsTKLQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	979	37.7605904999999993	-122.421380200000002
20	Soul Food City	403 Eddy St	(415) 441-1976	+14154411976	soul-food-city-san-francisco-2	http://www.yelp.com/biz/soul-food-city-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/-Po9LpV63Bcwxb8E9xAtPQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	38	37.7837370000000021	-122.414300699999998
21	Tanguito	2850 Jones St	(415) 577-4223	+14155774223	tanguito-san-francisco	http://www.yelp.com/biz/tanguito-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/-3mUK1XJ0GSnhEvC4HtQZA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	439	37.8076140000000009	-122.417203000000001
22	Izakaya Rintaro	82 14th St	(415) 589-7022	+14155897022	izakaya-rintaro-san-francisco	http://www.yelp.com/biz/izakaya-rintaro-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/Yh4qfUbp6rLvIzuqaN0nVA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	157	37.768814086914098	-122.415107727050994
23	Thoughts Style Cuisine Showroom	139 8th St	(415) 252-7919	+14152527919	thoughts-style-cuisine-showroom-san-francisco	http://www.yelp.com/biz/thoughts-style-cuisine-showroom-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/9x7QRO1EHg2p0GGQlaXaIg/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	37	37.7771759033202983	-122.412688806652994
24	FOB Kitchen	2351 Mission St	(415) 756-9844	+14157569844	fob-kitchen-san-francisco-4	http://www.yelp.com/biz/fob-kitchen-san-francisco-4?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/mqwWuMKZbO5QAnXCdULGNg/ms.jpg	5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/c7623205d5cd/ico/stars/v1/stars_small_5.png	17	37.759210000000003	-122.41892
25	Batter Up	888 Geneva Ave	(415) 205-6032	+14152056032	batter-up-san-francisco	http://www.yelp.com/biz/batter-up-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/SEITYc1YzyGyPjQOFN1d2A/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	237	37.7166905999999997	-122.441376300000002
26	El Capitan	1123 Folsom St	(415) 525-3676	+14155253676	el-capitan-san-francisco	http://www.yelp.com/biz/el-capitan-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/1QyeOldl2GeHcpDXhuRt3A/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	64	37.7761500000000012	-122.408320000000003
27	Cafe Me	500 Washington St	(415) 288-8628	+14152888628	cafe-me-san-francisco-2	http://www.yelp.com/biz/cafe-me-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/refB45MOelMzdDtdHsr1Hg/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	209	37.7958367325659026	-122.401855113180005
28	The Sandwich Spot	3213 Pierce St	(415) 829-2587	+14158292587	the-sandwich-spot-san-francisco-2	http://www.yelp.com/biz/the-sandwich-spot-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/wjARDK8-qObuP5tnmRMrdQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	490	37.7997036480886024	-122.439576733921001
29	Underdog	1634 Irving St	(415) 665-8881	+14156658881	underdog-san-francisco	http://www.yelp.com/biz/underdog-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/2aI8ohpEyqyzW6UL5BhUzA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	754	37.7637769999999975	-122.475703999999993
30	Elixiria	25 Beale St	(628) 444-3149	+16284443149	elixiria-san-francisco	http://www.yelp.com/biz/elixiria-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/Vs1cl8ZO9WM9JqmcrHXXaQ/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	57	37.7921996265650009	-122.396966367960005
31	Castagna	2015 Chestnut St	(415) 440-4290	+14154404290	castagna-san-francisco	http://www.yelp.com/biz/castagna-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/Eb9pT_mgkZYxF5dqqdQ29A/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	199	37.8005500000000012	-122.436499999999995
32	Le Cafe du Soleil	200 Fillmore St	(415) 934-8637	+14159348637	le-cafe-du-soleil-san-francisco-3	http://www.yelp.com/biz/le-cafe-du-soleil-san-francisco-3?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/gQmv87RkQGuNpWHJL04OAQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	615	37.7713499999999982	-122.430086000000003
33	Mission Rock Resort	817 Terry Francois Blvd	(415) 701-7625	+14157017625	mission-rock-resort-san-francisco-2	http://www.yelp.com/biz/mission-rock-resort-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/f8yzVkhKI5AXtToDMl9ttA/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	469	37.7653970834926014	-122.386461496352993
34	Cafe Zazo	64 14th St	(415) 626-5555	+14156265555	cafe-zazo-san-francisco	http://www.yelp.com/biz/cafe-zazo-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/AYYxgntDzIVvC8rOZkPGlQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	148	37.7686920000000015	-122.414837599999998
35	Belcampo Meat Co.	1998 Polk St	(415) 660-5573	+14156605573	belcampo-meat-co-san-francisco	http://www.yelp.com/biz/belcampo-meat-co-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/mMlO4X4AlssjWBz7wTBD4w/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	125	37.7948214667231994	-122.421481423079996
36	Jackson Place Cafe	633 Battery St	(415) 225-4891	+14152254891	jackson-place-cafe-san-francisco	http://www.yelp.com/biz/jackson-place-cafe-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/PF2a7EPR45EkvRK0KWRUxg/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	165	37.7971250333250026	-122.401331702377007
37	Grubstake	1525 Pine St	(415) 673-8268	+14156738268	grubstake-san-francisco	http://www.yelp.com/biz/grubstake-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/NToCb4CsHmnSQpn3cJbhuA/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	912	37.7895256999999987	-122.420865899999995
38	Bender's Bar and Grill	806 S Van Ness Ave	(415) 824-1800	+14158241800	benders-bar-and-grill-san-francisco	http://www.yelp.com/biz/benders-bar-and-grill-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/FsjckhTp_nbLzhL-qH15PA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	394	37.7601948000000007	-122.417180400000007
39	The Golden West	8 Trinity Pl	(415) 216-6443	+14152166443	the-golden-west-san-francisco	http://www.yelp.com/biz/the-golden-west-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/P95OWNhZJRlvQxmJkpErTA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	313	37.7901306999999989	-122.402604800000006
40	Acquolina	1600 Stockton St	(415) 781-0331	+14157810331	acquolina-san-francisco	http://www.yelp.com/biz/acquolina-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/jtakl4ObMhb5pLmtJavKCw/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	112	37.8006138590171972	-122.409087941050998
41	Luna's Coffee House	1101 Potrero Ave	(415) 710-3066	+14157103066	lunas-coffee-house-san-francisco-3	http://www.yelp.com/biz/lunas-coffee-house-san-francisco-3?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/MW0V_1qN-CKNAqK0bF40Eg/ms.jpg	5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/c7623205d5cd/ico/stars/v1/stars_small_5.png	18	37.7542538394443028	-122.406396576686006
42	Mission Bowling Club	3176 17th St	(415) 863-2695	+14158632695	mission-bowling-club-san-francisco	http://www.yelp.com/biz/mission-bowling-club-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/yuPSZ_nDPoFOylFYYcEvCQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	435	37.7637146469497011	-122.416815797940998
43	Curry Up Now	225 Bush St	(415) 735-3667	+14157353667	curry-up-now-san-francisco-6	http://www.yelp.com/biz/curry-up-now-san-francisco-6?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/WPhir3ciiw-HkHImKE-ypQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	829	37.7910766391999999	-122.401035453000006
44	Nourish Cafe	189 6th Ave	(415) 571-8780	+14155718780	nourish-cafe-san-francisco	http://www.yelp.com/biz/nourish-cafe-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/AIriJRTtzYdtW1aN5knHgQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	111	37.7852674573659968	-122.464657276869005
45	Presidio Social Club	563 Ruger St	(415) 885-1888	+14158851888	presidio-social-club-san-francisco	http://www.yelp.com/biz/presidio-social-club-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/LH9ouGM_dVh15o4bwuAq8w/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	887	37.7971000224352025	-122.447941750287995
46	The Ramp	855 Terry Francois St	(415) 621-2378	+14156212378	the-ramp-san-francisco	http://www.yelp.com/biz/the-ramp-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/2QlGM-NZNNQ2d-Sp7wI8Ag/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	850	37.7642598902420019	-122.386890321899998
47	Back Yard Kitchen	2760 Octavia St	(415) 655-3023	+14156553023	back-yard-kitchen-san-francisco	http://www.yelp.com/biz/back-yard-kitchen-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/3SFCDOckc30skpk_8tRoIA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	107	37.7975385636091019	-122.428763955831997
48	CHICA	120 Green St	(415) 757-0510	+14157570510	chica-san-francisco-2	http://www.yelp.com/biz/chica-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/Aa2kX7HkXiBLI4tuhK9pDw/ms.jpg	5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/c7623205d5cd/ico/stars/v1/stars_small_5.png	8	37.8005166340800969	-122.401859387754996
49	Pacific Catch	1200 9th Ave	(415) 504-6905	+14155046905	pacific-catch-san-francisco-2	http://www.yelp.com/biz/pacific-catch-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/l228qaB70fUK3BiUsJhaIQ/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	1410	37.7656700000000001	-122.466189999999997
50	Slurp Noodle Bar	469 Castro Street	(415) 553-6633	+14155536633	slurp-noodle-bar-san-francisco	http://www.yelp.com/biz/slurp-noodle-bar-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/1YU8PINmK8oiMsX1rVHbbQ/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	262	37.7614899000000008	-122.434692400000003
51	Aracely Cafe	401 13th St	(415) 985-7117	+14159857117	aracely-cafe-san-francisco-2	http://www.yelp.com/biz/aracely-cafe-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/29jnnCIlsQMw8dKTqFYeDg/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	56	37.8279878000000025	-122.373779900000002
52	Rose's Cafe	2298 Union St	(415) 775-2200	+14157752200	roses-cafe-san-francisco	http://www.yelp.com/biz/roses-cafe-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/zoDQy7BGKdZ3M3_ejEUYaw/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	750	37.7970699999999979	-122.436989999999994
53	Smokin' Warehouse Barbecue	1465 Carroll Ave	(415) 648-8881	+14156488881	smokin-warehouse-barbecue-san-francisco-4	http://www.yelp.com/biz/smokin-warehouse-barbecue-san-francisco-4?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/Qy9VJB32HfNbgD7S8yvOUg/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	128	37.723281860351598	-122.390907287597997
54	Ali's Pizzeria	407 Ellis St	(415) 872-9333	+14158729333	alis-pizzeria-san-francisco-3	http://www.yelp.com/biz/alis-pizzeria-san-francisco-3?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/jmmo9P7TUqqSsC7yoVY0jA/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	48	37.7847215000000034	-122.413026299999999
55	EPIC Steak	369 The Embarcadero	(415) 369-9955	+14153699955	epic-steak-san-francisco	http://www.yelp.com/biz/epic-steak-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/18x1da38lbuafhXXeY62jg/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	1557	37.790829305773002	-122.389254758020002
56	The Elite Cafe	2049 Fillmore St	(415) 346-8400	+14153468400	the-elite-cafe-san-francisco	http://www.yelp.com/biz/the-elite-cafe-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/KcROracQC6l0SW3aG0jRpg/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	1028	37.7885818481445028	-122.434028625487997
57	3 Potato 4	2800 Leavenworth St	(978) 317-0502	+19783170502	3-potato-4-san-francisco-2	http://www.yelp.com/biz/3-potato-4-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/oKBuv_GLz0P5ypsKNXogEQ/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	59	37.8074142999999978	-122.418582299999997
58	Bread & Butter Cafe	1901 Hayes St	(415) 221-8700	+14152218700	bread-and-butter-cafe-san-francisco-2	http://www.yelp.com/biz/bread-and-butter-cafe-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/w_oGsb3ToN-bOvMJyljLnA/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	67	37.7735900999999998	-122.447807299999994
59	Gott's Roadside	1 Ferry Bldg	(415) 318-3423	+14153183423	gotts-roadside-san-francisco-2	http://www.yelp.com/biz/gotts-roadside-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/zw9WnjKw8caryBq4by6fIA/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	2152	37.7960849485032	-122.394304275512994
60	Triptych	1155 Folsom St	(415) 703-0557	+14157030557	triptych-san-francisco	http://www.yelp.com/biz/triptych-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/d42ZLzv1jNC6aTBAbiWY3w/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	928	37.7757166000000026	-122.408984899999993
61	Slider Shack	400 Howard St	(415) 672-2902	+14156722902	slider-shack-san-francisco	http://www.yelp.com/biz/slider-shack-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/0DWs7ZgoWKfT7awpm0tWvw/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	127	37.7891526000000013	-122.395792799999995
62	The Brixton	2140 Union St	(415) 409-1114	+14154091114	the-brixton-san-francisco	http://www.yelp.com/biz/the-brixton-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/TzFrUee-FC6ADueD12pBpw/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	600	37.797254249453502	-122.434554174542001
63	Cafe Flore	2298 Market St	(415) 621-8579	+14156218579	café-flore-san-francisco-3	http://www.yelp.com/biz/caf%C3%A9-flore-san-francisco-3?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/xkZEd7mvMhLWbriVFvJVEw/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	881	37.7646560668945028	-122.432945251465
64	Firetrail Pizza	428 11th St	(415) 967-1363	+14159671363	firetrail-pizza-san-francisco	http://www.yelp.com/biz/firetrail-pizza-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/1OIsJrXsdwBWNE9dX10NNg/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	75	37.7697750000000028	-122.411918
65	Calzone's Pizza Cucina	430 Columbus Ave	(415) 397-3600	+14153973600	calzones-pizza-cucina-san-francisco	http://www.yelp.com/biz/calzones-pizza-cucina-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/CwU02iEG7W6RAIyt39AX-A/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	1099	37.7990319999999969	-122.408174299999999
66	Spice Kit	428 11th St	(415) 882-4581	+14158824581	spice-kit-san-francisco	http://www.yelp.com/biz/spice-kit-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/8j9E4tQ149nDe3YoRGV5ZA/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	456	37.7885039084164021	-122.395379701140996
67	La Urbana	661 Divisadero St	(415) 440-4500	+14154404500	la-urbana-san-francisco	http://www.yelp.com/biz/la-urbana-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/1whIEo0j4a6K9mqtQ0VWhw/ms.jpg	3	http://s3-media3.fl.yelpcdn.com/assets/2/www/img/902abeed0983/ico/stars/v1/stars_small_3.png	344	37.7757672498169015	-122.438140611628
68	Firehouse Pizzeria	6001 California St	(415) 221-7603	+14152217603	firehouse-pizzeria-san-francisco	http://www.yelp.com/biz/firehouse-pizzeria-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/Kk7jm25H3uaWKo0erqSpTQ/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	197	37.7837753295898011	-122.481964111327997
69	Alamo Square Cafe	711 Fillmore St	(415) 447-8636	+14154478636	alamo-square-cafe-san-francisco	http://www.yelp.com/biz/alamo-square-cafe-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/UB2gCtr8FtsUSH-kfyO8FQ/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	81	37.7760594000000012	-122.431376599999993
70	The Station SF	596 Pacific Ave	(415) 291-0690	+14152910690	the-station-sf-san-francisco	http://www.yelp.com/biz/the-station-sf-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/285ycFI8XHJp5R2Wcn9rPw/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	220	37.7972297999999967	-122.405151399999994
71	Pizzeria Avellino	2769 Lombard St	(415) 776-2500	+14157762500	pizzeria-avellino-san-francisco	http://www.yelp.com/biz/pizzeria-avellino-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/A9UmJguy1SZkSTcZsZxBWA/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	194	37.7983059000000026	-122.447070999999994
72	Sessions at the Presidio	1 Letterman Dr	(415) 655-9413	+14156559413	sessions-at-the-presidio-san-francisco	http://www.yelp.com/biz/sessions-at-the-presidio-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/rMMDEUo8ZHl_4Roi8l86NA/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	110	37.7992754582365009	-122.447810808984002
73	The Plant Cafe Organic	3352 Steiner St	(415) 931-2777	+14159312777	the-plant-café-organic-san-francisco-10	http://www.yelp.com/biz/the-plant-caf%C3%A9-organic-san-francisco-10?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/Ln3ykwO-c3xajNF6DUx2Mg/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	815	37.8003396729648031	-122.437772130688003
74	Melody	3401 Mission St	(415) 310-8412	+14153108412	melody-san-francisco	http://www.yelp.com/biz/melody-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/DQQuPNInxwnwvryap1VTrg/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	199	37.7419548034667969	-122.421905517577997
75	Fresco Pizza Shawarma	1338 Polk St	(415) 440-4410	+14154404410	fresco-pizza-shawarma-san-francisco-4	http://www.yelp.com/biz/fresco-pizza-shawarma-san-francisco-4?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/pVuNukKW1AFVDnBDYBmdYg/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	175	37.7893199000000024	-122.420199999999994
76	Katia's Russian Tea Room	600 5th Ave	(415) 668-9292	+14156689292	katias-russian-tea-room-san-francisco	http://www.yelp.com/biz/katias-russian-tea-room-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/bQD6ZvhZRqc2uVrYktxCTg/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	210	37.7771499999999989	-122.462689999999995
77	It's Tops Coffee Shop	1801 Market St	(415) 431-6395	+14154316395	its-tops-coffee-shop-san-francisco	http://www.yelp.com/biz/its-tops-coffee-shop-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/Q_MpQ1Ir7wGGam2RaCv1cw/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	389	37.7714306000000022	-122.423638800000006
78	Public House	24 Willie Mays Plz	(415) 644-0240	+14156440240	public-house-san-francisco	http://www.yelp.com/biz/public-house-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/72Avp41TrmmxJCvzqSiO5g/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	411	37.7781299999999973	-122.390810000000002
79	Connecticut Yankee	100 Connecticut St	(415) 552-4440	+14155524440	connecticut-yankee-san-francisco	http://www.yelp.com/biz/connecticut-yankee-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media1.fl.yelpcdn.com/bphoto/9M4vu9y2t5Z8UXwtIm0FwA/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	367	37.7650170000000003	-122.397419999999997
80	Bonita Taqueria Y Rotisserie	2257 Chestnut St	(415) 801-5599	+14158015599	bonita-taqueria-y-rotisserie-san-francisco	http://www.yelp.com/biz/bonita-taqueria-y-rotisserie-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/-0_K6l1oZnlC219K7OUe6Q/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	115	37.8000984000000031	-122.440399200000002
81	Osha Thai	311 3rd St	(415) 896-6742	+14158966742	osha-thai-san-francisco-13	http://www.yelp.com/biz/osha-thai-san-francisco-13?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/RTZJzHfL5lPlOF6Fz-b6eg/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	692	37.7837225999999973	-122.398650500000002
82	Tender Greens	266 King St	(415) 230-3141	+14152303141	tender-greens-san-francisco-4	http://www.yelp.com/biz/tender-greens-san-francisco-4?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/5msAaVS5sEC31_kYxWR-Wg/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	110	37.7772819013067007	-122.393357740114993
83	Black Bark BBQ	1325 Fillmore St	(415) 848-9055	+14158489055	black-bark-bbq-san-francisco	http://www.yelp.com/biz/black-bark-bbq-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/cOBwF1sn-9uLmtL7Z-ywow/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	59	37.781671099999997	-122.432541799999996
84	Rose Pistola	532 Columbus Ave	(415) 399-0499	+14153990499	rose-pistola-san-francisco	http://www.yelp.com/biz/rose-pistola-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/IkrBClcwHcBsBJhzGPSq6A/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	705	37.800060000000002	-122.409440000000004
85	Stone Korean Kitchen	4 Embarcadero Ctr	(415) 839-4070	+14158394070	stone-korean-kitchen-san-francisco-2	http://www.yelp.com/biz/stone-korean-kitchen-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/PXWLRRbjujdLaPUxxT44nQ/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	646	37.7950870000000023	-122.396135000000001
86	Peasant Pies	303 Sacramento St	(415) 730-1972	+14157301972	peasant-pies-san-francisco-4	http://www.yelp.com/biz/peasant-pies-san-francisco-4?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/9IchkAh7UlvXLtWFx16rYg/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	38	37.7942097207689969	-122.399407178163997
87	Golden Gate Market Deli & Liquor	2767 Lombard St	(415) 346-6052	+14153466052	golden-gate-market-deli-and-liquor-san-francisco-2	http://www.yelp.com/biz/golden-gate-market-deli-and-liquor-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/OWEvsOKlBLWWb_eU488Y8A/ms.jpg	4.5	http://s3-media2.fl.yelpcdn.com/assets/2/www/img/a5221e66bc70/ico/stars/v1/stars_small_4_half.png	62	37.798349199999997	-122.4471147
88	Balancoire	2565 Mission St	(415) 920-0577	+14159200577	balancoire-san-francisco-3	http://www.yelp.com/biz/balancoire-san-francisco-3?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/E4-H4Ny-2-h0xz_K6NWIng/ms.jpg	3	http://s3-media3.fl.yelpcdn.com/assets/2/www/img/902abeed0983/ico/stars/v1/stars_small_3.png	119	37.7560939999999974	-122.418453999999997
89	Hood Grub @ The Broken Record	1166 Geneva Ave	(415) 347-7811	+14153477811	hood-grub-the-broken-record-san-francisco	http://www.yelp.com/biz/hood-grub-the-broken-record-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/UHPUJSTV32we9CLX_I0_Sw/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	56	37.7143896999999981	-122.436924200000007
90	Etcetera Wine Bar	795 Valencia St	(415) 926-5477	+14159265477	etcetera-wine-bar-san-francisco	http://www.yelp.com/biz/etcetera-wine-bar-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/puMko6eMp3mKcJbBVGXmGA/ms.jpg	4	http://s3-media4.fl.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png	239	37.7603041380643987	-122.421362400055003
91	All Star Cafe	1500 Market St	(415) 252-9888	+14152529888	all-star-cafe-san-francisco	http://www.yelp.com/biz/all-star-cafe-san-francisco?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/yntdQnYHwaXyqD0FlJKZ7A/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	89	37.7752456665038991	-122.419532775879006
92	Ovok	2295 Market St	(415) 431-7700	+14154317700	ovok-san-francisco-6	http://www.yelp.com/biz/ovok-san-francisco-6?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media4.fl.yelpcdn.com/bphoto/4g_HV1pugzZGahdpNLCxJg/ms.jpg	3	http://s3-media3.fl.yelpcdn.com/assets/2/www/img/902abeed0983/ico/stars/v1/stars_small_3.png	24	37.7643334865569997	-122.432760447264002
93	Merigan Sub Shop	636 2nd St	(415) 536-2991	+14155362991	merigan-sub-shop-san-francisco-2	http://www.yelp.com/biz/merigan-sub-shop-san-francisco-2?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media2.fl.yelpcdn.com/bphoto/RhK7SQqZ_4028erHO6fRRw/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	156	37.7813579000000033	-122.391486799999996
94	Beach Street Grill	380 Beach St	(415) 867-1711	+14158671711	beach-street-grill-san-francisco-7	http://www.yelp.com/biz/beach-street-grill-san-francisco-7?utm_campaign=yelp_api&utm_medium=api_v2_phone_search&utm_source=nA0seEO0XHY1u3dWpKrAjA	http://s3-media3.fl.yelpcdn.com/bphoto/cxkeWlXY9BHPUwqBED2Tcg/ms.jpg	3.5	http://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png	217	37.8074099019557011	-122.415331071764001
\.


--
-- Name: restaurants_restaurant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('restaurants_restaurant_id_seq', 94, true);


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: user
--

COPY reviews (review_id, restaurant_id, user_id, rating, body) FROM stdin;
\.


--
-- Name: reviews_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('reviews_review_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY users (user_id, username, password, fname, lname) FROM stdin;
1	balloonicorn	asdf	Balloon	Icorn
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('users_user_id_seq', 1, true);


--
-- Data for Name: yelp_reviews; Type: TABLE DATA; Schema: public; Owner: user
--

COPY yelp_reviews (yelp_review_id, yelp_id, body) FROM stdin;
\.


--
-- Name: yelp_reviews_yelp_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('yelp_reviews_yelp_review_id_seq', 1, false);


--
-- Name: categories_alias_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_alias_key UNIQUE (alias);


--
-- Name: categories_category_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_category_key UNIQUE (category);


--
-- Name: categories_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (favorite_id);


--
-- Name: restaurant_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY restaurant_categories
    ADD CONSTRAINT restaurant_categories_pkey PRIMARY KEY (restaurant_category_id);


--
-- Name: restaurants_phone_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY restaurants
    ADD CONSTRAINT restaurants_phone_key UNIQUE (phone);


--
-- Name: restaurants_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY restaurants
    ADD CONSTRAINT restaurants_pkey PRIMARY KEY (restaurant_id);


--
-- Name: restaurants_yelp_id_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY restaurants
    ADD CONSTRAINT restaurants_yelp_id_key UNIQUE (yelp_id);


--
-- Name: restaurants_yelp_img_url_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY restaurants
    ADD CONSTRAINT restaurants_yelp_img_url_key UNIQUE (yelp_img_url);


--
-- Name: restaurants_yelp_phone_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY restaurants
    ADD CONSTRAINT restaurants_yelp_phone_key UNIQUE (yelp_phone);


--
-- Name: restaurants_yelp_url_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY restaurants
    ADD CONSTRAINT restaurants_yelp_url_key UNIQUE (yelp_url);


--
-- Name: reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: yelp_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY yelp_reviews
    ADD CONSTRAINT yelp_reviews_pkey PRIMARY KEY (yelp_review_id);


--
-- Name: yelp_reviews_yelp_id_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY yelp_reviews
    ADD CONSTRAINT yelp_reviews_yelp_id_key UNIQUE (yelp_id);


--
-- Name: favorites_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY favorites
    ADD CONSTRAINT favorites_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id);


--
-- Name: favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY favorites
    ADD CONSTRAINT favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: restaurant_categories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY restaurant_categories
    ADD CONSTRAINT restaurant_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES categories(category_id);


--
-- Name: restaurant_categories_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY restaurant_categories
    ADD CONSTRAINT restaurant_categories_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id);


--
-- Name: reviews_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY reviews
    ADD CONSTRAINT reviews_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id);


--
-- Name: reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: yelp_reviews_yelp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY yelp_reviews
    ADD CONSTRAINT yelp_reviews_yelp_id_fkey FOREIGN KEY (yelp_id) REFERENCES restaurants(yelp_id);


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

