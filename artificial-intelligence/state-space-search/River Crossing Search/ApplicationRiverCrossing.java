import java.util.ArrayList;
import java.util.Arrays;
import java.util.TreeMap;

public class ApplicationRiverCrossing {

    /**
     * Create notation of farmer, wolf, sheep and cabbage
     */
    public static int farmer = 0;
    public static int wolf = 1;
    public static int sheep = 2;
    public static int cabbage = 3;

    /**
     * Goal state
     */
    public static int[] goal = new int[] { 1, 1, 1, 1 };

    /**
     * Generate all possible states.
     *
     * @param withConditions
     *            Set to true to exclude invalid states.
     * @return List of all possible states.
     */
    public static ArrayList<int[]> generateStates(boolean withConditions) {
        ArrayList<int[]> states = new ArrayList<int[]>();

        // Loop through all possible combinations
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                for (int k = 0; k < 2; k++) {
                    for (int l = 0; l < 2; l++) {
                        int[] thisState = new int[] { i, j, k, l };
                        /*
                         * wolf&sheep and sheep&cabbage combinations cannot be
                         * on opposite side as farmer
                         */
                        if (withConditions) {
                            boolean sheepEaten = false;
                            boolean cabbageEaten = false;
                            if (thisState[farmer] == 0) {
                                sheepEaten = (thisState[sheep] == 1)
                                        && (thisState[wolf] == 1);
                                cabbageEaten = (thisState[sheep] == 1)
                                        && (thisState[cabbage] == 1);
                            }
                            if (thisState[farmer] == 1) {
                                sheepEaten = (thisState[sheep] == 0)
                                        && (thisState[wolf] == 0);
                                cabbageEaten = (thisState[sheep] == 0)
                                        && (thisState[cabbage] == 0);
                            }
                            if (!sheepEaten && !cabbageEaten) {
                                states.add(thisState);
                            }
                        } else {
                            states.add(thisState);
                        }
                    }
                }
            }
        }
        return states;
    }

    public static void displayStates(ArrayList<int[]> allowedStates) {
        // Display all valid states
        for (int i = 0; i < allowedStates.size(); i++) {
            System.out.print("State " + (i) + ": \t");
            for (int j = 0; j < 4; j++) {
                System.out.print(allowedStates.get(i)[j]);
            }
            System.out.print('\n');
        }
    }

    public static TreeMap<Integer, ArrayList<Integer>> findTransitions(
            ArrayList<int[]> allowedStates) {
        TreeMap<Integer, ArrayList<Integer>> transitionTable = new TreeMap<Integer, ArrayList<Integer>>();

        // Find transitions for all states
        for (int i = 0; i < allowedStates.size(); i++) {
            for (int j = 0; j < allowedStates.size(); j++) {
                int diffs = 0;
                int invalidChanges = 0;
                // Farmer changes sides in every state change
                if (allowedStates.get(i)[farmer] == 0
                        && allowedStates.get(j)[farmer] == 1) {
                    for (int k = 1; k < 4; k++) {
                        if (allowedStates.get(i)[k] != allowedStates.get(j)[k]) {
                            diffs++;
                        }
                        if (allowedStates.get(i)[k] == 1
                                && allowedStates.get(j)[k] == 0) {
                            invalidChanges++;
                        }
                    }
                }
                if (allowedStates.get(i)[farmer] == 1
                        && allowedStates.get(j)[farmer] == 0) {
                    for (int k = 1; k < 4; k++) {
                        if (allowedStates.get(i)[k] != allowedStates.get(j)[k]) {
                            diffs++;
                        }
                        if (allowedStates.get(i)[k] == 0
                                && allowedStates.get(j)[k] == 1) {
                            invalidChanges++;
                        }
                    }
                }
                if (allowedStates.get(i)[farmer] != allowedStates.get(j)[farmer]) {
                    if (diffs <= 1 && invalidChanges == 0) {
                        ArrayList<Integer> transitions = new ArrayList<Integer>();
                        if (transitionTable.containsKey(i)) {
                            transitions = transitionTable.get(i);
                            transitionTable.remove(i);
                        }
                        transitions.add(j);
                        transitionTable.put(i, transitions);
                    }
                }
            }
            // Remove all transitions starting at goal node to exclude from search
            if (Arrays.equals(allowedStates.get(i), goal)) {
                transitionTable.remove(i);
            }
        }
        return transitionTable;
    }

    public static TreeMap<Integer, Integer> createHeuristic(
            ArrayList<int[]> states) {
        TreeMap<Integer, Integer> heuristic = new TreeMap<Integer, Integer>();
        int sum = 0;
        // Loop through every state
        for (int i = 0; i < states.size(); i++) {
            for (int j = 0; j < states.get(i).length; j++) {
                sum += states.get(i)[j];
            }
            heuristic.put(i, 4 - sum);
            sum = 0;
        }
        return heuristic;
    }

    public static void main(String[] args) {

        // Generate all allowed states considering conditions
        ArrayList<int[]> statesWithConditions = generateStates(true);
        System.out.println("Allowed states (" + statesWithConditions.size()
                + ")");
        displayStates(statesWithConditions);

        // Find all transitions
        TreeMap<Integer, ArrayList<Integer>> transitionTable = findTransitions(statesWithConditions);
        System.out.println("\nTransition Table\n" + transitionTable.toString()
                + "\n");

        // Create heuristic
        System.out.print("Heuristic Function\n");
        TreeMap<Integer, Integer> heuristic = createHeuristic(statesWithConditions);
        System.out.println("h(n) = " + heuristic + "\n");

        /* Breadth First Search */
        System.out.print("Breadth-first Search");
        SearchUninformed.bfs(SearchType.BFS, statesWithConditions,
                transitionTable, heuristic);

        /* A* Search */
        System.out.print("\n\nA* Search");
        SearchUninformed.bfs(SearchType.ASTAR, statesWithConditions,
                transitionTable, heuristic);

    }
}