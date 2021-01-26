public class Pear extends Fruit {

    public String name = "Pear";
    public boolean isForSale = true;
    public static String salesCat = "individual produce";

    public Pear() {
        super("Fruit");
    }

    public void setIsForSale(boolean status) {
        this.isForSale = status;
    }

    public boolean getIsForSale() {
        return isForSale;
    }

    public static String getSalesCat() {
        return salesCat;
    }

    public String getName() {
        return name;
    }

    public Grape fruitSalad(){
        return new Grape();
    }

    public String toString() {
        return "Pears are fruits.";
    }

}
