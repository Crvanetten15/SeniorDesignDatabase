/*Creation of weekly disease totals*/
CREATE TABLE disease_weekly_totals (
disease VARCHAR(55),
year INT,
week INT,
CasesInWeek INT,
PRIMARY KEY(Disease, Year, Week)
);

INSERT INTO disease_weekly_totals (disease, year, week, CasesInWeek )
SELECT disease_name, year, week, SUM(disease_cases) as CasesInWeek
FROM weekly_data
GROUP BY disease_name, year, week;

/*Yearly Data Creation */
CREATE TABLE disease_yearly_totals (
disease VARCHAR(55),
year INT,
CasesInYear INT,
PRIMARY KEY(Disease, Year)
);

INSERT INTO disease_yearly_totals (disease, year, CasesInYear )
SELECT disease_name, year,  SUM(disease_cases) as CasesInYear
FROM weekly_data
GROUP BY disease_name, year;

CREATE TABLE highest_weekly_data (
            year INT NOT NULL,
            week INT NOT NULL,
            disease_name VARCHAR(50) NOT NULL,
            state VARCHAR(50) NOT NULL,
            disease_cases INT NOT NULL
            );

ALTER TABLE highest_weekly_data
ADD UNIQUE INDEX unique_row (year, week, disease_name, state, disease_cases);

INSERT IGNORE INTO highest_weekly_data (year, week, disease_name, state, disease_cases)
SELECT year, week, disease_name, state, disease_cases
FROM (
    SELECT year, week, disease_name, state, disease_cases,
        ROW_NUMBER() OVER (PARTITION BY year, week, disease_name ORDER BY disease_cases DESC) AS ranked
    FROM weekly_data
) ranked_data
WHERE ranked <= 5; 