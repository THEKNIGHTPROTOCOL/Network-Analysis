
# 🕸️ Network Analysis

## 📖 Overview
This project performs **network analysis of communication patterns** using graph theory.  
It uncovers **hidden structures, influential actors, and community clusters** in complex networks.  

Built with **Streamlit**, it provides an interactive dashboard for exploring communication data and visualizing networks.  

---

## 🔗 Links
- [📂 GitHub Repository](https://github.com/YOUR_USERNAME/network-analysis)  
- [🌐 Live Demo on Streamlit](https://network-analysis-mgdfibdiqg9p6uxytyn5tz.streamlit.app/)  

---

### 🚀 Features

✅ Upload or use sample dataset (`comms.csv`)  
✅ Compute **network centrality metrics**:
- **Degree Centrality** → Most connected actors  
- **Betweenness Centrality** → Information brokers / couriers  
- **Closeness Centrality** → Fastest spreaders  
✅ Perform **Community Detection** (clusters of tightly connected nodes)  
✅ Visualize the network graph with:
- Node size = centrality importance  
- Node color = community group  

---





### 🛠️ Installation

Clone this repository:

git clone https://github.com/YOUR_USERNAME/network-analysis.git
cd network-analysis

Run the App
streamlit run app.py


Then open the provided local URL in your browser.
The dashboard will load with sample data or any uploaded .csv.

---

### 📊 Sample Dataset

Sample dataset (data/comms.csv) simulating leaders, couriers, recruits, and members:

source,target,weight
Leader1,Recruit1,10
Leader1,Recruit2,8
Leader1,Courier1,5
Recruit1,Member1,3
Recruit1,Member2,4
Recruit2,Member3,2
Recruit2,Member4,6
Courier1,Leader2,7
Leader2,Recruit3,9
Leader2,Recruit4,5
Recruit3,Member5,4
Recruit4,Member6,3
Recruit4,Member7,2
Courier1,Leader3,4
Leader3,Recruit5,8
Leader3,Recruit6,7
Recruit5,Member8,3
Recruit6,Member9,4
Recruit6,Member10,2
Member2,Member8,1
Member3,Member7,2
Leader2,Leader3,6
Leader3,Leader1,4

---

### 🌐 Example Dashboard Screenshot

![](https://github.com/user-attachments/assets/03e98026-d64b-43f9-938d-5405296a180f)
![e](https://github.com/user-attachments/assets/50a59815-ca71-427b-b9b2-4138358b22aa)


---

### 📌 Insights

Leaders → highest degree centrality, most connections

Couriers → high betweenness, bridges between groups

Communities → tightly connected clusters (detected with modularity)

Cross-links between leaders → inter-group collaboration

---

### ⚡ Tech Stack

Streamlit
 – Interactive dashboard

Pandas
 – Data processing

NetworkX
 – Graph analysis

Matplotlib

 – Visualization

---

### 📌 Future Improvements

Time-based network evolution (who communicates when)

Integration with real-world datasets (GTD, Kaggle)

Export insights to PDF/CSV reports

Advanced community detection (Louvain, Girvan–Newman)

---

## 📂 Project Structure
```bash
network-analysis/
│── app.py                 # Main Streamlit app
│── requirements.txt       # Dependencies
│── data/
│    └── comms.csv         # Example dataset
│── README.md              # Documentation
