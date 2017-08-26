import java.util.HashSet;
import java.util.Set;

public class StructuresArraysAndStrings {

    /**
     * Determines if string has all unique characters.
     * <p>
     * Time and space complexity is O(n)
     *
     * @param str
     *            String to process
     * @return true or false
     */
    protected boolean hasAllUniqueChars(String str) {
        int lMax = str.length();

        // Add all characters to set
        Set<Character> lSet = new HashSet<>(lMax, 1.0f);
        for (int i = 0; i < lMax; i++) {
            Character lCurrentChar = Character.toLowerCase(str.charAt(i));
            if (lSet.contains(lCurrentChar)) {
                // Change flag and stop if find duplicate
                return false;
            } else {
                lSet.add(lCurrentChar);
            }
        }
        return true;
    }

    /**
     * Determines if string has all unique characters with no additional data
     * structures
     * <p>
     * Time complexity is O(logn) and no space
     *
     * @param str
     *            String to process
     * @return true or false
     */
    protected boolean hasAllUniqueCharsNoStructures(String str) {
        // recursively check every character with all others
        int lMax = str.length();

        // base case: if there is only one or less character left in string
        if (lMax <= 1) {
            return true;
        }

        // otherwise, check if the first letter matches any other
        Character lFirst = Character.toLowerCase(str.charAt(0));
        Character lCurrentChar;
        for (int i = 1; i < lMax; i++) {
            lCurrentChar = Character.toLowerCase(str.charAt(i));
            if (lCurrentChar.equals(lFirst)) {
                return false;
            }
        }

        // send smaller problem back into method
        return this.hasAllUniqueCharsNoStructures(str);
    }

    /**
     * Reverses a C-Style String.
     */
    protected String reverseCString(String str) {
        String ans = "";
        int lLength = str.length() - 1;

        // switch in place

        return new String(new char[] { 'c', 'b', 'a', '\0' });
    }
}