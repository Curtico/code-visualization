public class LinkedList<T> {
    
    // Node class representing each element in the LinkedList
    private static class Node<T> {
        T data;
        Node<T> next;

        public Node(T data) {
            this.data = data;
            this.next = null;
        }
    }
    
    private Node<T> head; // Head of the LinkedList
    private int size;     // Size of the LinkedList
    
    // Constructor to initialize an empty LinkedList
    public LinkedList() {
        head = null;
        size = 0;
    }
    
    // Method to add a new element to the end of the LinkedList
    public void add(T data) {
        Node<T> newNode = new Node<>(data);
        if (head == null) {
            head = newNode;
        } else {
            Node<T> current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        size++;
    }
    
    // Method to get the size of the LinkedList
    public int size() {
        return size;
    }
    
    // Method to check if the LinkedList is empty
    public boolean isEmpty() {
        return size == 0;
    }
    
    // Method to print the elements of the LinkedList
    public void printList() {
        Node<T> current = head;
        while (current != null) {
            System.out.print(current.data + " ");
            current = current.next;
        }
        System.out.println();
    }
}

