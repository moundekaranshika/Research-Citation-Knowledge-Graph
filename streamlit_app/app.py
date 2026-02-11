import streamlit as st
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

st.title("📚 Research Citation Knowledge Graph")

# 🔍 Top Cited Papers
st.header("Top Cited Papers")

with driver.session() as session:
    result = session.run("""
        MATCH (p:Paper)<-[:CITES]-()
        RETURN p.title AS title, COUNT(*) AS citations
        ORDER BY citations DESC
        LIMIT 10
    """)

    for record in result:
        st.write(f"📄 {record['title']} — {record['citations']} citations")

# 👨‍🔬 Top Authors
st.header("Top Authors")

with driver.session() as session:
    result = session.run("""
        MATCH (a:Author)-[:WROTE]->(p:Paper)
        RETURN a.name AS author, COUNT(p) AS papers
        ORDER BY papers DESC
        LIMIT 10
    """)

    for record in result:
        st.write(f"👤 {record['author']} — {record['papers']} papers")

# 🔎 Search Paper
st.header("Search Paper")

paper_title = st.text_input("Enter paper title")

if paper_title:
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Paper)
            WHERE p.title CONTAINS $title
            RETURN p.title AS title, p.year AS year
        """, title=paper_title)

        for record in result:
            st.write(f"📄 {record['title']} ({record['year']})")

driver.close()
