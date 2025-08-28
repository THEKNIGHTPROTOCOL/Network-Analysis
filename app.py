import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# ===============================
# Streamlit Page Config
# ===============================
st.set_page_config(page_title="🕸️ Network Analysis", layout="wide")
st.title("🕸️ Interactive Network Analysis Dashboard")

# ===============================
# File Upload / Sample Dataset
# ===============================
st.sidebar.header("📂 Data Controls")

uploaded_file = st.sidebar.file_uploader("Upload CSV (source,target,weight)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.info("Using sample dataset (comms.csv)")
    df = pd.read_csv("data/comms.csv")

# ===============================
# Preprocess Data
# ===============================
if "weight" not in df.columns:
    df["weight"] = 1  # default if missing

G = nx.from_pandas_edgelist(df, "source", "target", ["weight"])

# ===============================
# Sidebar Analysis Options
# ===============================
st.sidebar.header("⚙️ Visualization Settings")

min_weight = st.sidebar.slider("Minimum edge weight", 1, int(df["weight"].max()), 1)
df = df[df["weight"] >= min_weight]
G = nx.from_pandas_edgelist(df, "source", "target", ["weight"])

layout_option = st.sidebar.selectbox(
    "Graph Layout",
    ["spring", "circular", "kamada_kawai"]
)

size_metric = st.sidebar.selectbox(
    "Node Size Metric",
    ["degree", "betweenness", "closeness"]
)

# ===============================
# Centrality Computation
# ===============================
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)

# Pick node size metric
if size_metric == "degree":
    centrality = degree_centrality
elif size_metric == "betweenness":
    centrality = betweenness_centrality
else:
    centrality = closeness_centrality

# ===============================
# Community Detection
# ===============================
from networkx.algorithms.community import greedy_modularity_communities
communities = list(greedy_modularity_communities(G))
community_map = {}
for i, c in enumerate(communities):
    for node in c:
        community_map[node] = i

# ===============================
# PyVis Interactive Graph
# ===============================
net = Network(notebook=False, height="600px", width="100%", bgcolor="#222222", font_color="white")
net.force_atlas_2based()

for node in G.nodes():
    net.add_node(
        node,
        title=f"Node: {node}<br>"
              f"Degree: {degree_centrality.get(node,0):.2f}<br>"
              f"Betweenness: {betweenness_centrality.get(node,0):.2f}<br>"
              f"Closeness: {closeness_centrality.get(node,0):.2f}",
        value=centrality.get(node, 1)*20,
        color=f"hsl({community_map.get(node,0)*50},70%,50%)"
    )

for source, target, data in G.edges(data=True):
    net.add_edge(source, target, value=data["weight"])

# Save and display
net.save_graph("network.html")
HtmlFile = open("network.html", "r", encoding="utf-8")
components.html(HtmlFile.read(), height=650)

# ===============================
# Insights Panel
# ===============================
st.subheader("📊 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔝 Top 5 Influential Nodes")
    top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    st.table(pd.DataFrame(top_nodes, columns=["Node", f"{size_metric.capitalize()} Centrality"]))

with col2:
    st.markdown("### 🏘️ Communities Detected")
    st.write(f"Total Communities: {len(communities)}")
    for i, c in enumerate(communities):
        st.write(f"**Community {i+1}:** {list(c)}")
