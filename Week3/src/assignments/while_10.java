package assignments;


public class while_10 {

    public static int multiples(String[] args) {
        int num1 = Integer.parseInt(args[0]);
        int i = 1;
        int result = 0;
        while (i <= 10) {
            result = num1 * i;
            System.out.println(result);
            i++;

        }

        return (result);
    }




    public static void main (String... args){
        int num = multiples(args);
    }
}
