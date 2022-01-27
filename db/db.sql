create table Piscine_Installation_Aquatique (
  id integer primary key,
  piscine_id integer,
  type varchar(10),
  nom varchar(100),
  arrondissement varchar(150),
  adresse varchar(500),
  propriete varchar(100),
  gestion varchar(100),
  point_X real,
  point_Y real,
  equipement varchar(150),
  longitude real,
  latitude real
);



Create table Arrondissement_Patinoires(
  id_arrondissement integer primary key,
  nom_arrondissement varchar(500)
);

Create table Patinoires(
  id_arrondissement integer,
  id_patinoire integer primary key,
  nom_patinoire varchar(500),
  FOREIGN KEY (id_arrondissement) REFERENCES Arrondissement_Patinoires(id_arrondissement)
);


Create table Condition (
  id_condition integer primary key,
  id_patinoire  integer,
  date_heure text,
  ouvert integer,
  deblaye integer,
  arrose integer,
  resurface integer,
  FOREIGN KEY (id_patinoire) REFERENCES Patinoires(id_patinoire)
);



create table Glissades (
    glissade_id integer primary key,
    nom varchar(200),
    ouvert integer,
    deblaye integer,
    condition varchar(100)
   
);


create table Arrondissement (
        glissade_id integer primary key,
        nom_arrondissement varchar(300),
        cle varchar(10),
        date_mise_a_jour text,
        FOREIGN KEY (glissade_id) REFERENCES Glissades(glissade_id)
);




