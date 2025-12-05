import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import json

# Page configuration
st.set_page_config(page_title="Network Pathfinding Simulator", layout="wide")

# Initialize session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.DiGraph()
if 'edges' not in st.session_state:
    st.session_state.edges = []
if 'graph_name' not in st.session_state:
    st.session_state.graph_name = "My Network"
if 'animation_speed' not in st.session_state:
    st.session_state.animation_speed = 500
if 'node_positions' not in st.session_state:
    st.session_state.node_positions = {}

# Title
st.title("🔗 Network Pathfinding Simulator")
st.markdown("Build your network and find optimal paths between nodes")

# Sidebar - Graph Builder
st.sidebar.header("📊 Graph Builder")
st.sidebar.markdown("---")

with st.sidebar:
    # Graph Name
    graph_name = st.text_input("📝 Graph Name", value=st.session_state.graph_name, key="graph_name_input")
    if graph_name != st.session_state.graph_name:
        st.session_state.graph_name = graph_name
    
    st.markdown("---")
    st.subheader("Add Connection")
    
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Source Node", key="source")
    with col2:
        target = st.text_input("Target Node", key="target")
    
    weight = st.number_input("Weight (Cost/Time)", min_value=0.1, value=1.0, step=0.1, key="weight")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ Add Connection", use_container_width=True):
            if source and target:
                if source.strip() and target.strip():
                    st.session_state.graph.add_edge(source.strip(), target.strip(), weight=weight)
                    st.session_state.edges.append((source.strip(), target.strip(), weight))
                    st.success(f"Added: {source} → {target} (Weight: {weight})")
                    st.rerun()
                else:
                    st.error("Please enter valid node names")
            else:
                st.error("Please fill in both nodes")
    
    with col_btn2:
        if st.button("🗑️ Reset Graph", use_container_width=True):
            st.session_state.graph = nx.DiGraph()
            st.session_state.edges = []
            st.session_state.node_positions = {}
            st.success("Graph cleared!")
            st.rerun()
    
    st.markdown("---")
    st.subheader("📋 Current Connections")
    if st.session_state.edges:
        for src, tgt, wgt in st.session_state.edges:
            st.text(f"{src} → {tgt} : {wgt}")
    else:
        st.info("No connections yet")
    
    st.markdown("---")
    st.metric("Total Nodes", st.session_state.graph.number_of_nodes())
    st.metric("Total Edges", st.session_state.graph.number_of_edges())

