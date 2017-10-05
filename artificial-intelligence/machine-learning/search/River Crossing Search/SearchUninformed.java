import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.TreeMap;

public class SearchUninformed {

    /**
     * Depth-first search
     * 
     * @param graph
     *            Representation of graph in adjacency lists
     * @param marked
     *            Set of explored vertices
     * @param v
     *            Vertex to start DFS
     * @param componentNum
     *            Number to track connected part of graph
     */
    public static int[] dfs(ArrayList<ArrayList<Integer>> graph, int[] marked,
            int v, int componentNum) {
        // Mark current vertex as visited
        marked[v] = componentNum;
        ArrayList<Integer> vList = graph.get(v);

        // Loop through every edge connected to vertex
        for (int i = 1; i < vList.size(); i++) {
            int child = vList.get(i);
            // If connected vertex is not visited
            if (marked[child] == 0) {
                // Run DFS on that vertex
                marked[child] = v;
                marked = dfs(graph, marked, child, componentNum);
            }
        }
        return marked;
    }

    /**
     * @param states
     *            All possible states.
     * @param transitionTable
     *            All transitions between states.
     * @param heuristic
     *            A defined method to alter procedure.
     */
    public static void bfs(SearchType type, ArrayList<int[]> states,
            TreeMap<Integer, ArrayList<Integer>> transitionTable,
            TreeMap<Integer, Integer> heuristic) {

        int root = 0;
        LinkedList<int[]> frontier = new LinkedList<int[]>();
        LinkedList<Integer> explored = new LinkedList<Integer>();
        TreeMap<Integer, Integer> previous = new TreeMap<Integer, Integer>();

        int[] element = { root, 4 };
        frontier.add(element);
        previous.put(root, -1);

        // Explore frontier until empty
        while (frontier.size() > 0) {
            int current = 0;

            // Consider cost
            if (type.equals(SearchType.ASTAR)) {
                // A*: cost = heuristic + path cost
                current = getSmallest(frontier)[0];
            } else if (type.equals(SearchType.BFS)) {
                // BFS: cost = path cost
                current = frontier.pop()[0];
            }

            explored.add(current);
            if (Arrays.equals(ApplicationRiverCrossing.goal,
                    states.get(current))) {
                printPath(current, previous, states, true);
                return;
            }
            ArrayList<Integer> children = transitionTable.get(current);
            for (int i = 0; i < children.size(); i++) {
                int child = children.get(i);
                if (frontier.indexOf(child) == -1
                        && explored.indexOf(child) == -1) {
                    previous.put(child, current);
                    element[0] = child;
                    if (type.equals(SearchType.ASTAR)) {
                        element[1] = cost(child, states, previous, heuristic);
                    } else {
                        element[1] = 0;
                    }
                    frontier.add(element);
                }
            }
        }
        return;
    }

    public static int[] getSmallest(LinkedList<int[]> frontier) {
        int[] current = frontier.pop();
        int[] temp = {};

        for (int i = 0; i < frontier.size(); i++) {
            int[] compare = frontier.pop();
            if (current[1] > compare[1]) {
                temp = current;
                current = compare;
                compare = temp;
            }
            frontier.add(compare);
        }

        return current;
    }

    public static int cost(int child, ArrayList<int[]> states,
            TreeMap<Integer, Integer> explored,
            TreeMap<Integer, Integer> heuristic) {
        int cost = 0;

        // get path cost
        cost += printPath(0, explored, states, false);

        // add h(n)
        cost += heuristic.get(child);

        return cost;
    }

    public static int printPath(int goal, TreeMap<Integer, Integer> previous,
            ArrayList<int[]> states, boolean print) {
        int current = goal;
        LinkedList<Integer> shortestPath = new LinkedList<Integer>();
        while (current != -1) {
            shortestPath.addFirst(current);
            current = previous.get(current);
        }
        for (int i = 0; i < shortestPath.size(); i++) {
            if (print) {
                System.out.print("\nstep " + i + ": ");
                outputNice(shortestPath.get(i), states);
            }
        }
        return shortestPath.size() - 1;
    }

    public static void outputNice(int stateIndex, ArrayList<int[]> states) {
        int[] state = states.get(stateIndex);
        for (int i = 0; i < 2; i++) {
            if (state[ApplicationRiverCrossing.farmer] == i) {
                System.out.print("f ");
            } else {
                System.out.print("_ ");
            }
            if (state[ApplicationRiverCrossing.wolf] == i) {
                System.out.print("w ");
            } else {
                System.out.print("_ ");
            }
            if (state[ApplicationRiverCrossing.sheep] == i) {
                System.out.print("s ");
            } else {
                System.out.print("_ ");
            }
            if (state[ApplicationRiverCrossing.cabbage] == i) {
                System.out.print("c ");
            } else {
                System.out.print("_ ");
            }
            if (i == 0) {
                System.out.print("| ");
            }
        }
    }
}
