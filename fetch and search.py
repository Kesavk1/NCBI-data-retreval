from Bio import Entrez
import pandas as pd

# Set your email
Entrez.email = "your_email@example.com"

# Function to search and fetch articles
def fetch_pubmed_articles(keyword, max_results=50):
    handle = Entrez.esearch(db="pubmed", term=keyword, retmax=max_results)
    record = Entrez.read(handle)
    id_list = record["IdList"]
    handle.close()

    if not id_list:
        return pd.DataFrame()

    handle = Entrez.esummary(db="pubmed", id=",".join(id_list))
    summaries = Entrez.read(handle)
    handle.close()

    data = []
    for summary in summaries:
        data.append({
            "PubMed ID": summary["Id"],
            "Title": summary["Title"],
            "Authors": ", ".join([a["Name"] for a in summary.get("Authors", [])]),
            "Year": summary.get("PubDate", "").split(" ")[0]
        })

    return pd.DataFrame(data)

# search and run
keyword = "Chiari"
df = fetch_pubmed_articles(keyword)
df.head()


df.to_csv("chiari_pubmed_results.csv", index=False)



