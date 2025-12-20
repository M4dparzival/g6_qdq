from flask import Flask, request, render_template, session, jsonify
from algorithms import deque, queue, binarytree, binarysearchtree, graph as graph_module
import os

app = Flask(__name__)
app.secret_key = 'SDIYBT'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/q', methods=['GET', 'POST'])
def q():
    message = ""
    removed_message = ""

    if request.method == 'GET':
        session['queue_data'] = []
        session['message'] = ""
        session['removed_message'] = ""

    # Rebuild queue from session data
    my_queue = queue.Queue()
    for item in session['queue_data']:
        my_queue.enqueue(item)

    if request.method == 'POST':
        operation = request.form.get('operation')
        data = request.form.get('inputdata')

        if operation == 'enqueue' and data:
            my_queue.enqueue(data)
            message = f"Added {data} to queue"
            session['queue_data'] = my_queue.display()
        elif operation == 'dequeue':
            if my_queue.display():
                removed_item = my_queue.dequeue()
                removed_message = f"Removed {removed_item} from queue"
                session['queue_data'] = my_queue.display()
            else:
                message = "Queue is empty"

    queue_items = my_queue.display()
    return render_template('queue.html', queue_items=queue_items, message=message, removed_message=removed_message)

@app.route('/dq', methods=['GET', 'POST'])
def dq():
    message = ""
    removed_message = ""

    # Initialize deque in session
    if request.method == 'GET':
        session['deque_data'] = []
        session['message'] = ""
        session['removed_message'] = ""

    if 'deque_data' not in session:
        session['deque_data'] = []

    # Rebuild deque from session data
    my_deque = deque.Deque()
    for item in session['deque_data']:
        my_deque.add_rear(item)

    if request.method == 'POST':
        data = request.form.get('inputdata', '').strip()
        operation = request.form.get('operation')

        if operation == 'add_front' and data:
            my_deque.add_front(data)
        elif operation == 'add_rear' and data:
            my_deque.add_rear(data)
        elif operation == 'remove_front':
            removed = my_deque.remove_front()
            removed_message = f"Removed from front: {removed}" if removed else "Deque is empty."
        elif operation == 'remove_rear':
            removed = my_deque.remove_rear()
            removed_message = f"Removed from rear: {removed}" if removed else "Deque is empty."

        # Save updated deque back to session
        session['deque_data'] = my_deque.display()
        session.modified = True
    else:
        message = session.get('message', '')
        removed_message = session.get('removed_message', '')

    deque_items = my_deque.display()
    return render_template('deque.html', deque_items=deque_items, message=message, removed_message=removed_message)

