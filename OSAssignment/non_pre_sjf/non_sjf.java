import java.util.ArrayList;
import java.util.LinkedList;

public class non_sjf {

    ArrayList<process> processes = new ArrayList<>();
    LinkedList<process> queue = new LinkedList<>();
    LinkedList<segment> gantt_chart = new LinkedList<>();

    ArrayList<ArrayList<String>> arr_time_stamp = new ArrayList<>();

    int total_burst_time;

    process current;

    String output = "";

    public non_sjf(ArrayList<process> processes) {


        this.processes = processes;
        
        total_burst_time = get_total_burst_time();

        sort_process_queue();

        for (int clock = 0; clock < total_burst_time;) {

            add_process_to_queue(clock);

            sort_by_burst(queue);

            if (queue.size() == 0) {
                clock++;
                continue;
            }

            // get process to run
            try {
                current = queue.getFirst();

                gantt_chart.add(new segment(current.order, clock));

                clock += current.burst;

                current.finish = clock;

                queue.removeFirst();

            } catch (Exception e) {
                continue;
            }
        }

        cal_all_turnaround();
        cal_all_waiting();
        sort_by_order();

        add_arrival_segment();
        add_arrival_timestamp();

        print_table();

        output = output.concat("\n");
        
        print_gantt_chart();

    }

    public void add_process_to_queue(int clock) {

        for (process i : processes) {

            if (i.arrival <= clock && !i.in_queue) {
                queue.add(i);
                i.in_queue = true;
            }
        }
    }

    public void sort_process_queue() {

        LinkedList<process> temp_list = new LinkedList<>();
        LinkedList<process> output = new LinkedList<>();

        for (int i = 0; i < total_burst_time; i++) {

            // get all processes with the same arrival time
            for (process j : processes) {
                if (j.arrival == i) {
                    temp_list.add(j);
                }
            }

            sort_by_burst(temp_list);

            // add the processes to output linked_list
            for (process p : temp_list) {
                output.add(p);
            }

            temp_list.clear();
        }

        // update processes linked_list
        processes.clear();
        for (process p : output) {
            processes.add(p);
        }
    }

    public void sort_by_order() {
        boolean can_break = false;
        process temp;

        while (!can_break) {

            can_break = true;

            for (int j = 0; j < processes.size() - 1; j++) {
                if (processes.get(j).order > processes.get(j + 1).order) {
                    temp = processes.get(j);
                    processes.remove(j);
                    processes.add(temp);
                    j = 0;
                    can_break = false;
                }
            }
        }
    }

    public void sort_by_burst(LinkedList<process> the_list) {
        boolean can_break = false;
        process temp;

        while (!can_break) {

            can_break = true;

            for (int j = 0; j < the_list.size() - 1; j++) {
                if (the_list.get(j).burst > the_list.get(j + 1).burst) {
                    temp = the_list.get(j);
                    the_list.remove(j);
                    the_list.add(temp);
                    j = 0;
                    can_break = false;
                }
            }
        }
    }

    public int get_total_burst_time() {
        int output = 0;

        for (process i : processes)
            output += i.burst;

        return output;
    }

    public void cal_all_turnaround() {
        for (process p : processes) {
            p.calturnaround();
        }
    }

    public void cal_all_waiting() {
        for (process p : processes) {
            p.calwaiting();
        }
    }

    public void print_table() {

        output = output.concat("Non-preemptive SJF\n");

        print_line(72);
        output = output.concat("|  |Arrival Time|Burst Time|Finishing Time|Turnaround time|Waiting time|\n");
        print_line(72);

        for (process p : processes) {

            output = output
                    .concat(String.format("|%2s|%12d|%10d|%14d|%15d|%12d|\n", "P" + p.order, p.arrival, p.og_burst,
                            p.finish, p.turnaround, p.waiting));
            print_line(72);
        }
        print_line(72);

        int total_turnaround = 0;
        int total_waiting = 0;

        for (process p : processes) {
            total_turnaround += p.turnaround;
            total_waiting += p.waiting;
        }

        double avg_turnaround = (double) total_turnaround / processes.size();
        double avg_waiting = (double) total_waiting / processes.size();

        output = output.concat(String.format("|Total  |%49d|%12d|\n", total_turnaround, total_waiting));
        print_line(72);

        output = output.concat(String.format("|Average|%49.3f|%12.3f|\n", avg_turnaround, avg_waiting));
        print_line(72);
    }

    public void print_gantt_chart() {

        output = output.concat("Gantt Chart\n");

        print_line(gantt_chart.size() * 6 + 2);

        output = output.concat("  ");
        for (segment s : gantt_chart) {
            if (s.is_process)
                output = output.concat(" P" + s.order + "  |");
            else
                output = output.concat("     |");
        }
        output = output.concat("\n");

        print_line(gantt_chart.size() * 6 + 2);

        for (segment s : gantt_chart) {
            output = output.concat(String.format("%2d    ", s.time));
        }
        output = output.concat(total_burst_time + "\n");


        // arrival time
        for (int i = 0; i < arr_time_stamp.get(0).size(); i++) {
            for (int j = 0; j < arr_time_stamp.size(); j++) {
                if (arr_time_stamp.get(j).get(i) == null)
                    output = output.concat("      ");
                else
                    output = output.concat(arr_time_stamp.get(j).get(i));
            }

            output = output.concat("\n");
        }
    }

    void print_line(int x) {
        for (int i = 0; i < x; i++) {
            output = output.concat("_");
        }
        output = output.concat("\n");
    }

    public void add_arrival_segment() {

        for (int i = 0; i < processes.size(); i++) {
            for (int j = 0; j < gantt_chart.size() - 1; j++) {
                if (processes.get(i).arrival == gantt_chart.get(j).time) {
                    break;
                } else if (processes.get(i).arrival > gantt_chart.get(j).time
                        && processes.get(i).arrival < gantt_chart.get(j + 1).time) {
                    gantt_chart.add(j + 1, new segment(processes.get(i).arrival));
                    break;
                }
            }
        }
    }

    public void add_arrival_timestamp() {
        ArrayList<String> temp;
        int max = 0;

        for (int i = 0; i < gantt_chart.size(); i++) {

            temp = new ArrayList<>();

            for (int j = 0; j < processes.size(); j++) {
                if (gantt_chart.get(i).time == processes.get(j).arrival) {
                    temp.add("P" + processes.get(j).order + String.format("(%-2d)", processes.get(j).og_burst));
                }

                if (temp.size() > max) {
                    max = temp.size();
                }
            }
            arr_time_stamp.add(temp);
        }

        // add null to empty spaces
        for (int i = 0; i < arr_time_stamp.size(); i++) {
            for (int j = 0; j < max; j++) {
                try {
                    String txt = arr_time_stamp.get(i).get(j);
                } catch (Exception e) {
                    arr_time_stamp.get(i).add(null);
                }
            }
        }
    }

}