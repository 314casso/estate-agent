--
-- Data for Name: estatebase_office; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_office (id, name, address) FROM stdin;
3	Дом в Анапе	Агентство недвижимости "Дом в Анапе" Офис в Анапе: улица Астраханская, дом 100, этаж 2, офис 3 тел. (86133) 3 77 97, 8 918 647 27 27, 8 961 859 97 96, dom@vanape.ru, сайт www.domnatamani.ru
2	Дом в Новороссийске	Агентство недвижимости "Дом в Новороссийске" Офис в Новороссийске: улица Анапское шоссе, д. 15, эт. 3, оф. 301, бизнес-центр "Приморский" тел. 8 918 040 94 94, 8 918 041 06 66, pochta@domvnovorossiyske.ru, сайт www.domnatamani.ru
1	Дом на Тамани	Агентство недвижимости "Дом на Тамани" Офис в Темрюке: улица Ленина, дом 180, офис 2 (86148) 5 44 55, 8 918 980 28 70, 8 906 187 74 03, dom@natamani.ru, domnatamani@yandex.ru, сайт www.domnatamani.ru
\.


--
-- Data for Name: estatebase_office_regions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY estatebase_office_regions (id, office_id, region_id) FROM stdin;
1	3	1
2	2	1
3	2	2
4	1	4
\.