@app.route('/tree', methods=['GET', 'POST'])
def tree():
    message = ""
    traversal_result = ""
    search_result = ""
    tree_data = None

    if request.method == 'GET':
        session['tree'] = None

    if 'tree' not in session:
        session['tree'] = None

    if request.method == 'POST':
        operation = request.form.get('operation')
        value = request.form.get('value', '').strip()
        starting_node_value = request.form.get('starting_node', '').strip()
        action = request.form.get('action')

        # Handle clear action
        if action == 'clear':
            session['tree'] = None
            session.modified = True
            message = "Tree cleared successfully"
            return render_template('binarytree.html', tree=None, message=message)
        
        operation = request.form.get('operation')
        value = request.form.get('value', '').strip()
        starting_node_value = request.form.get('starting_node', '').strip()

        # Handle insertions
        if (operation == 'insert_left' or operation == 'insert_right') and value:
            bt = binarytree.BinaryTree()
            
            # If tree is empty, create root
            if session['tree'] is None:
                bt.root = binarytree.Node(value)
                session['tree'] = node_to_dict(bt.root)
                session.modified = True
                message = f"Inserted {value}"
            else:
                # Tree already exists, insert into it
                bt.root = node_from_dict(session['tree'])
                
                # Find starting node
                start_node = bt.root
                if starting_node_value:
                    start_node = bt.find_node_by_value(starting_node_value)
                    if not start_node:
                        message = f"Starting node {starting_node_value} not found"
                        tree_data = session['tree']
                        return render_template('binarytree.html', tree=tree_data, message=message)
                
                # Insert based on operation
                if operation == 'insert_left':
                    bt.insert_left(value, start_node)
                    if starting_node_value:
                        message = f"Inserted {value} to the left of {start_node.value}"
                    else:
                        message = f"Inserted {value}"
                else:  # insert_right
                    bt.insert_right(value, start_node)
                    if starting_node_value:
                        message = f"Inserted {value} to the right of {start_node.value}"
                    else:
                        message = f"Inserted {value}"
                
                session['tree'] = node_to_dict(bt.root)
                session.modified = True
        
        # Handle search
        elif operation == 'search' and value:
            if session['tree']:
                bt = binarytree.BinaryTree()
                bt.root = node_from_dict(session['tree'])
                
                if bt.search(value):
                    search_result = f"✓ Found: {value} exists in the tree"
                else:
                    search_result = f"✗ Not Found: {value} does not exist in the tree"
            else:
                message = "Tree is empty"
        
        # Handle delete
        elif operation == 'delete' and value:
            if session['tree']:
                bt = binarytree.BinaryTree()
                bt.root = node_from_dict(session['tree'])
                
                if bt.delete(value):
                    message = f"Deleted {value} from tree"
                    session['tree'] = node_to_dict(bt.root)
                    session.modified = True
                else:
                    message = f"Could not delete {value} - not found in tree"
            else:
                message = "Tree is empty"
        
        # Handle traversals
        elif operation in ['preorder_traversal', 'inorder_traversal', 'postorder_traversal']:
            if session['tree']:
                bt = binarytree.BinaryTree()
                bt.root = node_from_dict(session['tree'])
                
                if operation == 'preorder_traversal':
                    result = bt.preorder_traversal(bt.root).strip()
                    traversal_result = f"Preorder: {result}"
                elif operation == 'inorder_traversal':
                    result = bt.inorder_traversal(bt.root).strip()
                    traversal_result = f"Inorder: {result}"
                elif operation == 'postorder_traversal':
                    result = bt.postorder_traversal(bt.root).strip()
                    traversal_result = f"Postorder: {result}"
            else:
                message = "Tree is empty"

    tree_data = session['tree']
    return render_template('binarytree.html', tree=tree_data, message=message, traversal_result=traversal_result, search_result=search_result)

def node_to_dict(node):
    """Convert Node object to dictionary for JSON serialization"""
    if node is None:
        return None
    return {
        'value': node.value,
        'left': node_to_dict(node.left),
        'right': node_to_dict(node.right)
    }

def node_from_dict(data):
    """Convert dictionary back to Node object"""
    if data is None:
        return None
    return binarytree.Node(
        data['value'],
        node_from_dict(data['left']),
        node_from_dict(data['right'])
    )

