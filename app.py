import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit Page Config
st.set_page_config(page_title="🕸 Terrorist Network Analysis", layout="wide")
st.title("🕸 Network Analysis of Terrorist Groups")

# Sidebar for dataset input
st.sidebar.header("📂 Data Input")
uploaded_file = st.sidebar.file_uploader("Upload communication CSV", type=["csv"])

# Load dataset
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using sample dataset from /data/comms.csv")
    df = pd.read_csv("data/comms.csv")

st.subheader("🔍 Dataset Preview")
st.dataframe(df.head(15))

# ================== BUILD GRAPH ==================
G = nx.from_pandas_edgelist(df, "source", "target", ["weight"])

# ================== METRICS ==================
st.subheader("📊 Network Metrics")

degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)

metrics = pd.DataFrame({
    "Node": degree_centrality.keys(),
    "Degree Centrality": degree_centrality.values(),
    "Betweenness": betweenness.values(),
    "Closeness": closeness.values()
}).sort_values("Degree Centrality", ascending=False)

st.write(metrics)

# ================== COMMUNITY DETECTION ==================
st.subheader("👥 Community Detection")
try:
    from networkx.algorithms.community import greedy_modularity_communities
    communities = list(greedy_modularity_communities(G))
    comm_map = {}
    for I, comm in enumerate(communities):
        for node in comm:
            comm_map[node] = I
    metrics["Community"] = metrics["Node"].map(comm_map)
    st.write(metrics)
except Exception as e:
    st.warning("Community detection unavailable. Install networkx >= 2.8")

# ================== VISUALIZATION ==================
st.subheader("🌐 Network Graph")

fig, ax = plt.subplots(figsize=(10,7))
pos = nx.spring_layout(G, seed=42)

node_sizes = [v * 2500 for v in degree_centrality.values()]
node_colors = [comm_map.get(node, 0) for node in G.nodes()]

nx.draw_networkx(
    G, pos, with_labels=True, node_size=node_sizes,
    node_color=node_colors, cmap=plt.cm.Set3,
    edge_color="gray", font_size=9, ax=ax
)

st.pyplot(fig)

# ================== INSIGHTS ==================
st.subheader("📌 Key Insights")
st.markdown("""
- *Leaders* (high degree centrality) manage multiple recruits.  
- *Couriers* (high betweenness) act as bridges between clusters.  
- *Tightly connected groups* detected using community detection.  
- Cross-links between leaders show *inter-group collaboration*.  
""")
