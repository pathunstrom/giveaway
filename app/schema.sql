drop table if exists entries;
create table entries (
  id INTEGER PRIMARY KEY autoincrement,
  title text not NULL,
  text text not null
);