import codeviz.structures.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> list = new List<>();

        list.add(2);
        list.add(4);
        list.add(6);
        list.add(8);
        list.add(10);

        System.out.println("List size: " + list.size());

        System.out.println("Elements in the list:");
        for (int i = 0; i < list.size(); i++) {
            System.out.println(list.get(i));
        }
    }
}