@app.route('/bst', methods=['GET', 'POST'])
def bst():
    message = ""
    traversal_result = ""
    search_result = ""
    tree_data = None

    if request.method == 'GET':
        session['bst'] = None

    if 'bst' not in session:
        session['bst'] = None

    if request.method == 'POST':
        operation = request.form.get('operation')
        value = request.form.get('value', '').strip()
        action = request.form.get('action')

        # Handle clear action
        if action == 'clear':
            session['bst'] = None
            session.modified = True
            message = "Tree cleared successfully"
            return render_template('binarysearchtree.html', tree=None, message=message)

        # Handle insert
        if operation == 'insert' and value:
            bst_tree = binarysearchtree.BinarySearchTree()

            # If tree is empty, create root
            if session['bst'] is None:
                bst_tree.insert(value)
                session['bst'] = node_to_dict(bst_tree.root)
                session.modified = True
                message = f"Inserted {value}"
            else:
                # Tree already exists, insert into it
                bst_tree.root = node_from_dict(session['bst'])
                bst_tree.insert(value)
                session['bst'] = node_to_dict(bst_tree.root)
                session.modified = True
                message = f"Inserted {value}"

        # Handle search
        elif operation == 'search' and value:
            if session['bst']:
                bst_tree = binarysearchtree.BinarySearchTree()
                bst_tree.root = node_from_dict(session['bst'])

                if bst_tree.search(value):
                    search_result = f"✓ Found: {value} exists in the tree"
                else:
                    search_result = f"✗ Not Found: {value} does not exist in the tree"
            else:
                message = "Tree is empty"

        # Handle delete
        elif operation == 'delete' and value:
            if session['bst']:
                bst_tree = binarysearchtree.BinarySearchTree()
                bst_tree.root = node_from_dict(session['bst'])
                bst_tree.delete(value)
                session['bst'] = node_to_dict(bst_tree.root)
                session.modified = True
                message = f"Deleted {value} from tree"
            else:
                message = "Tree is empty"

        # Handle traversals
        elif operation in ['preorder_traversal', 'inorder_traversal', 'postorder_traversal']:
            if session['bst']:
                bst_tree = binarysearchtree.BinarySearchTree()
                bst_tree.root = node_from_dict(session['bst'])

                if operation == 'preorder_traversal':
                    result = bst_tree.preorder_traversal().strip()
                    traversal_result = f"Preorder: {result}"
                elif operation == 'inorder_traversal':
                    result = bst_tree.inorder_traversal().strip()
                    traversal_result = f"Inorder: {result}"
                elif operation == 'postorder_traversal':
                    result = bst_tree.postorder_traversal().strip()
                    traversal_result = f"Postorder: {result}"
            else:
                message = "Tree is empty"

    tree_data = session['bst']
    return render_template('binarysearchtree.html', tree=tree_data, message=message, traversal_result=traversal_result, search_result=search_result)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    message = ""
    result = ""
    graph_data = None

    if request.method == 'GET':
        session['graph'] = {}

    if 'graph' not in session:
        session['graph'] = {}

    if request.method == 'POST':
        operation = request.form.get('operation')
        value = request.form.get('value', '').strip()
        action = request.form.get('action')

        # Handle clear action
        if action == 'clear':
            session['graph'] = {}
            session.modified = True
            message = "Graph cleared successfully"
            return render_template('graph.html', graph=None, message=message)

        g = graph.Graph()
        # Rebuild graph from session data
        for vertex in session['graph']:
            g.add_vertex(vertex)
        for source, neighbors in session['graph'].items():
            for target in neighbors:
                g.add_edge(source, target)

        if operation == 'add_vertex' and value:
            g.add_vertex(value)
            message = f"Added vertex {value}"
        elif operation == 'add_edge' and value:
            target = request.form.get('target', '').strip()
            if target:
                g.add_edge(value, target)
                message = f"Added edge from {value} to {target}"
            else:
                message = "Target vertex required for add_edge"
        elif operation == 'get_neighbors' and value:
            neighbors = g.get_neighbors(value)
            result = f"Neighbors of {value}: {neighbors}"
        elif operation == 'bfs_shortest_path' and value:
            goal = request.form.get('goal', '').strip()
            if goal:
                path = g.bfs_shortest_path(value, goal)
                if path:
                    result = f"Shortest path from {value} to {goal}: {path}"
                else:
                    result = f"No path found from {value} to {goal}"
            else:
                message = "Goal vertex required for BFS shortest path"

        # Save updated graph back to session
        session['graph'] = g.adj_list
        session.modified = True

    graph_data = session['graph']
    return render_template('graph.html', graph=graph_data, message=message, result=result)

