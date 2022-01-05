# UI-Schedule

---

### Libraries:

1. PyQt5
2. Psycopg2
3. requests

---

### Functions timetable.py:

* _Delete_ - delete records from database 
* _Save all_ - add records to database 
* _Update_ - update records

---

### Methods of the "MainWindow" class:

* __connect_to_db_ - connect to database "Schedule"
* _datetime_ - add time in project
* __create_sсhedule_tab_ - create tab for selected day of week
* __create_one_day_table_ - create tabel
* __update_day_table_ - add rows from db and other update tabel
* __change_day_from_table_ - change rows in tabel
* __delete_row_ - delete row in tabel and db