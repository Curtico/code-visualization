package codeviz.structures;

import java.util.HashMap;
import java.util.Map.Entry;

public class Map<K, V> {
    private HashMap<K, V> map;

    public Map() {
        map = new HashMap<>();
    }

    public void put(K key, V value) {
        map.put(key, value);
    }

    public V get(K key) {
        return map.get(key);
    }

    public boolean containsKey(K key) {
        return map.containsKey(key);
    }

    public void display() {
        for (Entry<K, V> entry : map.entrySet()) {
            System.out.println("Key: " + entry.getKey() + ", Value: " + entry.getValue());
        }
    }

    public int size() {
        return map.size();
    }
}
