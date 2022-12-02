drop table if exists actions;
drop table if exists strategy;

create table strategy(opp TEXT, self TEXT, result TEXT);

create table actions(item TEXT, wins_against TEXT, score INTEGER);
insert into actions values ('r', 's', 1);
insert into actions values ('p', 'r', 2);
insert into actions values ('s', 'p', 3);

