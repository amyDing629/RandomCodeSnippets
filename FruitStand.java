public class FruitStand {

    public static void main(String[] args) {

        Fruit f1 = new Fruit("New Fruit");
        Fruit f2 = new Grape();
        Fruit f3 = new Pear();
        Grape f4 = (Grape)f2;
        Fruit f5 = (Fruit)f2;
        Pear f6 = new Pear();

        //System.out.println(f2 == f4);
        //System.out.println(f1);
        //System.out.println(f2);
        //System.out.println(f3);
        //System.out.println(f4);
        //System.out.println(f5);
        //System.out.println(f6);

        //System.out.println(f1.name);
        //System.out.println(f2.name);
        //System.out.println(f3.name);
        //System.out.println(f4.name);
        //System.out.println(f5.name);
        //System.out.println(f6.name);

        //System.out.println(f1.getName());
        //System.out.println(f2.getName()); //why .getname is different with .name
        //System.out.println(f3.getName());
        //System.out.println(f4.getName());
        //System.out.println(f5.getName());
        //System.out.println(f6.getName());

        //System.out.println(f1.salesCat);
        //System.out.println(f2.salesCat);
        //System.out.println(f3.salesCat);
        //System.out.println(f4.salesCat);
        //System.out.println(f5.salesCat);
        //System.out.println(f6.salesCat);

        //System.out.println(f1.getSalesCat());
        //System.out.println(f2.getSalesCat());
        //System.out.println(f3.getSalesCat());
        //System.out.println(f4.getSalesCat());
        //System.out.println(f5.getSalesCat());
        //System.out.println(f6.getSalesCat());

        //System.out.println(f1.getIsForSale()); // Does this work? yes/no and why?
        //System.out.println(f2.getIsForSale()); // Does this work? yes/no and why?
        //System.out.println(f3.getIsForSale()); // Does this work? yes/no and why?
        //System.out.println(f4.getIsForSale());
        //System.out.println(f5.getIsForSale()); // Does this work? yes/no and why?
        //System.out.println(f6.getIsForSale());

         //System.out.println(f1.numFruit);
         //System.out.println(f2.numFruit);
         //System.out.println(f3.numFruit);
         //System.out.println(f4.numFruit);
         //System.out.println(f5.numFruit);
         //System.out.println(f6.numFruit);

         //f1.whatIsThis();
         //f2.whatIsThis();
         //f3.whatIsThis();
         //f4.whatIsThis();
         //f5.whatIsThis();
         //f6.whatIsThis();

         //System.out.println(((Grape) f2).fruitSalad().getName());
         //System.out.println((f2.getName()).equals(f3.getName()));
         //System.out.println(((Grape) f2).getIsForSale().equals(((Pear) f3).getIsForSale())); //Does this work? yes/no and why?

        int x = 2;
        int y = 2;
        Integer a = new Integer(2);
        Integer b = new Integer(2);
         System.out.println(x == y);
         System.out.println(a == b);
         System.out.println(a == x);
         System.out.println(a.equals(x));
         System.out.println(a.equals(b));
         //System.out.println(x.equals(y); // Does this work? yes/no and why?
    }
}
