import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class StructuresArraysAndStringsUnitTest {
    /*
     * Test object
     */
    private StructuresArraysAndStrings myTestObject;

    @Before
    public void setUp() {
        this.myTestObject = new StructuresArraysAndStrings();
    }

    /**
     * Tests hasAllUniqueChars()
     */
    @Test
    public void testHasAllUniqueChars() {
        // Simple fail case
        Assert.assertFalse(this.myTestObject.hasAllUniqueChars("test"));

        // Simple pass case
        Assert.assertTrue(this.myTestObject.hasAllUniqueChars("bar"));

        // Edge case, zero
        Assert.assertTrue(this.myTestObject.hasAllUniqueChars(""));

        // Edge case, one
        Assert.assertTrue(this.myTestObject.hasAllUniqueCharsNoStructures("K"));

        // Harder, mix of white space
        Assert.assertFalse(this.myTestObject
                .hasAllUniqueChars("Our mental synchronization can have but one explanation"));

        // Harder, mix of cases
        Assert.assertFalse(this.myTestObject.hasAllUniqueChars("FoO Bar"));
    }

    /**
     * Tests hasAllUniqueCharsNoStructures()
     */
    @Test
    public void testHasAllUniqueCharsNoStructures() {
        // Simple fail case
        Assert.assertFalse(this.myTestObject.hasAllUniqueChars("test"));

        // Simple pass case
        Assert.assertTrue(this.myTestObject.hasAllUniqueChars("bar"));

        // Edge case, zero
        Assert.assertTrue(this.myTestObject.hasAllUniqueCharsNoStructures(""));

        // Harder, mix of white space
        Assert.assertFalse(this.myTestObject
                .hasAllUniqueChars("Our mental synchronization can have but one explanation"));

        // Harder, mix of cases
        Assert.assertFalse(this.myTestObject.hasAllUniqueChars("FoO Bar"));
    }

    /**
     * Tests reverseCString()
     */
    @Test
    public void testReverseCString() {
        String lStr = new String(new char[] { 'a', 'b', 'c', '\0' });
        String lActual = this.myTestObject.reverseCString(lStr);
        String lExpected = new String(new char[] { 'c', 'b', 'a', '\0' });

        Assert.assertEquals(lActual, lExpected);

    }
}