@app.route('/mrt_map', methods=['GET', 'POST'])
def mrt_map():
    stations = [
        # MRT-3: Vertical line from North to South along EDSA
        {'name': 'North Avenue', 'x': 600, 'y': 50, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Quezon Avenue', 'x': 600, 'y': 130, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'GMA Kamuning', 'x': 600, 'y': 210, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Araneta Center-Cubao', 'x': 690, 'y': 290, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Santolan-Annapolis', 'x': 600, 'y': 370, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Ortigas', 'x': 600, 'y': 450, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Shaw Boulevard', 'x': 600, 'y': 530, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Boni', 'x': 600, 'y': 610, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Guadalupe', 'x': 600, 'y': 690, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Buendia', 'x': 600, 'y': 770, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Ayala', 'x': 600, 'y': 850, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Magallanes', 'x': 600, 'y': 930, 'line': 'MRT-3', 'color': 'blue'},
        {'name': 'Taft Avenue', 'x': 600, 'y': 1010, 'line': 'MRT-3', 'color': 'blue'},
        # LRT-1: Vertical line from North to South
        {'name': 'Fernando Poe Jr.', 'x': 200, 'y': 50, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Balintawak', 'x': 200, 'y': 90, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Monumento', 'x': 200, 'y': 130, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': '5th Avenue', 'x': 200, 'y': 170, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'R. Papa', 'x': 200, 'y': 210, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Abad Santos', 'x': 200, 'y': 250, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Blumentritt', 'x': 200, 'y': 290, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Tayuman', 'x': 200, 'y': 330, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Bambang', 'x': 200, 'y': 370, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Doroteo Jose', 'x': 200, 'y': 410, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Carriedo', 'x': 200, 'y': 450, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Central Terminal', 'x': 200, 'y': 490, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'United Nations', 'x': 200, 'y': 530, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Pedro Gil', 'x': 200, 'y': 570, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Quirino', 'x': 200, 'y': 610, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Vito Cruz', 'x': 200, 'y': 650, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Gil Puyat', 'x': 200, 'y': 690, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Libertad', 'x': 200, 'y': 730, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'EDSA', 'x': 200, 'y': 770, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Baclaran', 'x': 200, 'y': 810, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Redemptorist-Aseana', 'x': 200, 'y': 850, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'MIA', 'x': 200, 'y': 890, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'PITX', 'x': 200, 'y': 930, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Ninoy Aquino Avenue', 'x': 200, 'y': 970, 'line': 'LRT-1', 'color': 'yellow'},
        {'name': 'Dr. Santos', 'x': 200, 'y': 1010, 'line': 'LRT-1', 'color': 'yellow'},
        # LRT-2: Horizontal line from West to East at y=290
        {'name': 'Recto', 'x': 200, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Legarda', 'x': 270, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Pureza', 'x': 340, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'V. Mapa', 'x': 410, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'J. Ruiz', 'x': 480, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Gilmore', 'x': 550, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Betty Go-Belmonte', 'x': 620, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Araneta Center-Cubao', 'x': 690, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Anonas', 'x': 760, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Katipunan', 'x': 830, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Santolan', 'x': 900, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Marikina-Pasig', 'x': 970, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
        {'name': 'Antipolo', 'x': 1040, 'y': 290, 'line': 'LRT-2', 'color': 'purple'},
    ]

    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON data'}), 400

            start = data.get('start')
            goal = data.get('goal')

            if not start or not goal:
                return jsonify({'error': 'Start and goal stations are required'}), 400

            g = graph_module.Graph()
            for s in stations:
                g.add_vertex(s['name'])

            # MRT-3
            mrt3 = ["North Avenue", "Quezon Avenue", "GMA Kamuning", "Araneta Center-Cubao", "Santolan-Annapolis", "Ortigas", "Shaw Boulevard", "Boni", "Guadalupe", "Buendia", "Ayala", "Magallanes", "Taft Avenue"]
            for i in range(len(mrt3) - 1):
                g.add_edge(mrt3[i], mrt3[i + 1])

            # LRT-1: North to South
            lrt1 = ["Fernando Poe Jr.", "Balintawak", "Monumento", "5th Avenue", "R. Papa", "Abad Santos", "Blumentritt", "Tayuman", "Bambang", "Doroteo Jose", "Carriedo", "Central Terminal", "United Nations", "Pedro Gil", "Quirino", "Vito Cruz", "Gil Puyat", "Libertad", "EDSA", "Baclaran", "Redemptorist-Aseana", "PITX", "Dr. Santos"]
            for i in range(len(lrt1) - 1):
                g.add_edge(lrt1[i], lrt1[i + 1])

            # LRT-2: West to East
            lrt2 = ["Recto", "Legarda", "Pureza", "V. Mapa", "J. Ruiz", "Gilmore", "Betty Go-Belmonte", "Araneta Center-Cubao", "Anonas", "Katipunan", "Santolan", "Marikina-Pasig", "Antipolo"]
            for i in range(len(lrt2) - 1):
                g.add_edge(lrt2[i], lrt2[i + 1])

            # Add transfer connections
            g.add_edge("North Avenue", "North Avenue")  # LRT-1 to MRT-3 transfer at North Avenue
            g.add_edge("Recto", "Doroteo Jose")  # LRT-2 to LRT-1 transfer at Recto-Doroteo Jose
            g.add_edge("Araneta Center-Cubao", "Araneta Center-Cubao")  # MRT-3 to LRT-2 transfer (same station name)
            g.add_edge("EDSA", "Taft Avenue")  # LRT-1 to MRT-3 transfer at EDSA

            if start not in g.adj_list:
                return jsonify({'error': f'Start station "{start}" not found'}), 400
            if goal not in g.adj_list:
                return jsonify({'error': f'Goal station "{goal}" not found'}), 400

            path = g.bfs_shortest_path(start, goal)
            if path is None:
                return jsonify({'error': f'No path found from {start} to {goal}'}), 400

            return jsonify({'path': path})

        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500

    return render_template('mrt_map.html', stations=stations)

@app.route('/contact')
def contact():
    return render_template('contacts.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
