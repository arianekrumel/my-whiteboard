import java.util.Iterator;

import components.binarytree.BinaryTree;
import components.binarytree.BinaryTree1;
import components.set.Set;
import components.set.SetSecondary;

/**
 * {@code Set} represented as a {@code BinaryTree} (maintained as a binary
 * search tree) of elements with implementations of primary methods.
 * 
 * @param <T>
 *            type of {@code Set} elements
 * @mathdefinitions <pre>
 * {@code IS_BST(
 *   tree: binary tree of T
 *  ): boolean satisfies
 *  [tree satisfies the binary search tree properties as described in the
 *   slides with the ordering reported by compareTo for T, including that
 *   it has no duplicate labels]}
 * </pre>
 * @convention <pre>
 * {@code IS_BST($this.tree)}
 * </pre>
 * @correspondence <pre>
 * {@code this = labels($this.tree)}
 * </pre>
 */
public class SetOnBST<T extends Comparable<T>> extends SetSecondary<T> {

    /*
     * Private members --------------------------------------------------------
     */

    /**
     * Elements included in {@code this}.
     */
    private BinaryTree<T> tree;

    /**
     * Returns whether {@code x} is in {@code t}.
     * 
     * @param <T>
     *            type of {@code BinaryTree} labels
     * @param t
     *            the {@code BinaryTree} to be searched
     * @param x
     *            the label to be searched for
     * @return true if t contains x, false otherwise
     * @requires <pre>
     * {@code IS_BST(t)}
     * </pre>
     * @ensures <pre>
     * {@code isInTree = (x is in labels(t))}
     * </pre>
     */
    private static <T extends Comparable<T>> boolean isInTree(BinaryTree<T> t,
            T x) {
        assert t != null : "Violation of: t is not null";
        assert x != null : "Violation of: x is not null";

        // create necessary variables
        boolean answer = false;
        BinaryTree<T> left = new BinaryTree1<>();
        BinaryTree<T> right = new BinaryTree1<>();

        // check how x compares to tree root
        if (t.size() > 0) {
            T root = t.disassemble(left, right);
            if (root.equals(x)) {
                answer = true;
            } else if (root.compareTo(x) > 0 && !answer) {
                // if not and less than, check left
                answer = isInTree(left, x);
            } else if (root.compareTo(x) < 0 && !answer) {
                // if not and more than, check right
                answer = isInTree(right, x);
            }

            // restore tree
            t.assemble(root, left, right);
        }

        return answer;
    }

    /**
     * Inserts {@code x} in {@code t}.
     * 
     * @param <T>
     *            type of {@code BinaryTree} labels
     * @param t
     *            the {@code BinaryTree} to be searched
     * @param x
     *            the label to be inserted
     * @aliases reference {@code x}
     * @updates {@code t}
     * @requires <pre>
     * {@code IS_BST(t)  and  x is not in labels(t)}
     * </pre>
     * @ensures <pre>
     * {@code IS_BST(t)  and  labels(t) = labels(#t) union {x}}
     * </pre>
     */
    private static <T extends Comparable<T>> void insertInTree(BinaryTree<T> t,
            T x) {
        assert t != null : "Violation of: t is not null";
        assert x != null : "Violation of: x is not null";

        BinaryTree<T> emptyLeft = new BinaryTree1<>();
        BinaryTree<T> emptyRight = new BinaryTree1<>();

        // if empty, put in as root        
        if (t.size() == 0) {
            t.assemble(x, emptyLeft, emptyRight);
        } else {
            BinaryTree<T> left = new BinaryTree1<>();
            BinaryTree<T> right = new BinaryTree1<>();

            T root = t.disassemble(left, right);

            // recursive check for left and right subtrees
            if (root.compareTo(x) > 0) {
                insertInTree(left, x);
            }
            if (root.compareTo(x) < 0) {
                insertInTree(right, x);
            }

            t.assemble(root, left, right);

        }

    }

    /**
     * Removes and returns the smallest (left-most) label in {@code t}.
     * 
     * @param <T>
     *            type of {@code BinaryTree} labels
     * @param t
     *            the {@code BinaryTree} from which to remove the label
     * @return the smallest label in the given {@code BinaryTree}
     * @updates {@code t}
     * @requires <pre>
     * {@code IS_BST(t)  and  |t| > 0}
     * </pre>
     * @ensures <pre>
     * {@code IS_BST(t)  and  removeSmallest = [the smallest label in #t]  and
     *  labels(t) = labels(#t) \ {removeSmallest}}
     * </pre>
     */
    private static <T> T removeSmallest(BinaryTree<T> t) {
        assert t != null : "Violation of: t is not null";

        //initialize variables
        BinaryTree<T> left = new BinaryTree1<T>();
        BinaryTree<T> right = new BinaryTree1<T>();
        T root = t.disassemble(left, right);
        T result = root;

        //check if left tree is not empty
        if (left.size() > 0) {
            result = removeSmallest(left);
            //if left is empty, root is smallest    
        } else {
            result = root;
            t.transferFrom(right);
        }

        if (!root.equals(result)) {
            t.assemble(root, left, right);
        }

        return result;
    }

