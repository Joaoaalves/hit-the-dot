CREATE TABLE IF NOT EXISTS Ferias (
	id int NOT NULL,
	inicio int NOT NULL,
	fim int NOT NULL
);

CREATE TABLE IF NOT EXISTS Faltas (
	func_id int NOT NULL,
	current_status varchar(15) NOT NULL,
	id int NOT NULL,
	date varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS Users(
	id int NOT NULL,
	email varchar(60) NOT NULL,
	role varchar(20) NOT NULL,
	inicio_trabalho varchar(10),
	cargo int NOT NULL,
	name varchar(50) NOT NULL,
	turno int NOT NULL,
	dias_trabalho int NOT NULL,
	celular varchar(20)
);

CREATE TABLE IF NOT EXISTS Turnos(
	user_id int NOT NULL,
	almocou boolean NOT NULL,
	current_status varchar(15) NOT NULL,
	dia varchar(10) NOT NULL,
	hora_entrada varchar(8),
	hora_saida varchar(8),
	inicio_almoco varchar(8),
	fim_almoco varchar(8)
);

CREATE TABLE IF NOT EXISTS Feriados(
	id int NOT NULL,
	date varchar(10) NOT NULL,
	name varchar(50) NOT NULL,
	`repeat` boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS Cargos(
	id int NOT NULL,
	nome varchar(30) NOT NULL,
	descricao varchar(600)
);
