/* ============================================================
   ANALYSIS 1
   ============================================================ */

-- Q1 PER-FIGHT TABLE 
DROP TABLE IF EXISTS tmp_a2_upset_per_fight;

CREATE TEMP TABLE tmp_a2_upset_per_fight AS
SELECT
  e.country,
  e.state,
  t.numberofrounds,
  f.winner,
  f.r_odds,
  f.b_odds,
  CASE
    WHEN f.r_odds > f.b_odds THEN 'Red'
    WHEN f.b_odds > f.r_odds THEN 'Blue'
    ELSE NULL
  END AS underdog_side,
  CASE
    WHEN (f.r_odds > f.b_odds AND f.winner = 'Red')  THEN 1
    WHEN (f.b_odds > f.r_odds AND f.winner = 'Blue') THEN 1
    ELSE 0
  END AS is_upset
FROM public.fact_fight f
JOIN public.dim_event e ON e.event_key = f.event_key
JOIN public.dim_type  t ON t.type_key  = f.type_key
WHERE f.winner IN ('Red','Blue')
  AND f.r_odds IS NOT NULL
  AND f.b_odds IS NOT NULL
  AND f.r_odds <> f.b_odds;


SELECT *
FROM tmp_a2_upset_per_fight
ORDER BY country, numberofrounds
LIMIT 25;



-- Q2 ROLL-UP on country and numberofrounds
DROP TABLE IF EXISTS tmp_a2_upset_rollup;

CREATE TEMP TABLE tmp_a2_upset_rollup AS
SELECT
  COALESCE(country, 'ALL') AS country,
  COALESCE(numberofrounds::text, 'ALL') AS numberofrounds,
  COUNT(*) AS fights,
  SUM(is_upset) AS upset_count,
  ROUND(100.0 * SUM(is_upset)::numeric / NULLIF(COUNT(*),0), 2) AS upset_pct
FROM tmp_a2_upset_per_fight
GROUP BY ROLLUP (country, numberofrounds)
ORDER BY country, numberofrounds;


SELECT *
FROM tmp_a2_upset_rollup
ORDER BY country, numberofrounds;

-- Q3 PIVOT 
DROP TABLE IF EXISTS tmp_a2_upset_pivot;

CREATE TEMP TABLE tmp_a2_upset_pivot AS
SELECT
  country,
  COUNT(*) FILTER (WHERE numberofrounds = 3) AS fights_3r,
  ROUND(
    100.0 * SUM(is_upset) FILTER (WHERE numberofrounds = 3)::numeric
    / NULLIF(COUNT(*) FILTER (WHERE numberofrounds = 3), 0)
  , 2) AS upset_pct_3r,

  COUNT(*) FILTER (WHERE numberofrounds = 5) AS fights_5r,
  ROUND(
    100.0 * SUM(is_upset) FILTER (WHERE numberofrounds = 5)::numeric
    / NULLIF(COUNT(*) FILTER (WHERE numberofrounds = 5), 0)
  , 2) AS upset_pct_5r
FROM tmp_a2_upset_per_fight
GROUP BY country
HAVING COUNT(*) >= 30
ORDER BY (COUNT(*)) DESC;


SELECT *
FROM tmp_a2_upset_pivot
ORDER BY (fights_3r + fights_5r) DESC;



/* =====================================================================
   ANALYSIS 2
   ===================================================================== */

-- Q1 APPEARANCES TABLE 
DROP TABLE IF EXISTS tmp_a3_appearances;

CREATE TEMP TABLE tmp_a3_appearances AS
SELECT
  d.year,
  'R'::text AS corner,
  fr.fighter_name AS fighter,
  fr.age_range,
  CASE
    WHEN fr.champion THEN 'Champion'
    WHEN (fr.wc_ranked OR fr.pfp_ranked) THEN 'Ranked'
    ELSE 'Unranked'
  END AS rank_status,
  CASE
    WHEN fr.stance IN ('Orthodox','Southpaw','Switch') THEN fr.stance
    WHEN fr.stance IS NULL OR fr.stance = '' THEN 'Unknown'
    ELSE 'Other'
  END AS stance_group,
  f.r_avgsigstratt AS sig_att,
  f.r_avgctrltime  AS ctrl_time
