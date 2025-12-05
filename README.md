# 🔗 Network Pathfinding Simulator

**An interactive visualization tool to simulate, analyze, and understand network routing algorithms and Critical Path Methods (CPM).**

[](https://www.google.com/search?q=https://your-app-url-here.streamlit.app/)

## 📝 Introduction

The **Network Pathfinding Simulator** is a web-based application designed to demonstrate how data (or tasks) flow through a complex system. Whether you are a student learning about computer networks, a project manager studying dependencies, or a developer interested in graph theory, this tool provides a visual playground to test different scenarios.

Built with **Python** and **Streamlit**, it uses **NetworkX** for powerful graph calculations and **Vis.js** for beautiful, animated rendering of the network.

## ⚙️ How It Works

The application transforms abstract mathematical graphs into an interactive visual simulation:

1.  **Graph Construction:** Users manually build a network by adding **Nodes** (locations/tasks) and **Edges** (connections/dependencies) with specific **Weights** (time/cost).
2.  **Algorithm Selection:** The core engine allows users to switch between two opposing logic models:
      * **Dijkstra's Algorithm:** Finds the *Shortest Path* (Efficiency).
      * **Critical Path Method:** Finds the *Longest Path* (Bottlenecks).
3.  **Simulation:** The app animates the traversal process, highlighting nodes as they are "explored" and finally illuminating the resulting path in neon colors.

## 🚀 Key Features

  * **Interactive Builder:** Add connections dynamically via the sidebar.
  * **Dual Algorithms:** Compare "Shortest Path" (Networking logic) vs. "Critical Path" (Project Management logic) on the exact same dataset.
  * **Visual Animation:** Watch the algorithm "think" with adjustable animation speeds.
  * **Drag & Drop UI:** Interactive canvas allows you to rearrange nodes to better visualize the structure.
  * **Real-Time Metrics:** Instantly calculates total cost, hop count, and node traversal stats.

## 🎯 Real-World Applications

This simulation models problems found in various industries:

  * **Computer Networking:** Simulating OSPF (Open Shortest Path First) routing to find the fastest way to send data packets.
  * **Project Management:** Identifying the "Critical Path" in a schedule—the sequence of tasks that dictates the minimum project duration.
  * **Logistics & Supply Chain:** Finding bottlenecks in delivery routes where delays could be catastrophic.

## ⚖️ Advantages

1.  **Educational Value:** Converts invisible algorithmic logic into a visible, step-by-step animation.
2.  **Immediate Feedback:** Users can change a single weight (e.g., increase traffic on one route) and immediately see how the path changes.
3.  **No Installation:** Fully web-based; runs in any browser.

## 🚧 Limitations

While this tool is a powerful simulation, it is a demonstration prototype with the following limitations:

  * **Volatile Memory:** The graph resets if the browser page is refreshed (no backend database integration).
  * **Scale:** Designed for educational graphs (5-50 nodes). Rendering performance may degrade with hundreds of nodes.
  * **Directed Graphs Only:** The simulation assumes directionality (A $\to$ B is different from B $\to$ A), which is standard for Critical Path but may differ from simple road maps.

## 🔮 Future Prospects

To evolve this project into a full-scale tool, the following features are planned:

  * **Save/Load Functionality:** Export graphs to JSON so users can save their work.
  * **Preset Scenarios:** Pre-loaded complex graph templates (e.g., "Server Cluster", "House Construction Project").
  * **Cycle Detection:** Automatic warning systems for deadlocks (loops).
  * **More Algorithms:** Implementation of A\* Search and Bellman-Ford.

## 🛠️ Installation (Run Locally)

If you wish to run this on your own machine instead of the cloud:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/network-simulator.git
    cd network-simulator
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**

    ```bash
    streamlit run app.py
    ```

## 🏁 Conclusion

The **Network Pathfinding Simulator** bridges the gap between theory and practice. By visualizing the "Critical Path," it helps users understand that optimizing the *fastest* parts of a system is useless if the *bottlenecks* are ignored. It serves as a compact, interactive demonstration of graph theory fundamentals.

-----
