CREATE CONSTRAINT paper_id_unique IF NOT EXISTS
FOR (p:Paper)
REQUIRE p.paper_id IS UNIQUE;

CREATE CONSTRAINT author_name_unique IF NOT EXISTS
FOR (a:Author)
REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT institution_name_unique IF NOT EXISTS
FOR (i:Institution)
REQUIRE i.name IS UNIQUE;

CREATE CONSTRAINT topic_name_unique IF NOT EXISTS
FOR (t:Topic)
REQUIRE t.name IS UNIQUE;