FROM public.fact_fight f
JOIN public.dim_date d     ON d.date_key = f.date_key
JOIN public.dim_fighter fr ON fr.fighter_key = f.red_fighter_key

UNION ALL

SELECT
  d.year,
  'B'::text AS corner,
  fb.fighter_name AS fighter,
  fb.age_range,
  CASE
    WHEN fb.champion THEN 'Champion'
    WHEN (fb.wc_ranked OR fb.pfp_ranked) THEN 'Ranked'
    ELSE 'Unranked'
  END AS rank_status,
  CASE
    WHEN fb.stance IN ('Orthodox','Southpaw','Switch') THEN fb.stance
    WHEN fb.stance IS NULL OR fb.stance = '' THEN 'Unknown'
    ELSE 'Other'
  END AS stance_group,
  f.b_avgsigstratt AS sig_att,
  f.b_avgctrltime  AS ctrl_time
FROM public.fact_fight f
JOIN public.dim_date d     ON d.date_key = f.date_key
JOIN public.dim_fighter fb ON fb.fighter_key = f.blue_fighter_key;

SELECT *
FROM tmp_a3_appearances
ORDER BY year, rank_status, age_range, stance_group
LIMIT 25;


-- Q2 ROLL-UP (rank_status) with totals
DROP TABLE IF EXISTS tmp_a3_rollup;

CREATE TEMP TABLE tmp_a3_rollup AS
SELECT
  CASE WHEN GROUPING(rank_status)=1 THEN 'ALL' ELSE rank_status END AS rank_status,
  COUNT(*) AS appearances,
  ROUND(AVG(sig_att)::numeric, 1)   AS avg_sig_att,
  ROUND(AVG(ctrl_time)::numeric, 1) AS avg_ctrl_time
FROM tmp_a3_appearances
GROUP BY ROLLUP (rank_status);

SELECT *
FROM tmp_a3_rollup
ORDER BY (rank_status='ALL')::int, rank_status;

-- Q3 PIVOT by stance for the most relevant rank segments 
DROP TABLE IF EXISTS tmp_a3_stance_pivot_final;

CREATE TEMP TABLE tmp_a3_stance_pivot_final AS
SELECT
  a.rank_status,
  COUNT(*) AS appearances,
  ROUND((AVG(a.sig_att) FILTER (WHERE a.stance_group='Orthodox'))::numeric, 1) AS orthodox_avg_sig_att,
  ROUND((AVG(a.sig_att) FILTER (WHERE a.stance_group='Southpaw'))::numeric, 1) AS southpaw_avg_sig_att,
  ROUND((AVG(a.sig_att) FILTER (WHERE a.stance_group='Switch'))::numeric, 1)   AS switch_avg_sig_att,
  ROUND((AVG(a.ctrl_time) FILTER (WHERE a.stance_group='Orthodox'))::numeric, 1) AS orthodox_avg_ctrl_time,
  ROUND((AVG(a.ctrl_time) FILTER (WHERE a.stance_group='Southpaw'))::numeric, 1) AS southpaw_avg_ctrl_time,
  ROUND((AVG(a.ctrl_time) FILTER (WHERE a.stance_group='Switch'))::numeric, 1)   AS switch_avg_ctrl_time
  
FROM tmp_a3_appearances a
WHERE a.rank_status IN (
  SELECT rank_status
  FROM tmp_a3_rollup
  WHERE rank_status <> 'ALL'
)
GROUP BY a.rank_status;

SELECT *
FROM tmp_a3_stance_pivot_final
ORDER BY appearances DESC, rank_status;

/* ============================================================
   ANALYSIS 3
   ============================================================ */

-- Q1 Base table with winner-oriented diffs 
DROP TABLE IF EXISTS tmp_a4_base;

