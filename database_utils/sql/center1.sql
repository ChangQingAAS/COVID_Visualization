-- because of updating data several times, get the newest data
select sum(confirm),(select suspect from history order by ds desc limit 1), sum(heal), sum(dead) 
from details 
where update_time=(
    select update_time 
    from details 
    order by update_time desc 
    limit 1
) 