# Main area - Simulation Controls
if st.session_state.graph.number_of_nodes() > 0:
    nodes_list = sorted(list(st.session_state.graph.nodes()))
    
    st.header("🎯 Pathfinding Simulation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        start_node = st.selectbox("Select Start Node", options=nodes_list, key="start")
    
    with col2:
        end_node = st.selectbox("Select Destination Node", options=nodes_list, key="end")
    
    with col3:
        algorithm = st.radio(
            "Algorithm",
            options=["Find Shortest Path (Dijkstra)", "Find Critical Path (Longest Path)"],
            key="algorithm"
        )
    
    with col4:
        animation_speed = st.select_slider(
            "Animation Speed",
            options=[100, 300, 500, 800, 1200, 2000],
            value=st.session_state.animation_speed,
            format_func=lambda x: f"{'Very Fast' if x==100 else 'Fast' if x==300 else 'Normal' if x==500 else 'Slow' if x==800 else 'Very Slow' if x==1200 else 'Ultra Slow'}",
            key="speed_slider"
        )
        st.session_state.animation_speed = animation_speed
    
    run_simulation = st.button("🚀 Run Simulation", type="primary", use_container_width=True)
    
    st.markdown("---")
    
    # Calculate path if simulation is run
    path = None
    path_cost = None
    algo_name = None
    visited_nodes = []
    
    if run_simulation and start_node and end_node:
        try:
            if algorithm == "Find Shortest Path (Dijkstra)":
                path = nx.shortest_path(st.session_state.graph, source=start_node, target=end_node, weight='weight')
                path_cost = nx.shortest_path_length(st.session_state.graph, source=start_node, target=end_node, weight='weight')
                algo_name = "Shortest Path (Dijkstra)"
                
                # Simulate visited nodes for Dijkstra (BFS-like exploration)
                visited_nodes = list(nx.single_source_shortest_path(st.session_state.graph, start_node).keys())
            else:
                G_neg = st.session_state.graph.copy()
                for u, v, data in G_neg.edges(data=True):
                    data['weight'] = -data['weight']
                
                path = nx.shortest_path(G_neg, source=start_node, target=end_node, weight='weight')
                path_cost = sum(st.session_state.graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
                algo_name = "Longest Path (Critical Path)"
                
                # For longest path, visited nodes are similar to shortest path exploration
                visited_nodes = list(nx.single_source_shortest_path(G_neg, start_node).keys())
            
            st.success(f"✅ {algo_name} found!")
                
        except nx.NetworkXNoPath:
            st.error(f"❌ No path exists between **{start_node}** and **{end_node}**")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Prepare data for visualization
    nodes_data = []
    edges_data = []
    
    # Convert NetworkX graph to node/edge lists
    for node in st.session_state.graph.nodes():
        # Get or generate position for this node
        if node not in st.session_state.node_positions:
            # Generate initial random position
            import random
            st.session_state.node_positions[node] = {
                'x': random.uniform(-300, 300),
                'y': random.uniform(-200, 200)
            }
        
        nodes_data.append({
            'id': node,
            'label': node,
            'x': st.session_state.node_positions[node]['x'],
            'y': st.session_state.node_positions[node]['y'],
            'inPath': path is not None and node in path,
            'isStart': node == start_node if path else False,
            'isEnd': node == end_node if path else False
        })
    
    for u, v, data in st.session_state.graph.edges(data=True):
        is_in_path = False
        if path:
            for i in range(len(path)-1):
                if path[i] == u and path[i+1] == v:
                    is_in_path = True
                    break
        
        edges_data.append({
            'from': u,
            'to': v,
            'weight': data['weight'],
            'inPath': is_in_path
        })
    
    # Create interactive visualization using vis.js
    graph_data = {
        'nodes': nodes_data,
        'edges': edges_data,
        'path': path if path else [],
        'visitedNodes': visited_nodes if visited_nodes else [],
        'animationSpeed': st.session_state.animation_speed,
        'graphName': st.session_state.graph_name,
        'algoName': algo_name if algo_name else "",
        'startNode': start_node if path else "",
        'endNode': end_node if path else ""
    }
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #0a0a0a;
                font-family: 'Arial', sans-serif;
            }}
            #mynetwork {{
                width: 100%;
                height: 600px;
                background: #000000;
                border: 3px solid #00ff88;
                box-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
            }}
            #graph-title {{
                position: absolute;
                top: 15px;
                left: 20px;
                color: #00ff88;
                font-size: 26px;
                font-weight: bold;
                text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
                z-index: 1000;
                background: rgba(0, 0, 0, 0.9);
                padding: 12px 25px;
                border-radius: 10px;
                border: 2px solid #00ff88;
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
            }}
            #status-box {{
                position: absolute;
                bottom: 15px;
                left: 20px;
                color: #ffffff;
                font-size: 14px;
                z-index: 1000;
                background: rgba(0, 0, 0, 0.95);
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #00ff88;
                min-width: 250px;
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
            }}
            .status-item {{
                margin: 8px 0;
                font-size: 13px;
            }}
            .status-label {{
                color: #00ff88;
                font-weight: bold;
            }}
            #path-display {{
                position: absolute;
                bottom: 15px;
                right: 20px;
                color: #ffffff;
                font-size: 14px;
                z-index: 1000;
                background: rgba(0, 0, 0, 0.95);
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #ff00ff;
                max-width: 400px;
                box-shadow: 0 0 20px rgba(255, 0, 255, 0.4);
            }}
            .path-title {{
                color: #ff00ff;
                font-weight: bold;
                font-size: 16px;
                margin-bottom: 10px;
                text-shadow: 0 0 10px rgba(255, 0, 255, 0.8);
            }}
            .path-steps {{
                color: #00ffff;
                font-size: 13px;
                line-height: 1.8;
            }}
            .path-arrow {{
                color: #ffff00;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div id="graph-title"></div>
        <div id="mynetwork"></div>
        <div id="status-box">
            <div class="status-item"><span class="status-label">Status:</span> <span id="status-text">Ready</span></div>
            <div class="status-item"><span class="status-label">Current Node:</span> <span id="current-node">-</span></div>
            <div class="status-item"><span class="status-label">Nodes Explored:</span> <span id="explored-count">0</span></div>
            <div class="status-item"><span class="status-label">Progress:</span> <span id="progress-text">0%</span></div>
        </div>
        <div id="path-display" style="display: none;">
            <div class="path-title">🎯 Path Traversed</div>
            <div class="path-steps" id="path-steps"></div>
        </div>
        <script type="text/javascript">
            var graphData = {json.dumps(graph_data)};
            
            // Set graph title
            document.getElementById('graph-title').textContent = graphData.graphName + (graphData.algoName ? ' - ' + graphData.algoName : '');
            
            // Create nodes
            var nodes = new vis.DataSet(
                graphData.nodes.map(function(node) {{
                    var nodeColor = '#1e90ff'; // Default blue
                    var borderColor = '#0066cc';
                    
                    if (node.isStart) {{
                        nodeColor = '#00ff00'; // Green for start
                        borderColor = '#00cc00';
                    }} else if (node.isEnd) {{
                        nodeColor = '#ff0000'; // Red for end
                        borderColor = '#cc0000';
                    }}
                    
                    return {{
                        id: node.id,
                        label: node.label,
                        x: node.x,
                        y: node.y,
                        color: {{
                            background: nodeColor,
                            border: borderColor,
                            highlight: {{
                                background: '#00ffff',
                                border: '#00cccc'
                            }},
                            hover: {{
                                background: '#00ffff',
                                border: '#00cccc'
                            }}
                        }},
                        font: {{
                            color: '#ffffff',
                            size: 18,
                            face: 'arial',
                            bold: true
                        }},
                        size: 35,
                        shadow: {{
                            enabled: true,
                            size: 15,
                            x: 3,
                            y: 3,
                            color: 'rgba(0, 255, 255, 0.5)'
                        }},
                        physics: false
                    }};
                }})
            );
            
            // Create edges
            var edges = new vis.DataSet(
                graphData.edges.map(function(edge) {{
                    return {{
                        from: edge.from,
                        to: edge.to,
                        label: edge.weight.toFixed(1),
                        arrows: 'to',
                        color: {{
                            color: '#666666',
                            highlight: '#00ffff'
                        }},
                        width: 2,
                        font: {{
                            size: 14,
                            align: 'middle',
                            background: '#000000',
                            color: '#ffff00',
                            strokeWidth: 2,
                            strokeColor: '#000000'
                        }},
                        smooth: {{
                            type: 'curvedCW',
                            roundness: 0.2
                        }}
                    }};
                }})
            );
            
            var container = document.getElementById('mynetwork');
            var data = {{
                nodes: nodes,
                edges: edges
            }};
            
            var options = {{
                physics: {{
                    enabled: false
                }},
                interaction: {{
                    dragNodes: true,
                    dragView: true,
                    zoomView: true,
                    hover: true,
                    hoverConnectedEdges: true,
                    selectConnectedEdges: false,
                    navigationButtons: false,
                    keyboard: false
                }},
                manipulation: {{
                    enabled: false
                }},
                edges: {{
                    arrows: {{
                        to: {{
                            enabled: true,
                            scaleFactor: 1.2
                        }}
                    }},
                    smooth: {{
                        type: 'curvedCW',
                        roundness: 0.2
                    }}
                }},
                nodes: {{
                    shape: 'dot',
                    borderWidth: 3,
                    borderWidthSelected: 4
                }}
            }};
            
            var network = new vis.Network(container, data, options);
            
            // Save positions when nodes are dragged
            network.on('dragEnd', function(params) {{
                if (params.nodes.length > 0) {{
                    var nodeId = params.nodes[0];
                    var position = network.getPositions([nodeId])[nodeId];
                    
                    // Send position back to Streamlit
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        nodeId: nodeId,
                        position: position
                    }}, '*');
                }}
            }});
            
            // Animation function
            async function animatePathfinding() {{
                if (graphData.path.length === 0) return;
                
                var animSpeed = graphData.animationSpeed;
                var path = graphData.path;
                var visitedNodes = graphData.visitedNodes;
                
                document.getElementById('status-text').textContent = 'Exploring...';
                document.getElementById('status-text').style.color = '#ffff00';
                
                // First, animate exploration of visited nodes
                for (var i = 0; i < visitedNodes.length; i++) {{
                    var nodeId = visitedNodes[i];
                    document.getElementById('current-node').textContent = nodeId;
                    document.getElementById('explored-count').textContent = (i + 1);
                    document.getElementById('progress-text').textContent = Math.round((i + 1) / visitedNodes.length * 50) + '%';
                    
                    // Skip start and end nodes in exploration phase
                    if (nodeId !== graphData.startNode && nodeId !== graphData.endNode) {{
                        nodes.update({{
                            id: nodeId,
                            color: {{
                                background: '#ffaa00',
                                border: '#ff8800'
                            }},
                            shadow: {{
                                enabled: true,
                                size: 20,
                                color: 'rgba(255, 170, 0, 0.8)'
                            }}
                        }});
                    }}
                    
                    await new Promise(resolve => setTimeout(resolve, animSpeed / 2));
                }}
                
                document.getElementById('status-text').textContent = 'Path Found!';
                document.getElementById('status-text').style.color = '#00ff00';
                
                // Reset explored nodes
                for (var i = 0; i < visitedNodes.length; i++) {{
                    var nodeId = visitedNodes[i];
                    if (path.indexOf(nodeId) === -1 && nodeId !== graphData.startNode && nodeId !== graphData.endNode) {{
                        nodes.update({{
                            id: nodeId,
                            color: {{
                                background: '#1e90ff',
                                border: '#0066cc'
                            }},
                            shadow: {{
                                enabled: true,
                                size: 15,
                                color: 'rgba(0, 255, 255, 0.5)'
                            }}
                        }});
                    }}
                }}
                
                await new Promise(resolve => setTimeout(resolve, animSpeed));
                
                // Show path display
                document.getElementById('path-display').style.display = 'block';
                var pathStepsDiv = document.getElementById('path-steps');
                pathStepsDiv.innerHTML = '';
                
                // Now animate the final path
                for (var i = 0; i < path.length; i++) {{
                    var nodeId = path[i];
                    document.getElementById('current-node').textContent = nodeId;
                    document.getElementById('progress-text').textContent = Math.round(50 + (i + 1) / path.length * 50) + '%';
                    
                    // Update path display
                    if (i > 0) {{
                        pathStepsDiv.innerHTML += '<span class="path-arrow"> → </span>';
                    }}
                    pathStepsDiv.innerHTML += '<span style="color: #00ff88; font-weight: bold;">' + nodeId + '</span>';
                    
                    // Don't recolor start and end nodes
                    if (nodeId !== graphData.startNode && nodeId !== graphData.endNode) {{
                        nodes.update({{
                            id: nodeId,
                            color: {{
                                background: '#ff00ff',
                                border: '#cc00cc'
                            }},
                            size: 40,
                            shadow: {{
                                enabled: true,
                                size: 25,
                                color: 'rgba(255, 0, 255, 0.9)'
                            }}
                        }});
                    }}
                    
                    if (i > 0) {{
                        // Highlight the edge with bright color
                        edges.update({{
                            from: path[i-1],
                            to: path[i],
                            color: {{
                                color: '#00ffff'
                            }},
                            width: 5,
                            shadow: {{
                                enabled: true,
                                size: 10,
                                color: 'rgba(0, 255, 255, 0.8)'
                            }},
                            font: {{
                                background: '#ffff00',
                                color: '#000000',
                                size: 16,
                                strokeWidth: 0
                            }}
                        }});
                    }}
                    
                    await new Promise(resolve => setTimeout(resolve, animSpeed));
                }}
                
                document.getElementById('status-text').textContent = 'Complete!';
                document.getElementById('status-text').style.color = '#00ff00';
                document.getElementById('progress-text').textContent = '100%';
            }}
            
            // Start animation if path exists
            if (graphData.path.length > 0) {{
                setTimeout(animatePathfinding, 500);
            }}
        </script>
    </body>
    </html>
    """
    
    components.html(html_content, height=650, scrolling=False)
    
    # Display path details if path exists
    if path and path_cost is not None:
        st.markdown("### 📊 Final Path Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Path Length (Hops)", len(path) - 1)
        with col2:
            st.metric("Total Cost/Duration", f"{path_cost:.2f}")
        with col3:
            st.metric("Nodes Traversed", len(path))
        with col4:
            st.metric("Nodes Explored", len(visited_nodes))
        
        # Show detailed path with weights
        st.markdown("#### 🛤️ Detailed Path Journey")
        path_details = []
        for i in range(len(path) - 1):
            edge_weight = st.session_state.graph[path[i]][path[i+1]]['weight']
            path_details.append(f"**{path[i]}** →[{edge_weight}]→ **{path[i+1]}**")
        
        st.info(" | ".join(path_details))

else:
    st.info("👈 Start by adding connections in the sidebar to build your network graph")
    st.markdown("""
    ### How to use:
    1. **Name your graph** at the top of the sidebar
    2. **Add nodes and edges** using the connection builder
    3. **Select start and destination** nodes
    4. **Choose an algorithm**:
       - **Shortest Path (Dijkstra)**: Finds the path with minimum total weight
       - **Longest Path (Critical Path)**: Finds the path with maximum total weight (useful for bottleneck analysis)
    5. **Adjust animation speed** to watch the pathfinding process
    6. **Run the simulation** to see the animated pathfinding
    
    ### Interactive Controls:
    - **Drag nodes**: Click and hold any node to move it around
    - **Pan view**: Click and drag on empty space to pan
    - **Zoom**: Use mouse wheel to zoom in/out
    
    ### Visual Guide:
    - **Green Node**: Start point
    - **Red Node**: Destination
    - **Blue Nodes**: Regular nodes
    - **Orange Glow**: Nodes being explored
    - **Purple/Magenta Glow**: Final path nodes
    - **Cyan/Bright Edges**: Path edges with glowing effect
    
    ### Example:
    Try creating a network like:
    - A → B (weight: 2)
    - A → C (weight: 5)
    - B → D (weight: 3)
    - C → D (weight: 1)
    - Then find the path from A to D and watch the animation!
    """)
