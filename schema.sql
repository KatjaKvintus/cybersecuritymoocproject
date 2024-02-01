CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL, 
    name VARCHAR(20) NOT NULL CHECK (length(name) >= 3), 
    password TEXT NOT NULL, 
    role TEXT NOT NULL
);

CREATE UNIQUE INDEX users_name_index ON users (name);

CREATE TABLE recipes (
    id SERIAL NOT NULL, 
    name VARCHAR(40) NOT NULL, 
    type VARCHAR(40) NOT NULL, 
    author_id INTEGER NOT NULL, 
    base_liquid VARCHAR(40) NOT NULL, 
    grain VARCHAR(40) NOT NULL, 
    protein VARCHAR(40) NOT NULL, 
    ingredient_1 VARCHAR(40) NOT NULL, 
    ingredient_2 VARCHAR(40) NOT NULL, 
    sweetener VARCHAR(40) NOT NULL,
    CONSTRAINT recipes_pk PRIMARY KEY (id),
    CONSTRAINT recipes_users_fk
        FOREIGN KEY(author_id)
            REFERENCES users(id)
);

CREATE UNIQUE INDEX recipes_name_index ON recipes (lower(name));

CREATE INDEX recipes_ingredients_index ON recipes 
    (lower(base_liquid), lower(grain), lower(protein), 
    lower(ingredient_1), lower(ingredient_2), lower(sweetener));

CREATE INDEX recipes_type_index ON recipes (lower(type));


CREATE TABLE favorites (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    recipe_id INTEGER NOT NULL, 
    CONSTRAINT favorites_pk PRIMARY KEY (id),
    CONSTRAINT favorites_users_fk
        FOREIGN KEY(user_id)
            REFERENCES users(id),
    CONSTRAINT favorites_recipes_fk
        FOREIGN KEY(recipe_id)
            REFERENCES recipes(id)
);

CREATE UNIQUE INDEX favorites_unique_index ON favorites (recipe_id, user_id);

CREATE TABLE upvotes (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    recipe_id INTEGER NOT NULL, 
    stars INTEGER NOT NULL,
    CONSTRAINT upvotes_pk PRIMARY KEY (id),
    CONSTRAINT upvotes_users_fk
        FOREIGN KEY(user_id)
            REFERENCES users(id),
    CONSTRAINT upvotes_recipes_fk
        FOREIGN KEY(recipe_id)
            REFERENCES recipes(id)
);

CREATE UNIQUE INDEX upvotes_unique_index ON upvotes (user_id, recipe_id);

CREATE TABLE comments (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    recipe_id INTEGER NOT NULL, 
    comment_text TEXT NOT NULL CHECK (length(comment_text) <= 1000),
    CONSTRAINT comments_pk PRIMARY KEY (id),
    CONSTRAINT comments_users_fk
        FOREIGN KEY(user_id)
            REFERENCES users(id),
    CONSTRAINT comments_recipes_fk
        FOREIGN KEY(recipe_id)
            REFERENCES recipes(id)
);

CREATE INDEX comments_search_index ON comments (user_id, recipe_id);

CREATE TABLE recipe_of_the_week (
    id SERIAL NOT NULL, 
    recipe_id INTEGER NOT NULL, 
    date TEXT NOT NULL,
    CONSTRAINT recipe_of_the_week_pk PRIMARY KEY (id),
    CONSTRAINT recipe_of_the_week_recipes_fk
        FOREIGN KEY(recipe_id)
            REFERENCES recipes(id)
);

CREATE UNIQUE INDEX recipe_of_the_week_unique_index ON recipe_of_the_week 
    (recipe_id, date);

INSERT INTO users(name, password, role) VALUES('admin', 'admin', 'admin');
