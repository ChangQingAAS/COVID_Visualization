-- 返回最近的30条热搜
select content 
from hotsearch 
order by id desc 
limit 30 
