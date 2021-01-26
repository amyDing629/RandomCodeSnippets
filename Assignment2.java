// CSC343, Introduction to Databases
// Department of Computer Science, University of Toronto

// This code is provided solely for the personal and private use of
// students taking the course CSC343 at the University of Toronto.
// Copying for purposes other than this use is expressly prohibited.
// All forms of distribution of this code, whether as given or with
// any changes, are expressly prohibited.

// Authors: Diane Horton and Marina Tawfik

// Copyright (c) 2020 Diane Horton and Marina Tawfik


import java.sql.*;
import java.util.ArrayList;

public class Assignment2 {
  
  // A connection to the database
  Connection connection;

  Assignment2() throws SQLException {
    try {
      Class.forName("org.postgresql.Driver");
    } catch  (ClassNotFoundException e) {
      e.printStackTrace();
    }
  }

  public boolean connectDB(String url, String username, String password) {
    // Replace the line below and implement this method!
    try{ connection = DriverManager.getConnection(url, username, password);
      PreparedStatement ps = connection.prepareStatement("set search_path to library, public");
      ps.execute();
      if (!connection.isClosed()){return true;}
      return false;}
    catch(SQLException se){
      return false;}
  }

  /**
   * Closes the database connection.
   *
   * @return true if the closing was successful, false otherwise
   */
  public boolean disconnectDB() {
    // Replace the line below and implement this method!
    try{connection.close();
      if (connection.isClosed()){return true;}
      return false;}
    catch(SQLException se){
      return false;}
  }

  /**
   * Returns the titles of all holdings at the given library branch
   * by any contributor with the given last name.
   * If no matches are found, returns an empty list.
   * If two different holdings happen to have the same title, returns both
   * titles.
   *
   * @param  lastName  the last name to search for.
   * @param  branch    the unique code of the branch to search within.
   * @return           a list containing the titles of the matched items.
   */
  public ArrayList<String> search(String lastName, String branch) {
    // Replace the line below and implement this method!
    try {
      String queryString = "select title from "+
              "libraryCatalogue c1, holding c2, contributor c3, "+
              "holdingcontributor c4 where c1.holding = c4.holding "+
              "and c1.holding=c2.id and library = ? "+
              "and contributor = c3.id and last_name = ? group by c2.id";
      PreparedStatement pStatement =
              connection.prepareStatement(queryString);
      pStatement.setString(1,branch);
      pStatement.setString(2, lastName);
      ResultSet rs = pStatement.executeQuery();
      ArrayList<String> answer = new ArrayList<String> ();
      while (rs.next()){

        answer.add(rs.getString("title"));}
      return answer;}
    catch(SQLException se){
      return null;
    }}



  /**
   * Records a patron's registration for a specific event.
   * Returns True iff
   *  (1) the card number and event ID provided are both valid 
   *  (2) This patron is not already registered for this event
   * Otherwise, returns False.
   *
   * @param  cardNumber  card number of the patron.
   * @param  eventID     id of the event.
   * @return             true if the operation was successful 
   *                     (as per the above criteria), and false otherwise.
   */
  public boolean register(String cardNumber, int eventID) {
    try {
      String queryString1 = "select count(*) as num from (\n" +
              "select p.card_number as patron, l.id as event\n" +
              "from patron p, libraryevent l\n" +
              "where (p.card_number, l.id) not in (select patron, event from eventsignup)) a\n" +
              "where patron = ?  and event = cast(? as Integer);";
      PreparedStatement pStatement1 =
              connection.prepareStatement(queryString1);
      pStatement1.setString(1 , cardNumber);
      pStatement1.setString(2, String.valueOf(eventID));
      ResultSet rs = pStatement1.executeQuery();
      while (rs.next()){
        if (rs.getInt("num") == 0){
          return false;
        }else{
          String sql = "insert into eventsignup values('" + cardNumber + "', " + eventID + ")";
          PreparedStatement pStatement2 =
                  connection.prepareStatement(sql);
          pStatement2.executeUpdate();
          return true;
        }}
    } catch (SQLException throwables) {
      throwables.printStackTrace();
    }
    return false;
  }


