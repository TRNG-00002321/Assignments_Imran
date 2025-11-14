package assignments;

public class if_else3num {



    // New method that contains all the program's primary logic
    public static int runProgram(String[] args) {
        // All argument parsing and function calls are here, NOT in main.
        int num1 = Integer.parseInt(args[0]);
        int num2 = Integer.parseInt(args[1]);
        int num3 = Integer.parseInt(args[2]);
        int max_int = 9;

        if(num1 > num2 && num1 > num3){
            max_int = num1;
        }
        else if(num2 > num3) {
            max_int = num2;
            }
        else{
            max_int = num3;
            }
        return(max_int);
    }



    public static void main (String[] args) {

        int max_int = runProgram(args);

        if (args.length >= 3) {
            System.out.println("The greatest number is: " + max_int);
        }
    }

}