    /**
     * Finds label {@code x} in {@code t}, removes it from {@code t}, and
     * returns it.
     * 
     * @param <T>
     *            type of {@code BinaryTree} labels
     * @param t
     *            the {@code BinaryTree} from which to remove label {@code x}
     * @param x
     *            the label to be removed
     * @return the removed label
     * @updates {@code t}
     * @requires <pre>
     * {@code IS_BST(t)  and  x is in labels(t)}
     * </pre>
     * @ensures <pre>
     * {@code IS_BST(t)  and  removeFromTree = x  and
     *  labels(t) = labels(#t) \ {x}}
     * </pre>
     */
    private static <T extends Comparable<T>> T removeFromTree(BinaryTree<T> t,
            T x) {
        assert t != null : "Violation of: t is not null";
        assert x != null : "Violation of: x is not null";

        // look for item, base case
        BinaryTree<T> left = new BinaryTree1<>();
        BinaryTree<T> right = new BinaryTree1<>();

        T answer;
        T root = t.disassemble(left, right);

        //compare root to x
        if (root.equals(x)) {
            //check both subtrees
            if (left.size() > 0 && right.size() > 0) {
                T smallest = removeSmallest(right);
                t.assemble(smallest, left, right);
                answer = root;
                //if no left tree t = right tree
            } else if (left.size() == 0 && right.size() > 0) {
                t.transferFrom(right);
                answer = root;
                //if no right tree t = left tree    
            } else {
                t.transferFrom(left);
                answer = root;
            }
            //determine which tree x is in (left or right)   
        } else if (root.compareTo(x) > 0) {
            //go into left tree
            answer = removeFromTree(left, x);
            t.assemble(root, left, right);
        } else {
            //go into right tree
            answer = removeFromTree(right, x);
            t.assemble(root, left, right);
        }

        return answer;
    }

    /**
     * Creator of initial representation.
     */
    private void createNewRep() {

        this.tree = new BinaryTree1<>();

    }

    /*
     * Constructors -----------------------------------------------------------
     */

    /**
     * Default constructor.
     */
    public Set3() {

        this.createNewRep();

    }

    /*
     * Standard methods -------------------------------------------------------
     */

    @SuppressWarnings("unchecked")
    @Override
    public final Set<T> newInstance() {
        try {
            return this.getClass().newInstance();
        } catch (ReflectiveOperationException e) {
            throw new AssertionError("Cannot construct object of type "
                    + this.getClass());
        }
    }

    @Override
    public final void clear() {
        this.createNewRep();
    }

    @Override
    public final void transferFrom(Set<T> source) {
        assert source != null : "Violation of: source is not null";
        assert source != this : "Violation of: source is not this";
        assert source instanceof Set3<?> : ""
                + "Violation of: source is of dynamic type Set3<?>";
        /*
         * This cast cannot fail since the assert above would have stopped
         * execution in that case: source must be of dynamic type Set3<?>, and
         * the ? must be T or the call would not have compiled.
         */
        Set3<T> localSource = (Set3<T>) source;
        this.tree = localSource.tree;
        localSource.createNewRep();
    }

    /*
     * Kernel methods ---------------------------------------------------------
     */

    @Override
    public final void add(T x) {
        assert x != null : "Violation of: x is not null";
        assert !this.contains(x) : "Violation of: x is not in this";

        insertInTree(this.tree, x);

    }

    @Override
    public final T remove(T x) {
        assert x != null : "Violation of: x is not null";
        assert this.contains(x) : "Violation of: x is in this";

        // remove and return element
        T removed = removeFromTree(this.tree, x);

        return removed;
    }

    @Override
    public final T removeAny() {
        assert this.size() > 0 : "Violation of: this /= empty_set";

        // remove and return any element
        T removed = removeSmallest(this.tree);

        return removed;
    }

    @Override
    public final boolean contains(T x) {
        assert x != null : "Violation of: x is not null";

        // evaluate if x is present
        boolean answer = isInTree(this.tree, x);

        return answer;
    }

    @Override
    public final int size() {

        // evaluate size of tree
        int answer = this.tree.size();

        return answer;
    }

    @Override
    public final Iterator<T> iterator() {
        return this.tree.iterator();
    }

}
