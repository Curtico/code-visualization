public class Test {
    public static void main(String[] args) {
        LinkedList<Integer> list = new LinkedList<>();

        list.add(1);
        list.add(2);
        list.add(3);

        System.out.println("Size of the list: " + list.size());
        System.out.println("Elements of the list:");
        list.printList();
    }
}
