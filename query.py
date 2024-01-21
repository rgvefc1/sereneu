from sqlalchemy import text

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
    serene_member a
LEFT JOIN
    (
        SELECT
            s1.member_id,
            s1.visit_time AS max_visit_time,
            s1.surgery_info,
            ROW_NUMBER() OVER(PARTITION BY s1.member_id ORDER BY s1.visit_time DESC) AS rn
        FROM
            serene_surgery s1
        WHERE
            s1.visit_time = (
                SELECT MAX(s2.visit_time)
                FROM serene_surgery s2
                WHERE s2.member_id = s1.member_id
            )
    ) s ON a.member_id = s.member_id AND s.rn = 1
LEFT JOIN
    serene_imgfile i ON a.member_id = i.member_id
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
    FROM serene_surgery a
    LEFT JOIN serene_member b ON a.member_id = b.member_id
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
  from serene_surgery a
left join serene_member b on a.member_id = b.member_id 
left join serene_imgfile c on b.member_id = c.member_id
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
    UPDATE serene_surgery 
   SET surgery_info = :categori,
	   payment_amount = :price,
       member_id = :member_id,
       visit_time = :visit_time
WHERE SURGERY_ID = :sergery_id                     
                      
                      """)

update_date = text("""
    UPDATE serene_surgery 
    SET visit_time = :visit_time
    WHERE SURGERY_ID = :sergery_id               
                   """)

delete_surgery = text("""
    DELETE from serene_surgery WHERE surgery_id = :sergery_id
                      """)

selectMemberSearchFlag = text("""
SELECT
    a.member_id,
    a.customer_name,
    a.customer_phone,
    a.gender,
    MAX(CASE WHEN i.categori = 'profile' THEN i.file_path END) AS profile_img
FROM
    serene_member a
LEFT JOIN
    serene_imgfile i ON a.member_id = i.member_id
WHERE a.customer_name = :member_name or a.customer_phone = :member_phone
GROUP BY
    a.member_id,
    a.customer_name,
    a.customer_phone,
    a.gender
""")
selectMemberFilterName = "select* from serene_member where customer_name = %s"
selectMemberFilterPhone = "select* from serene_member where customer_phone = %a"
selectMemberALL ="select* from serene_member"