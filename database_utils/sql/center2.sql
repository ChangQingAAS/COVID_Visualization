-- 返回各省数据
-- because of updating data several times, get the newest data
select province,sum(confirm) 
from details 
where update_time=(
    select update_time 
    from details
    order by update_time desc 
    limit 1
) 
group by province