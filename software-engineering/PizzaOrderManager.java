import components.map.Map;
import components.map.Map1L;
import components.simplereader.SimpleReader;
import components.simplereader.SimpleReader1L;
import components.simplewriter.SimpleWriter;
import components.simplewriter.SimpleWriter1L;

/**
 * Simple pizza order manager: inputs orders from a file and computes and
 * displays the total price for each order.
 * 
 */
public final class PizzaOrderManager {

    /**
     * Private constructor so this utility class cannot be instantiated.
     */
    private PizzaOrderManager() {
    }

    /**
     * Inputs a "menu" of words (items) and their prices from the given file and
     * stores them in the given {@code Map}.
     * 
     * @param fileName
     *            the name of the input file
     * @param priceMap
     *            the word -> price map
     * @replaces {@code priceMap}
     * @requires <pre>
     * {@code [file named fileName exists but is not open, and has the
     *  format of one "word" (unique in the file) and one price (in cents)
     *  per line, with word and price separated by ','; the "word" may
     *  contain whitespace but not ',']}
     * </pre>
     * @ensures <pre>
     * {@code [priceMap contains word -> price mapping from file fileName]}
     * </pre>
     */
    private static void getPriceMap(String fileName,
            Map<String, Integer> priceMap) {
        assert fileName != null : "Violation of: fileName is not null";
        assert priceMap != null : "Violation of: priceMap is not null";
        /*
         * Note: Precondition not checked!
         */

        SimpleReader input = new SimpleReader1L(fileName);
        while (!input.atEOS()) {
            String thisLine = input.nextLine();
            String thisKey = thisLine.substring(0, thisLine.indexOf(','));
            String thisValue = thisLine.substring(thisLine.indexOf(',') + 1,
                    thisLine.length());
            int value = Integer.parseInt(thisValue);
            priceMap.add(thisKey, value);
        }
        input.close();

    }

    /**
     * Input one pizza order and compute and return the total price.
     * 
     * @param input
     *            the input stream
     * @param sizePriceMap
     *            the size -> price map
     * @param toppingPriceMap
     *            the topping -> price map
     * @return the total price (in cents)
     * @updates {@code input}
     * @requires <pre>
     * {@code input.is_open and 
     * [input.content begins with a pizza order consisting of a size
     *  (something defined in sizePriceMap) on the first line, followed
     *  by zero or more toppings (something defined in toppingPriceMap)
     *  each on a separate line, followed by an empty line]}
     * </pre>
     * @ensures <pre>
     * {@code input.is_open and
     * #input.content = [one pizza order (as described
     *              in the requires clause)] * input.content and
     * getOneOrder = [total price (in cents) of that pizza order]}
     * </pre>
     */
    private static int getOneOrder(SimpleReader input,
            Map<String, Integer> sizePriceMap,
            Map<String, Integer> toppingPriceMap) {
        assert input != null : "Violation of: input is not null";
        assert sizePriceMap != null : "Violation of: sizePriceMap is not null";
        assert toppingPriceMap != null : "Violation of: toppingPriceMap is not null";
        assert input.isOpen() : "Violation of: input.is_open";
        int price = 0;
        int size = sizePriceMap.value(input.nextLine());
        price = price + size;
        String toppingSTR = input.nextLine();
        int topping = 0;
        while (!toppingSTR.isEmpty()) {
            topping = toppingPriceMap.value(toppingSTR);
            price += topping;
            toppingSTR = input.nextLine();
        }
        return price;
    }

    /**
     * Output the given price formatted in dollars and cents.
     * 
     * @param output
     *            the output stream
     * @param price
     *            the price to output
     * @updates {@code output}
     * @requires <pre>
     * {@code output.is_open = true and 0 <= price}
     * </pre>
     * @ensures <pre>
     * {@code output.is_open and
     * output.content = #output.content *
     *  [display of price, where price is in cents but
     *   display is formatted in dollars and cents]}
     * </pre>
     */
    private static void putPrice(SimpleWriter output, int price) {
        assert output != null : "Violation of: output is not null";
        assert output.isOpen() : "Violation of: output.is_open";
        assert 0 <= price : "Violation of: 0 <= price";

        int cents = price % 100;
        price /= 100;
        if (cents < 10) {
            output.println("$" + price + ".0" + cents);
        } else {
            output.println("$" + price + "." + cents);
        }
    }

    /**
     * Main method.
     * 
     * @param args
     *            the command line arguments
     */
    public static void main(String[] args) {
        SimpleReader in = new SimpleReader1L("data/orders.txt");
        SimpleWriter out = new SimpleWriter1L();
        Map<String, Integer> sizeMenu = new Map1L<String, Integer>();
        Map<String, Integer> toppingMenu = new Map1L<String, Integer>();
        int orderNumber = 1;
        /*
         * Get menus of sizes with prices and toppings with prices
         */
        getPriceMap("data/sizes.txt", sizeMenu);
        getPriceMap("data/toppings.txt", toppingMenu);
        /*
         * Output heading for report of pizza orders
         */
        out.println();
        out.println("Order");
        out.println("Number Price");
        out.println("------ ------");
        /*
         * Process orders, one at a time, from input file
         */
        while (!in.atEOS()) {
            int price = getOneOrder(in, sizeMenu, toppingMenu);
            out.print(orderNumber + "      ");
            putPrice(out, price);
            out.println();
            orderNumber++;
        }
        out.println();
        /*
         * Close input and output streams
         */
        in.close();
        out.close();
    }

}
