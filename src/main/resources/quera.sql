--历史战绩
select
-- avg(htgoal),avg(gtgoal)
*
from T_FOOTBALL_DATA_1 t
where 1=1
and leagid=179
--and (hteamname='都灵' and gteamname='国际米兰')
and (hteamname='国际米兰' and gteamname='都灵')
order by vsdate  desc;

---------------------------------------------本赛季平均进失球
--主
select
--*
hteamname,avg(htgoal),avg(gtgoal)
from T_FOOTBALL_DATA_1 t
where 1=1
--odds1!=0 and odds2!=0 and odds3!=0
and leagid=12
and hteamname='西班牙人'
and vsdate>to_date('2018-06-01','yyyy-MM-dd')
group by hteamname;
--客
select
*
--gteamname,avg(htgoal),avg(gtgoal)
from T_FOOTBALL_DATA_1 t
where 1=1
--odds1!=0 and odds2!=0 and odds3!=0
and leagid=12
and gteamname='皇家马德里'
and vsdate>to_date('2018-06-01','yyyy-MM-dd')
order by vsdate desc
group by gteamname;

-- 各队进球数分布
--主
select
hteamname,
sum(case when htgoal=0 then g else 0 end) g0,
sum(case when htgoal=1 then g else 0 end) g1,
sum(case when htgoal=2 then g else 0 end) g2,
sum(case when htgoal=3 then g else 0 end) g3,
sum(case when htgoal=4 then g else 0 end) g4,
sum(case when htgoal=5 then g else 0 end) g5,
sum(case when htgoal=6 then g else 0 end) g6,
sum(case when htgoal=7 then g else 0 end) g7,
sum(case when htgoal=8 then g else 0 end) g8,
sum(case when htgoal=9 then g else 0 end) g9,
sum(case when htgoal=10 then g else 0 end) g10
from (
select
hteamname,htgoal,count(htgoal) as g
from T_FOOTBALL_DATA_1 t
group by hteamname,htgoal
)
where 1=1
group by hteamname
order by hteamname
