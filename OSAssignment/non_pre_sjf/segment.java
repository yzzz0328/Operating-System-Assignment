public class segment {
    int order = 9;
    int time;

    boolean is_process = true;


    public segment(int order, int time)
    {
        this.order = order;
        this.time = time;
    }

    public segment(int time)
    {
        this.time = time;
        is_process = false;
    }

  
}
