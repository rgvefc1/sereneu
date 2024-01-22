from sqlalchemy import text

selectMemberFilterName = text("""SELECT member_id,customer_name,customer_phone,gender FROM SERENE_MEMBER WHERE CUSTOMER_NAME = :member_name""")

selectMemberFilterPhone = text("""
                        SELECT * FROM SERENE_MEMBER WHERE CUSTOMER_PHONE = :member_phone      
                              """)

insertSergery = text("""
        INSERT INTO SERENE_SURGERY (surgery_info, payment_amount, member_id, visit_time)
        VALUES (:surgery_info, :payment_amount, :member_id, :visit_time)
""")

insertMember = text("""
        INSERT INTO SERENE_MEMBER (customer_name, customer_phone, gender)
        VALUES (:customer_name, :customer_phone, :gender)
                    """)

insertImgFile = text("""
    INSERT INTO SERENE_IMGFILE (member_id, categori, uploaddate, file_path, file_name)
    VALUES (:member_id,:categori,:uploaddate,:file_path,:file_name)
""")
selectMemberSergical = text("""
    SELECT
    a.member_id,
    a.customer_name,
    a.customer_phone,
    a.gender,
    max_visit_time,
    surgery_info,
    MAX(CASE WHEN i.categori = 'profile' THEN i.file_path END) AS profile_img,
    MAX(CASE WHEN i.categori = 'before' THEN i.file_path END) AS before_img,
    MAX(CASE WHEN i.categori = 'after' THEN i.file_path END) AS after_img
FROM
    SERENE_MEMBER a
LEFT JOIN
    (
        SELECT
            s1.member_id,
            s1.visit_time AS max_visit_time,
            s1.surgery_info,
            ROW_NUMBER() OVER(PARTITION BY s1.member_id ORDER BY s1.visit_time DESC) AS rn
        FROM
            SERENE_SURGERY s1
        WHERE
            s1.visit_time = (
                SELECT MAX(s2.visit_time)
                FROM SERENE_SURGERY s2
                WHERE s2.member_id = s1.member_id
            )
    ) s ON a.member_id = s.member_id AND s.rn = 1
LEFT JOIN
    SERENE_IMGFILE i ON a.member_id = i.member_id
GROUP BY
    a.member_id,
    a.customer_name,
    a.customer_phone,
    a.gender,
    max_visit_time,
    surgery_info
""")

selectSchedule = text("""
    SELECT surgery_id as id, customer_name as title, DATE_FORMAT(visit_time,'%Y-%m-%dT%H:%i:%S') as start 
    FROM SERENE_SURGERY a
    LEFT JOIN SERENE_MEMBER b ON a.member_id = b.member_id
    WHERE visit_time BETWEEN :start_date AND :end_date
    ORDER BY visit_time
""")

selectSurgeryform = text("""
select 
       a.surgery_info as surgery_info
	   ,a.payment_amount as price
       ,a.visit_time as visit_time
       ,b.member_id as member_id
       ,b.customer_name as member_name
       ,b.customer_phone as member_phone
       ,b.gender  as gender
       ,MAX(CASE WHEN c.categori = 'profile' THEN c.file_path END) AS profile_img
       ,a.surgery_id as surgery_id
  from SERENE_SURGERY a
left join SERENE_MEMBER b on a.member_id = b.member_id 
left join SERENE_IMGFILE c on b.member_id = c.member_id
 where surgery_id = :surgery_id
   and c.categori = 'profile'
group by a.surgery_info
	   ,a.payment_amount
       ,a.visit_time 
       ,b.member_id
       ,b.customer_name
       ,b.customer_phone
       ,b.gender
       """)

update_surgery = text("""
    UPDATE SERENE_SURGERY 
   SET surgery_info = :categori,
	   payment_amount = :price,
       member_id = :member_id,
       visit_time = :visit_time
WHERE SURGERY_ID = :sergery_id                     
                      
                      """)

update_date = text("""
    UPDATE SERENE_SURGERY 
    SET visit_time = :visit_time
    WHERE SURGERY_ID = :sergery_id               
                   """)

delete_surgery = text("""
    DELETE from SERENE_SURGERY WHERE surgery_id = :sergery_id
                      """)

selectMemberSearchFlag = text("""
SELECT
    a.member_id,
    a.customer_name,
    a.customer_phone,
    a.gender,
    MAX(CASE WHEN i.categori = 'profile' THEN i.file_path END) AS profile_img
FROM
    SERENE_MEMBER a
LEFT JOIN
    SERENE_IMGFILE i ON a.member_id = i.member_id
WHERE a.customer_name = :member_name or a.customer_phone = :member_phone
GROUP BY
    a.member_id,
    a.customer_name,
    a.customer_phone,
    a.gender
""")

selectMemberALL ="select* from SERENE_MEMBER"