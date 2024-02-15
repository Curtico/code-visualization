import java.util.LinkedList;

class LinkedListTest{
    public static void main(String args[]){  
        LinkedList<String> numbers = new LinkedList<String>();
        numbers.add("Zero");
        numbers.add("One");
        numbers.add("Two");
        numbers.add("Three");
        numbers.add("Four");

        int count = 0;
        int size = 5;
        for(count = 0; count < size; count++){
                System.out.println("" + numbers.get(count));
        }
        System.out.println(numbers);
    }
}

