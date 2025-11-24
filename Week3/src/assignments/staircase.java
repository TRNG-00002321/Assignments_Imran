package assignments;

public class staircase {
    public static void main (String... args){


        int N = Integer.parseInt(args[0]);

        for(int i = 1; i <= N; i++){

            for(int n = 1; n <= i; n++){
                System.out.print("*");
            }

            System.out.println();
        }

        for(int i = N - 1; i >= 1; i--){

            for(int n = 1; n <= i; n++){
                System.out.print("*");
            }

            System.out.println();
        }
    }
}