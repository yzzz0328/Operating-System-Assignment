public class process
{
    int arrival;
    int og_burst;
    int burst;

    int finish;
    int turnaround;
    int waiting;

    int order;

    boolean in_queue = false;

    public process(int order, int arrival, int burst)
    {
        this.order = order;
        this.arrival = arrival;
        this.burst = burst;
        og_burst = burst;

    }

    public void calturnaround()
    {
        this.turnaround = this.finish - this. arrival;
    }

    public void calwaiting()
    {
        this.waiting = this.turnaround - this.og_burst;
    }
}