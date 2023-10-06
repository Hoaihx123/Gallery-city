# Gallery_city
![image](https://github.com/Hoaihx123/Gallery_city/assets/99666261/34e4c470-c7ee-42c5-927d-1882b6343464)
# Fix migrate erro: 
python manage.py migrate --fake core zero  
python manage.py makemigrations core  
python manage.py migrate core      
# if DELETE CASCADE in Django doesn't work, please run the SQL command below:
ALTER TABLE IF EXISTS "core_work_exhibit"
    ADD CONSTRAINT action_collec FOREIGN KEY ("work_id")
    REFERENCES "core_work" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS "core_work_exhibit"
    ADD CONSTRAINT action_collec2 FOREIGN KEY ("exhibit_id")
    REFERENCES "core_exhibit" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS "core_place"
    ADD CONSTRAINT artist1 FOREIGN KEY ("artist_id")
    REFERENCES "core_artist" (user_id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS "core_place"
    ADD CONSTRAINT artist2 FOREIGN KEY ("exhibit_id")
    REFERENCES "core_exhibit" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS "core_notification"
    ADD CONSTRAINT noti1 FOREIGN KEY ("exhibit_id")
    REFERENCES "core_exhibit" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;name, start_time, end_time, type


