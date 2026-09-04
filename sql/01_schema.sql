-- PostgreSQL warehouse initialization.
-- Run from the repository root so psql can resolve data/processed/fights.csv.

BEGIN;

DROP TABLE IF EXISTS public.fact_fight CASCADE;
DROP TABLE IF EXISTS public.dim_fighter CASCADE;
DROP TABLE IF EXISTS public.dim_finish CASCADE;
DROP TABLE IF EXISTS public.dim_type CASCADE;
DROP TABLE IF EXISTS public.dim_event CASCADE;
DROP TABLE IF EXISTS public.dim_date CASCADE;
DROP TABLE IF EXISTS public.staging_fight CASCADE;

-- ============================================================
-- 1) STAGING TABLE
-- ============================================================
CREATE TABLE public.staging_fight (
  r_name                     TEXT,
  b_name                     TEXT,
  event                      TEXT,
  date                       DATE,
  month                      INTEGER,
  year                       INTEGER,
  gender                     TEXT,
  city                       TEXT,
  state                      TEXT,
  country                    TEXT,
  referee                    TEXT,
  winner                     TEXT,
  finish                     TEXT,
  finishdetails              TEXT,
  finishround                INTEGER,
  titlebout                  BOOLEAN,
  weightclass                TEXT,
  numberofrounds             INTEGER,
  emptyarena                 BOOLEAN,
  heightdif                  REAL,
  agedif                     REAL,
  reachdif                   REAL,
  r_odds                     INTEGER,
  r_age                      INTEGER,
  r_age_range                TEXT,
  r_stance                   TEXT,
  b_odds                     INTEGER,
  b_age                      INTEGER,
  b_age_range                TEXT,
  b_stance                   TEXT,
  r_avgkd                    REAL,
  r_avgsigstratt             REAL,
  r_avgsigstrlanded          REAL,
  r_avgtdatt                 REAL,
  r_avgtdlanded              REAL,
  r_avgsubatt                REAL,
  "r_avgctrltime(seconds)"   REAL,
  b_avgkd                    REAL,
  b_avgsigstratt             REAL,
  b_avgsigstrlanded          REAL,
  b_avgtdatt                 REAL,
  b_avgtdlanded              REAL,
  b_avgsubatt                REAL,
  "b_avgctrltime(seconds)"   REAL,
  r_undefeated               BOOLEAN,
  b_undefeated               BOOLEAN,
  r_wc_ranked                BOOLEAN,
  r_pfp_ranked               BOOLEAN,
  b_wc_ranked                BOOLEAN,
  b_pfp_ranked               BOOLEAN,
  r_champion                 BOOLEAN,
  b_champion                 BOOLEAN
);

-- ============================================================
-- CSV LOADING
-- ============================================================
\copy public.staging_fight FROM 'data/processed/fights.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"')

ALTER TABLE public.staging_fight
  ADD COLUMN stg_id SERIAL PRIMARY KEY;

-- ============================================================
-- 2) DIMENSIONS
-- ============================================================

-- DIM DATE
CREATE TABLE public.dim_date (
  date_key SERIAL PRIMARY KEY,
  date     DATE NOT NULL UNIQUE,
  month    SMALLINT,
  year     SMALLINT
);

INSERT INTO public.dim_date(date, month, year)
SELECT DISTINCT
  s.date,
  EXTRACT(MONTH FROM s.date)::SMALLINT,
  EXTRACT(YEAR  FROM s.date)::SMALLINT
FROM public.staging_fight s
WHERE s.date IS NOT NULL;

-- DIM EVENT 
CREATE TABLE public.dim_event (
  event_key SERIAL PRIMARY KEY,
  event     TEXT NOT NULL,
  country   TEXT,
  state     TEXT,
  city      TEXT
);

INSERT INTO public.dim_event(event, country, state, city)
SELECT DISTINCT
  s.event,
  s.country,
  s.state,
  s.city
FROM public.staging_fight s
WHERE s.event IS NOT NULL;

-- DIM TYPE
CREATE TABLE public.dim_type (
  type_key       SERIAL PRIMARY KEY,
  weightclass    TEXT,
  numberofrounds INTEGER,
  titlebout      BOOLEAN,
  emptyarena     BOOLEAN
);

INSERT INTO public.dim_type(weightclass, numberofrounds, titlebout, emptyarena)
SELECT DISTINCT
  s.weightclass,
  s.numberofrounds,
  s.titlebout,
  s.emptyarena
FROM public.staging_fight s;

-- DIM FINISH 
CREATE TABLE public.dim_finish (
  finish_key    SERIAL PRIMARY KEY,
  finish        TEXT,
  finishdetails TEXT,
  finishround   INTEGER
);

INSERT INTO public.dim_finish( finish, finishdetails, finishround)
SELECT DISTINCT
  s.finish,
  s.finishdetails,
  s.finishround
FROM public.staging_fight s;

