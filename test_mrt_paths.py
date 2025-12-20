#!/usr/bin/env python3
"""
Test script for Manila MRT/LRT shortest path API.
Tests the bidirectional transfer between Doroteo Jose (LRT-1) and Recto (LRT-2).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms import graph as graph_module

def build_mrt_graph():
    """Build the MRT/LRT graph as in app.py"""
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

    return g

def test_paths():
    """Test critical paths for the transfer."""
    g = build_mrt_graph()

    test_cases = [
        # Doroteo Jose to LRT-2 stations
        ("Doroteo Jose", "Recto", ["Doroteo Jose", "Recto"]),  # Direct transfer
        ("Doroteo Jose", "Legarda", ["Doroteo Jose", "Recto", "Legarda"]),  # Via Recto
        ("Doroteo Jose", "Antipolo", ["Doroteo Jose", "Recto", "Legarda", "Pureza", "V. Mapa", "J. Ruiz", "Gilmore", "Betty Go-Belmonte", "Araneta Center-Cubao", "Anonas", "Katipunan", "Santolan", "Marikina-Pasig", "Antipolo"]),  # Full LRT-2

        # Recto to LRT-1 stations
        ("Recto", "Doroteo Jose", ["Recto", "Doroteo Jose"]),  # Direct transfer
        ("Recto", "Carriedo", ["Recto", "Doroteo Jose", "Carriedo"]),  # Via Doroteo Jose
        ("Recto", "Baclaran", ["Recto", "Doroteo Jose", "Carriedo", "Central Terminal", "United Nations", "Pedro Gil", "Quirino", "Vito Cruz", "Gil Puyat", "Libertad", "EDSA", "Baclaran"]),  # Full LRT-1 south

        # Other connections to ensure no breakage
        ("North Avenue", "Quezon Avenue", ["North Avenue", "Quezon Avenue"]),  # MRT-3
        ("Blumentritt", "Tayuman", ["Blumentritt", "Tayuman"]),  # LRT-1
        ("Legarda", "Pureza", ["Legarda", "Pureza"]),  # LRT-2
        ("Araneta Center-Cubao", "Santolan-Annapolis", ["Araneta Center-Cubao", "Santolan-Annapolis"]),  # MRT-3
    ]

    results = []
    for start, goal, expected in test_cases:
        path = g.bfs_shortest_path(start, goal)
        if path == expected:
            results.append(f"✓ PASS: {start} -> {goal}: {path}")
        else:
            results.append(f"✗ FAIL: {start} -> {goal}\n  Expected: {expected}\n  Got: {path}")

    return results

if __name__ == "__main__":
    print("Testing MRT/LRT Shortest Paths...")
    results = test_paths()
    for result in results:
        print(result)
    print("\nTest completed.")
