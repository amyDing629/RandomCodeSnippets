public class Grape extends Fruit {

    public String name = "Grape";
    public boolean isForSale = true;
    public static String salesCat = "individual produce";

    public Grape() {
        super("Fruit");
    }

    public static String getSalesCat() {
        return salesCat;
    }

    public boolean getIsForSale() {
        return isForSale;
    }

    public void setIsForSale(boolean status) {
        isForSale = status;
    }

    public String getName() {
        return name;
    }

    public Pear fruitSalad(){
        return new Pear();
    }

    public String toString() {
        return "Grapes are fruits.";
    }
}
