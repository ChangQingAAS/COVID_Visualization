--  因为会更新多次数据，取时间戳最新的那组数据
select end_update_time,province,city,county,address,type
from risk_area  
where end_update_time=(
    select end_update_time  
    from risk_area 
    order by end_update_time desc 
    limit 1
) 