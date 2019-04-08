--- Creates the CAMD database schema

DROP SCHEMA camd CASCADE
CREATE SCHEMA IF NOT EXISTS camd;



CREATE TABLE IF NOT EXISTS camd.material (
    id INT PRIMARY KEY,
    definition JSON,
    poscar TEXT,
    defintion_dft JSON,
    poscar_dft TEXT
);

CREATE TABLE IF NOT EXISTS camd.material_set (
    id SERIAL PRIMARY KEY,
    material_ids INT[]
);

CREATE TABLE IF NOT EXISTS camd.feature (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR
);

CREATE TABLE IF NOT EXISTS camd.feature_set (
    id SERIAL PRIMARY KEY,
    feature_ids INT[]
);

CREATE TABLE IF NOT EXISTS camd.featurization (
    id SERIAL PRIMARY KEY,
    material_id INT REFERENCES camd.material(id),
    feature_id INT REFERENCES camd.feature(id),
    value DECIMAL
);

CREATE TABLE IF NOT EXISTS camd.algorithm (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR
);

CREATE TABLE IF NOT EXISTS camd.dft_recipe (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR,
    definition JSON
);

CREATE TABLE IF NOT EXISTS camd.dft_runs (
    id SERIAL PRIMARY KEY,
    date_time TIMESTAMP WITH TIME ZONE,
    dft_recipe_id INT REFERENCES camd.dft_recipe(id),
    material_id INT REFERENCES camd.material(id),
    results JSON
);

CREATE TABLE IF NOT EXISTS camd.mlmodel (
    id SERIAL PRIMARY KEY,
    material_set_id INT REFERENCES camd.material_set(id),
    feature_set_id INT REFERENCES camd.feature_set(id),
    algorithm_id INT REFERENCES camd.algorithm(id),
    train_set_id INT REFERENCES camd.material_set(id),
    dev_set_id INT REFERENCES camd.material_set(id),
    date_time_fit TIMESTAMP WITH TIME ZONE,
    performance JSON,
    pickle_location VARCHAR
);