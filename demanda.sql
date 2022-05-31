CREATE TABLE `service` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL,
	`valor` INT NOT NULL,
	`tempo` INT NOT NULL,
	`categoria` INT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `servicos_atribuidos` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`service_id` INT NOT NULL,
	`user_id` INT NOT NULL,
	`status` varchar(50) NOT NULL,
	`is_verified` BINARY NOT NULL,
	`cliente_id` INT NOT NULL,
	`link_trello` VARCHAR(300),
	PRIMARY KEY (`id`)
);

CREATE TABLE `categoria_servico` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `cliente`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`id`)
);
