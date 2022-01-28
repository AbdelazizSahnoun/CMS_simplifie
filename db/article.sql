create table article (
  id integer primary key,
  titre varchar(100),
  identifiant varchar(50),
  auteur varchar(100),
  date_publication text,
  paragraphe varchar(500)
);

--source /home/vagrant/inf5190_tp1_venv/bin/activate
INSERT INTO article VALUES(1,"Salut","AAA","Lako","2021-10-18","C'EST LUI");
INSERT INTO article VALUES(2,"Daru","BBB","Mako","2021-10-18","C'EST ELLE");
INSERT INTO article VALUES(3,"Laru","CCC","Zako","2021-10-18","C'EST TOI");
INSERT INTO article VALUES(4,"Paru","DDD","Nako","2021-10-18","C'EST EUX");
INSERT INTO article VALUES(5,"Garu","EEE","Oako","2021-10-18","C'EST NOUS");
INSERT INTO article VALUES(6,"Naru","FFF","Pako","2021-10-18","C'EST VOUS");
INSERT INTO article VALUES(7,"Taru","GGG","Dako","2015-04-01","C'EST MOI");
INSERT INTO article VALUES(8,"Qaru","GGG","Dako","2015-04-01","C'EST MOI");
INSERT INTO article VALUES(9,"Zaru","GGG","Dako","2015-04-01","C'EST MOI");