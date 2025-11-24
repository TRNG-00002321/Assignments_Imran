package assignments;

class factorial {
    public static int fctrl(int n){
        int ans = 1;
        for(int i = 2; i <= n; i++) {
            ans = ans * i;
        }
    return(ans);
    }

     static void main (String[] args){
        int num = 5;
        System.out.println(fctrl(num));
}
}
