import java.util.ArrayList;
import java.util.Scanner;

public class ApplicationGraphComponents {

    /*
     * Retrieve information from user input
     *
     * @param in Input stream
     *
     * @param verticesInGraph Number of adjacency lists
     *
     * @returns Graph representation in adjacency lists
     */
    private static ArrayList<ArrayList<Integer>> createLists(Scanner in,
            int verticesInGraph) {

        // Prepare adjacency list representation
        ArrayList<ArrayList<Integer>> allAdjLists = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i <= verticesInGraph; i++) {
            allAdjLists.add(i, null);
        }

        // Loop through input to build all adjacency lists
        for (int i = 0; i < verticesInGraph; i++) {
            System.out.print("Give adjacency list: ");
            // Retrieve line from input
            String input = in.nextLine();
            String[] tokens = input.split(" ");

            // Create new list per vertex
            ArrayList<Integer> vertexAdjList = new ArrayList<Integer>();
            vertexAdjList.add(i + 1);

            // Add each connected vertex to list
            int v = Integer.parseInt(tokens[0]);
            int d = Integer.parseInt(tokens[1]);
            for (int j = 0; j < d; j++) {
                vertexAdjList.add(Integer.parseInt(tokens[2 + j]));
            }
            allAdjLists.set(v, vertexAdjList);
        }
        return allAdjLists;
    }

    /**
     * Output number and contents of components
     *
     * @param verticesInGraph
     *            Number of vertices in graph
     * @param componentsTotal
     *            Number of components in graph
     * @param marked
     *            Set of explored vertices
     */
    public static void outputComponents(int verticesInGraph,
            int componentsTotal, int[] marked) {
        // Display number of components
        System.out.print("Components = " + componentsTotal + "\n");

        // Display contents of each component
        for (int i = 1; i <= componentsTotal; i++) {
            System.out.print("Component " + i + " Vertex List:");

            // Go through marked array and print out all connected
            for (int j = 1; j <= verticesInGraph; j++) {
                if (marked[j] == i) {
                    System.out.print(" " + j);
                }
            }
            System.out.println("\n");
        }
    }

    public static void main(String[] args) {
        // Retrieve total number of vertices in graph
        System.out.print("Give number of vertices: ");
        Scanner in = new Scanner(System.in);
        int verticesInGraph = Integer.parseInt(in.nextLine());
        ArrayList<ArrayList<Integer>> allAdjLists = createLists(in,
                verticesInGraph);
        in.close();

        int[] marked = new int[verticesInGraph + 1];
        int componentsTotal = 0;

        // Run DFS on graph
        for (int i = 1; i <= verticesInGraph; i++) {
            if (marked[i] == 0) {
                marked = SearchUninformed.dfs(allAdjLists, marked, i,
                        componentsTotal + 1);
                componentsTotal++;
            }
        }
        outputComponents(verticesInGraph, componentsTotal, marked);
    }
}