  /**
   * Records that a checked out library item was returned and returns 
   * the fines incurred on that item.
   *
   * Does so by inserting a row in the Return table and updating the
   * LibraryCatalogue table to indicate the revised number of copies 
   * available.
   * 
   * Uses the same due date rules as the SQL queries.
   * The fines incurred are calculated as follows: for every day overdue 
   * i.e. past the due date:
   *    books and audiobooks incurr a $0.50 charge
   *    other holding types incurr a $1.00 charge
   * 
   * A return operation is considered successful iff:
   *    (1) The checkout id provided is valid. 
   *    (2) A return has not already been recorded for this checkout
   *    (3) The number of available copies is less than the number of holdings
   * If the return operation is unsuccessful, the db instance should not 
   * be modified at all.
   * 
   * @param  checkout  id of the checkout
   * @return           the amount of fines incurred if the return operation
   *                   was successful, -1 otherwise.
   */
  public double item_return(int checkout) {
    try {
      String queryString1 = "select count(*) as num from checkout \n" +
              "where id not in (select checkout from return) and \n" +
              "holding in (select holding from librarycatalogue \n" +
              "where num_holdings > copies_available) and id = cast(? as Integer);";
      PreparedStatement pStatement1 =
              connection.prepareStatement(queryString1);
      pStatement1.setString(1, String.valueOf(checkout));
      ResultSet rs = pStatement1.executeQuery();
      while (rs.next()){
        if (rs.getInt("num") == 0){
          return -1;
        }else{
          String sql = "insert into return values(" + checkout + ", now());";
          PreparedStatement pStatement2 =
                  connection.prepareStatement(sql);
          pStatement2.executeUpdate();
          String sql2 = "update librarycatalogue set copies_available = copies_available + 1 \n" +
                  "from checkout where checkout.id = cast(? as Integer) and checkout.holding = librarycatalogue.holding;";
          PreparedStatement pStatement3 = connection.prepareStatement(sql2);
          pStatement3.setString(1, String.valueOf(checkout));
          pStatement3.executeUpdate();
          String sql3 = "select checkout.id, htype, date(return_time) - date(checkout_time) as own_time\n" +
                  "from checkout, holding, return\n" +
                  "where checkout.id = return.checkout and " +
                  "checkout.holding = holding.id and checkout.id = cast(? as Integer);";
          PreparedStatement pStatement4 = connection.prepareStatement(sql3);
          pStatement4.setString(1, String.valueOf(checkout));
          ResultSet rs2 = pStatement4.executeQuery();
          while (rs2.next()){
            String type = rs2.getString("htype");
            int own_time = rs2.getInt("own_time");
            if (type.equals("books") || (type.equals("audiobooks"))){
              return 0.5 * (own_time - 21);
            }else {
              return own_time - 7;
            }
          }
        }}
    } catch (SQLException throwables) {
      throwables.printStackTrace();
    }
    return 0.0;
  }

  public static void main(String[] args) {

    Assignment2 a2;
    try {
      // Demo of using an ArrayList.
      ArrayList<String> baking = new ArrayList<String>();
      baking.add("croissant");
      baking.add("choux pastry");
      baking.add("jelly roll");

      // Make an instance of the Assignment2 class.  It has an instance 
      // variable that will hold on to our database connection as long
      // as the instance exists -- even between method calls.
      a2 = new Assignment2();

      // Use your connect method to connect to your database.  You need
      // to pass in the url, username, and password, rather than have them
      // hard-coded in the method.  (This is different from the JDBC code
      // we worked on in a class exercise.) Replace the XXXXs with your
      // username, of course.
      a2.connectDB("jdbc:postgresql://localhost:5432/csc343h-dingyiy1", "dingyiy1", "Yesorno12345Ding");

      // You can call your methods here to test them. It will not affect our 
      // autotester.
      System.out.println(a2.item_return(1));
    }
    catch (Exception ex) {      
      System.out.println("exception was thrown");
      ex.printStackTrace();
    }
  }

}

