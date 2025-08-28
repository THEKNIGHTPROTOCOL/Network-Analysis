import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
from io import StringIO, BytesIO
import base64

# ================== CONFIG ==================
st.set_page_config(page_title="🌐 Network Analysis Dashboard", layout="wide")
st.title("🌐 Network Analysis Dashboard")
st.write("Analyze communication patterns and connections within suspected networks.")

# ================== LOAD DATA ==================
st.sidebar.header("📂 Data Options")
uploaded_file = st.sidebar.file_uploader("Upload Edge List CSV", type=["csv"])

@st.cache_data
def load_sample_data():
    data = {
        "source": ["A", "A", "B", "C", "D", "E", "F", "G"],
        "target": ["B", "C", "D", "D", "E", "F", "G", "A"],
        "weight": [5, 3, 4, 2, 1, 2, 4, 3]
    }
    return pd.DataFrame(data)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.info("No file uploaded. Using **sample dataset**.")
    df = load_sample_data()

st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

# ================== GRAPH SETTINGS ==================
st.sidebar.header("⚙️ Graph Settings")
directed = st.sidebar.checkbox("Directed Graph", value=True)
weight_threshold = st.sidebar.slider("Minimum Edge Weight", 0, int(df["weight"].max()), 0)

# Filter dataset by weight
df_filtered = df[df["weight"] >= weight_threshold]

# Build graph
G = nx.DiGraph() if directed else nx.Graph()
for _, row in df_filtered.iterrows():
    G.add_edge(row["source"], row["target"], weight=row.get("weight", 1))

# ================== METRICS ==================
st.sidebar.header("📈 Metrics")
metrics_choice = st.sidebar.multiselect(
    "Select Metrics", ["Degree", "Betweenness", "Closeness", "Eigenvector"], default=["Degree"]
)

metrics = {}
if "Degree" in metrics_choice:
    metrics["Degree"] = nx.degree_centrality(G)
if "Betweenness" in metrics_choice:
    metrics["Betweenness"] = nx.betweenness_centrality(G)
if "Closeness" in metrics_choice:
    metrics["Closeness"] = nx.closeness_centrality(G)
if "Eigenvector" in metrics_choice:
    try:
        metrics["Eigenvector"] = nx.eigenvector_centrality(G)
    except nx.NetworkXException:
        st.warning("⚠️ Eigenvector centrality failed (disconnected graph).")

# Convert metrics to DataFrame
if metrics:
    metrics_df = pd.DataFrame(metrics)
    st.subheader("📌 Node Metrics")
    st.dataframe(metrics_df)

    # Download metrics as CSV
    csv_buffer = StringIO()
    metrics_df.to_csv(csv_buffer)
    st.download_button("⬇️ Download Metrics CSV", data=csv_buffer.getvalue(), file_name="metrics.csv", mime="text/csv")

# ================== VISUALIZATION ==================
st.subheader("🌍 Network Graph")

def visualize_graph(G, metrics):
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
    net.force_atlas_2based()

    # Add nodes with metric values
    for node in G.nodes():
        title = "<br>".join([f"{m}: {round(v.get(node,0),3)}" for m,v in metrics.items()])
        net.add_node(node, label=node, title=title, size=15 + (metrics.get("Degree", {}).get(node, 0) * 50))

    # Add edges
    for source, target, data in G.edges(data=True):
        net.add_edge(source, target, value=data.get("weight", 1))

    return net

net = visualize_graph(G, metrics)

# Render directly inside Streamlit
html = net.generate_html()
st.components.v1.html(html, height=650, scrolling=True)

# ================== EGO NETWORK ==================
st.sidebar.header("👤 Ego Network")
ego_node = st.sidebar.selectbox("Select a node to focus", ["None"] + list(G.nodes()))
if ego_node != "None":
    st.subheader(f"🔎 Ego Network for {ego_node}")
    ego_graph = nx.ego_graph(G, ego_node, radius=1)
    ego_net = visualize_graph(ego_graph, metrics)
    ego_html = ego_net.generate_html()
    st.components.v1.html(ego_html, height=500, scrolling=True)

# ================== DOWNLOAD GRAPH ==================
st.sidebar.header("💾 Export")
html_str = net.generate_html()
b64 = base64.b64encode(html_str.encode()).decode()
href = f'<a href="data:text/html;base64,{b64}" download="network_graph.html">⬇️ Download Network Graph HTML</a>'
st.sidebar.markdown(href, unsafe_allow_html=True)

