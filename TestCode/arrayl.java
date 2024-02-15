import java.util.ArrayList; 

class ArrayListTest{
    public static void main(String args[]){  
          ArrayList<String> colors = new ArrayList<String>();
          colors.add("red");
          colors.add("yellow");
          colors.add("blue");
          colors.add("green");
          colors.add("pink");
                
          int count = 0;
          int size = 5;
          for(count = 0; count < size; count++){
                System.out.println("" + colors.get(count));
          }
    }
}