CREATE TEMP TABLE tmp_a4_base AS
SELECT
  f.winner,
  df.finish,
  df.finishdetails,

  -- winner-oriented diffs
  CASE WHEN f.winner = 'Blue' THEN -1 * f.heightdif ELSE f.heightdif END AS win_heightdif,
  CASE WHEN f.winner = 'Blue' THEN -1 * f.agedif    ELSE f.agedif    END AS win_agedif,
  CASE WHEN f.winner = 'Blue' THEN -1 * f.reachdif  ELSE f.reachdif  END AS win_reachdif,

  -- measure (total volume)
  (COALESCE(f.r_avgsigstratt,0) + COALESCE(f.b_avgsigstratt,0)) AS total_sig_att

FROM public.fact_fight f
JOIN public.dim_finish df ON df.finish_key = f.finish_key
WHERE f.winner IN ('Red','Blue');

SELECT *
FROM tmp_a4_base
LIMIT 25;


-- Q2 ROLL-UP by finish 
DROP TABLE IF EXISTS tmp_a4_finish_rollup;

CREATE TEMP TABLE tmp_a4_finish_rollup AS
SELECT
  CASE
    WHEN finish IN ('M-DEC','U-DEC','S-DEC') THEN 'Decision'
    WHEN finish = 'KO/TKO'                  THEN 'KO/TKO'
    WHEN finish = 'SUB'                     THEN 'Submission'
    ELSE 'Other'
  END AS finish_category,

  COUNT(*) AS fights,
  ROUND(AVG(win_heightdif)::numeric, 2) AS avg_win_heightdif,
  ROUND(AVG(win_agedif)::numeric, 2)    AS avg_win_agedif,
  ROUND(AVG(win_reachdif)::numeric, 2)  AS avg_win_reachdif,
  ROUND(AVG(total_sig_att)::numeric, 1) AS avg_total_sig_att

FROM tmp_a4_base
GROUP BY finish_category;

SELECT *
FROM tmp_a4_finish_rollup
ORDER BY fights DESC;


-- Q3 SLICE & DICE on KO/TKO + DRILL-DOWN on non-null finishdetails
DROP TABLE IF EXISTS tmp_a4_ko_details_drilldown;

CREATE TEMP TABLE tmp_a4_ko_details_drilldown AS
SELECT
  finishdetails,
  COUNT(*) AS fights,
  ROUND(AVG(win_heightdif)::numeric, 2) AS avg_win_heightdif,
  ROUND(AVG(win_agedif)::numeric, 2)    AS avg_win_agedif,
  ROUND(AVG(win_reachdif)::numeric, 2)  AS avg_win_reachdif,
  ROUND(AVG(total_sig_att)::numeric, 1) AS avg_total_sig_att
FROM tmp_a4_base
WHERE finish = 'KO/TKO'                 -- SLICE
  AND finishdetails IS NOT NULL         -- DICE 
  AND finishdetails <> ''
GROUP BY finishdetails                -- DRILL-DOWN level
HAVING count(*) >= 5;

SELECT *
FROM tmp_a4_ko_details_drilldown
ORDER BY fights DESC, finishdetails;

-- 2nd version with SUM
DROP TABLE IF EXISTS tmp_a4_sub_details_drilldown;

CREATE TEMP TABLE tmp_a4_sub_details_drilldown AS
SELECT
  finishdetails,
  COUNT(*) AS fights,
  ROUND(AVG(win_heightdif)::numeric, 2) AS avg_win_heightdif,
  ROUND(AVG(win_agedif)::numeric, 2)    AS avg_win_agedif,
  ROUND(AVG(win_reachdif)::numeric, 2)  AS avg_win_reachdif,
  ROUND(AVG(total_sig_att)::numeric, 1) AS avg_total_sig_att
FROM tmp_a4_base
WHERE finish = 'SUB'                    -- SLICE (only submissions)
  AND finishdetails IS NOT NULL         -- DICE (keep meaningful details)
  AND finishdetails <> ''
GROUP BY finishdetails                  -- DRILL-DOWN 
HAVING COUNT(*) >= 5;

SELECT *
FROM tmp_a4_sub_details_drilldown
ORDER BY fights DESC, finishdetails;
