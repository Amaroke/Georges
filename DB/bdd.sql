    CREATE TABLE `analogie` (
      `analogie_id` int NOT NULL,
      `page1` varchar(100) DEFAULT NULL,
      `page2` varchar(100) DEFAULT NULL,
      `difference_niveau_gris` double DEFAULT NULL,
      `difference_point_noir` int DEFAULT NULL,
      `difference_point_blanc` int DEFAULT NULL,
      `difference_gamma` double DEFAULT NULL,
      `difference_matrices` double DEFAULT NULL
    );

    CREATE TABLE `matrice` (
      `matrice_id` int NOT NULL,
      `page_id` varchar(100) NOT NULL,
      `haut_gauche` double NOT NULL,
      `haut_milieu` double NOT NULL,
      `haut_droite` double NOT NULL,
      `bas_gauche` double NOT NULL,
      `bas_milieu` double NOT NULL,
      `bas_droite` double NOT NULL
    );


    CREATE TABLE `page` (
      `page_id` varchar(100) NOT NULL,
      `fascicule_id` varchar(100) NOT NULL,
      `niveau_gris` double NOT NULL
    );


    CREATE TABLE `triplet` (
      `triplet_id` int NOT NULL,
      `page_id` varchar(100) NOT NULL,
      `point_noir` int NOT NULL,
      `point_blanc` int NOT NULL,
      `gamma` double NOT NULL
    );

    ALTER TABLE `analogie`
      ADD PRIMARY KEY (`analogie_id`);

    ALTER TABLE `matrice`
      ADD PRIMARY KEY (`matrice_id`);

    ALTER TABLE `page`
      ADD PRIMARY KEY (`page_id`);

    ALTER TABLE `triplet`
      ADD PRIMARY KEY (`triplet_id`);

    ALTER TABLE `matrice`
      MODIFY `matrice_id` int NOT NULL AUTO_INCREMENT;

    ALTER TABLE `triplet`
      MODIFY `triplet_id` int NOT NULL AUTO_INCREMENT;

    ALTER TABLE `analogie`
      MODIFY `analogie_id` int NOT NULL AUTO_INCREMENT;

    ALTER TABLE `analogie`
      ADD CONSTRAINT `page1FK` FOREIGN KEY (`page1`) REFERENCES `page` (`page_id`);

    ALTER TABLE `analogie`
      ADD CONSTRAINT `page2FK` FOREIGN KEY (`page2`) REFERENCES `page` (`page_id`);

    ALTER TABLE `matrice`
      ADD CONSTRAINT `pageFK` FOREIGN KEY (`page_id`) REFERENCES `page` (`page_id`);

    ALTER TABLE `triplet`
      ADD CONSTRAINT `page` FOREIGN KEY (`page_id`) REFERENCES `page` (`page_id`);