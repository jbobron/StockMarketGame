CREATE TABLE `Users` (
  `uid` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `firstname` VARCHAR(100),
  `lastname` VARCHAR(100),
  `email` VARCHAR(120) UNIQUE,
  `pwdhash` VARCHAR(100),
  `initialCash` FLOAT,
  `cashRemaining` FLOAT,
  `portfolioWorth` FLOAT
);

CREATE TABLE `UserGroups` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `u_id` INT,
  PRIMARY KEY  (`id`)
);

CREATE TABLE `Group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `groupname` VARCHAR(120),
  `start` DATE,
  `end` DATE,
  `g_id` INT,
  PRIMARY KEY  (`id`)
);

CREATE TABLE `Portfolio` (
  `stock_id` INT,
  `u_id` INT,
  `g_id` INT,
  `execution_date` DATE,
  `quantity` INT,
  `fees` INT
);

CREATE TABLE `Stock` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100),
  `symbol` VARCHAR(100),
  PRIMARY KEY  (`id`)
);

CREATE TABLE `StockPrice` (
  `stock_id` INT,
  `date` DATE,
  `open` FLOAT,
  `close` FLOAT,
  `low` FLOAT,
  `high` FLOAT,
  `volume` INT
);

CREATE TABLE `test1` (
  `mynumeric` Numeric,
  `mydecimal` DECIMAL,
  `myfloatAsDec` FLOAT.asDecimal,
  `mydecimal` DECIMAL

);

CREATE TABLE `portfolio` (
  `pid` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100),
  `ticker` VARCHAR(100),
  `quantity` INT,
  `price` FLOAT,
  `execution_date` DATE,
  `last_queried` DATE,
  `currentPrice` FLOAT,
  PRIMARY KEY  (`pid`)
);
-- for each stock:
-- portfolioWorth = portfolioWorth + (currentPrice-price)


CREATE TABLE `testForUsers` (
  `uid` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `firstname` VARCHAR(100),
  `lastname` VARCHAR(100),
  `email` VARCHAR(120) UNIQUE,
  `pwdhash` VARCHAR(100),
  `initialCash` FLOAT,
  `currentCash` FLOAT
);

CREATE TABLE `stockshistory` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ticker` VARCHAR(100),
  `volume` FLOAT,
  `high` FLOAT,
  `low` FLOAT,
  `date` DATE,
  `close` FLOAT,
  `open` FLOAT
);











ALTER TABLE `UserGroups` ADD CONSTRAINT `UserGroups_fk1` FOREIGN KEY (`u_id`) REFERENCES User(`id`);
ALTER TABLE `Group` ADD CONSTRAINT `Group_fk1` FOREIGN KEY (`g_id`) REFERENCES Group(`id`);
ALTER TABLE `Portfolio` ADD CONSTRAINT `Portfolio_fk1` FOREIGN KEY (`stock_id`) REFERENCES Stock(`id`);
ALTER TABLE `Portfolio` ADD CONSTRAINT `Portfolio_fk2` FOREIGN KEY (`u_id`) REFERENCES User(`id`);
ALTER TABLE `Portfolio` ADD CONSTRAINT `Portfolio_fk3` FOREIGN KEY (`g_id`) REFERENCES Group(`id`);

ALTER TABLE `StockPrice` ADD CONSTRAINT `StockPrice_fk1` FOREIGN KEY (`stock_id`) REFERENCES Stock(`id`)