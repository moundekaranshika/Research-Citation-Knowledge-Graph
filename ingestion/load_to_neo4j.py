from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection details
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"  # change this

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def load_data():
    df = pd.read_csv("../data/sample_data.csv")

    with driver.session() as session:
        for _, row in df.iterrows():

            # Create Paper
            session.run("""
                MERGE (p:Paper {paper_id: $paper_id})
                SET p.title = $title,
                    p.year = $year
            """, paper_id=row["paper_id"],
                 title=row["title"],
                 year=int(row["year"]))

            # Create Topic
            session.run("""
                MERGE (t:Topic {name: $topic})
                WITH t
                MATCH (p:Paper {paper_id: $paper_id})
                MERGE (p)-[:HAS_TOPIC]->(t)
            """, topic=row["topic"],
                 paper_id=row["paper_id"])

            # Create Institution
            session.run("""
                MERGE (i:Institution {name: $institution})
            """, institution=row["institution"])

            # Create Authors
            authors = row["authors"].split(";")
            for author in authors:
                session.run("""
                    MERGE (a:Author {name: $author})
                    WITH a
                    MATCH (p:Paper {paper_id: $paper_id})
                    MERGE (a)-[:WROTE]->(p)
                """, author=author.strip(),
                     paper_id=row["paper_id"])

                session.run("""
                    MATCH (a:Author {name: $author})
                    MATCH (i:Institution {name: $institution})
                    MERGE (a)-[:AFFILIATED_WITH]->(i)
                """, author=author.strip(),
                     institution=row["institution"])

            # Create Citation Relationship
            if pd.notna(row["cited_paper_id"]):
                session.run("""
                    MATCH (p1:Paper {paper_id: $paper_id})
                    MATCH (p2:Paper {paper_id: $cited_id})
                    MERGE (p1)-[:CITES]->(p2)
                """, paper_id=row["paper_id"],
                     cited_id=row["cited_paper_id"])

    print("Data Loaded Successfully!")

if __name__ == "__main__":
    load_data()
    driver.close()
