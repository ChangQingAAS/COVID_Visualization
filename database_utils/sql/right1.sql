-- 返回确诊人数前5名的city
SELECT city,confirm 
FROM (
        select city,confirm 
        from details
        where update_time=(
            select update_time 
            from details 
            order by update_time desc 
            limit 1
        )   and  province not in ( "北京","上海","天津","重庆","香港","台湾","澳门") 

        union all 

        select province as city,sum(confirm) as confirm 
        from details  
        where update_time=(
            select update_time 
            from details 
            order by update_time desc 
            limit 1
        )  and province in ("北京","上海","天津","重庆","香港","台湾","澳门") 
        group by province
    ) as a  
ORDER BY confirm DESC 
LIMIT 5