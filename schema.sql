
create table referer (
    id integer primary key autoincrement,
    domain varchar(100) not null,
    date timestamp not null,
    creative_size varchar(50) not null
);

create index ref_index on referer (domain, date);
