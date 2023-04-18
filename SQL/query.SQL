/*These tables need to be deleted and recreated or failure will occur*/
DROP TABLE disease_weekly_totals;
DROP TABLE disease_yearly_totals;
DROP TABLE highest_weekly_data;
DROP TABLE average_cases_per_disease;

/*Creation of weekly disease totals*/
CREATE TABLE IF NOT EXISTS disease_weekly_totals (
disease VARCHAR(55),
year INT,
week INT,
CasesInWeek INT,
PRIMARY KEY(Disease, Year, Week)
);

INSERT INTO disease_weekly_totals (disease, year, week, CasesInWeek )
SELECT disease_name, year, week, SUM(disease_cases) as CasesInWeek
FROM weekly_data
GROUP BY disease_name, year, week
ON DUPLICATE KEY UPDATE CasesInWeek = CasesInWeek; 

/*Yearly Data Creation */
CREATE TABLE IF NOT EXISTS disease_yearly_totals (
disease VARCHAR(55),
year INT,
CasesInYear INT,
PRIMARY KEY(Disease, Year)
);

INSERT INTO disease_yearly_totals (disease, year, CasesInYear )
SELECT disease_name, year,  SUM(disease_cases) as CasesInYear
FROM weekly_data
GROUP BY disease_name, year
ON DUPLICATE KEY UPDATE CasesInYear = CasesInYear; 

CREATE TABLE IF NOT EXISTS highest_weekly_data (
            year INT NOT NULL,
            week INT NOT NULL,
            disease_name VARCHAR(50) NOT NULL,
            state VARCHAR(50) NOT NULL,
            disease_cases INT NOT NULL, 
            PRIMARY KEY(year, week, disease_name, state)
            );

INSERT INTO highest_weekly_data (year, week, disease_name, state, disease_cases)
SELECT year, week, disease_name, state, disease_cases
FROM (
    SELECT year, week, disease_name, state, disease_cases,
        ROW_NUMBER() OVER (PARTITION BY year, week, disease_name ORDER BY disease_cases DESC) AS ranked
    FROM weekly_data
) ranked_data
WHERE ranked <= 5
ON DUPLICATE KEY UPDATE disease_cases = disease_cases; 

CREATE TABLE IF NOT EXISTS average_cases_per_disease (
    year INT NOT NULL,
    week INT NOT NULL,
    disease_name VARCHAR(255) NOT NULL,
    average_cases FLOAT NOT NULL,
    PRIMARY KEY(year, week, disease_name)
);

-- insert the data, ignoring duplicates
INSERT INTO average_cases_per_disease (year, week, disease_name, average_cases)
SELECT year, week, disease_name, AVG(disease_cases)
FROM weekly_data
GROUP BY year, week, disease_name
ON DUPLICATE KEY UPDATE average_cases = average_cases;



SELECT * FROM weekly_data;
SELECT * FROM daily_data;
SELECT * FROM disease_weekly_totals;
SELECT * FROM disease_yearly_totals;
SELECT * FROM population_data;
SELECT * FROM highest_weekly_data;
SELECT * FROM average_cases_per_disease;