-- DIM FIGHTER 
CREATE TABLE public.dim_fighter (
  fighter_key  SERIAL PRIMARY KEY,
  stg_id       INTEGER NOT NULL REFERENCES public.staging_fight(stg_id),
  corner       CHAR(1) NOT NULL CHECK (corner IN ('R','B')),
  fighter_name TEXT NOT NULL,
  gender       TEXT,
  age          INTEGER,
  age_range    TEXT,
  stance       TEXT,
  undefeated   BOOLEAN,
  wc_ranked    BOOLEAN,
  pfp_ranked   BOOLEAN,
  champion     BOOLEAN,
  UNIQUE (stg_id, corner)
);

INSERT INTO public.dim_fighter(
  stg_id, corner, fighter_name, gender, age, age_range, stance,
  undefeated, wc_ranked, pfp_ranked, champion
)
SELECT
  s.stg_id,
  'R' AS corner,
  s.r_name,
  s.gender,
  s.r_age,
  s.r_age_range,
  s.r_stance,
  s.r_undefeated,
  s.r_wc_ranked,
  s.r_pfp_ranked,
  s.r_champion
FROM public.staging_fight s
WHERE s.r_name IS NOT NULL

UNION ALL

SELECT
  s.stg_id,
  'B' AS corner,
  s.b_name,
  s.gender,
  s.b_age,
  s.b_age_range,
  s.b_stance,
  s.b_undefeated,
  s.b_wc_ranked,
  s.b_pfp_ranked,
  s.b_champion
FROM public.staging_fight s
WHERE s.b_name IS NOT NULL;

-- ============================================================
-- 3) FACT TABLE
-- ============================================================
CREATE TABLE public.fact_fight AS
WITH base AS (
  SELECT
    s.stg_id,
    dd.date_key,
    de.event_key,
    dt.type_key,
    df.finish_key,
    fr.fighter_key AS red_fighter_key,
    fb.fighter_key AS blue_fighter_key,
    s.winner,
    s.referee,
    s.heightdif,
    s.agedif,
    s.reachdif,
    s.r_odds,
    s.b_odds,
    s.r_avgkd,
    s.b_avgkd,
    s.r_avgsigstratt,
    s.b_avgsigstratt,
    s.r_avgsigstrlanded,
    s.b_avgsigstrlanded,
    s.r_avgtdatt,
    s.b_avgtdatt,
    s.r_avgtdlanded,
    s.b_avgtdlanded,
    s.r_avgsubatt,
    s.b_avgsubatt,
    s."r_avgctrltime(seconds)" AS r_avgctrltime,
    s."b_avgctrltime(seconds)" AS b_avgctrltime
  FROM public.staging_fight s
  JOIN public.dim_date  dd ON dd.date = s.date
  JOIN public.dim_event de ON de.event = s.event
  JOIN public.dim_type  dt
    ON dt.weightclass    IS NOT DISTINCT FROM s.weightclass
   AND dt.numberofrounds IS NOT DISTINCT FROM s.numberofrounds
   AND dt.titlebout      IS NOT DISTINCT FROM s.titlebout
   AND dt.emptyarena     IS NOT DISTINCT FROM s.emptyarena
  JOIN public.dim_finish df 
    ON df.finish        IS NOT DISTINCT FROM s.finish
   AND df.finishdetails IS NOT DISTINCT FROM s.finishdetails
   AND df.finishround   IS NOT DISTINCT FROM s.finishround
  JOIN public.dim_fighter fr ON fr.stg_id = s.stg_id AND fr.corner = 'R'
  JOIN public.dim_fighter fb ON fb.stg_id = s.stg_id AND fb.corner = 'B'
)
SELECT
  ROW_NUMBER() OVER (ORDER BY stg_id) AS fight_key,
  date_key,
  event_key,
  type_key,
  finish_key,
  red_fighter_key,
  blue_fighter_key,
  winner,
  referee,
  heightdif,
  agedif,
  reachdif,
  r_odds,
  b_odds,
  r_avgkd,
  b_avgkd,
  r_avgsigstratt,
  b_avgsigstratt,
  r_avgsigstrlanded,
  b_avgsigstrlanded,
  r_avgtdatt,
  b_avgtdatt,
  r_avgtdlanded,
  b_avgtdlanded,
  r_avgsubatt,
  b_avgsubatt,
  r_avgctrltime,
  b_avgctrltime
FROM (
  SELECT DISTINCT ON (stg_id) *
  FROM base
  ORDER BY stg_id
) x
ORDER BY fight_key;

ALTER TABLE public.fact_fight ADD PRIMARY KEY (fight_key);
CREATE INDEX fact_fight_date_idx ON public.fact_fight(date_key);
CREATE INDEX fact_fight_event_idx ON public.fact_fight(event_key);
CREATE INDEX fact_fight_finish_idx ON public.fact_fight(finish_key);
CREATE INDEX fact_fight_red_fighter_idx ON public.fact_fight(red_fighter_key);
CREATE INDEX fact_fight_blue_fighter_idx ON public.fact_fight(blue_fighter_key);

COMMIT;
