
create table documents(
    id integer primary key autoincrement,
    title varchar(50) not null,
    create_time timestamp  DEFAULT CURRENT_TIMESTAMP,
    content text not null
);

create unique index doc_index on documents (title, create_time);
