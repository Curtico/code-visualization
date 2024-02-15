import codeviz.structures.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> map = new Map<>();

        map.put("red", 10);
        map.put("yellow", 20);
        map.put("blue", 30);

        System.out.println("Map size: " + map.size());
        System.out.println("Value for key 'red': " + map.get("red"));
        System.out.println("Value for key 'yellow': " + map.get("yellow"));

        System.out.println("Displaying map contents:");
        map.display();
    }
}
