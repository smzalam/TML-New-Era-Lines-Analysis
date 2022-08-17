import database_fill.database_functions as dbf

#constants 
DB_NAME = 'leafsroster'

# create table in database
table = "CREATE TABLE `nhl_teams` (`team` varchar(250) NOT NULL, `team_id` varchar(250) NOT NULL, `conference` varchar(250) NOT NULL, `division` varchar(250) NOT NULL, PRIMARY KEY (`team_id`)) ENGINE=InnoDB"

dbf.create_tables(DB_NAME, table)