import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.util.ArrayList;

public class non_sjf_interface extends JFrame implements ActionListener {

    JPanel[] rows = new JPanel[10];

    JTextField[] arrival_text = new JTextField[10];
    JTextField[] burst_text = new JTextField[10];
    JLabel[] order_label = new JLabel[10];

    JButton calc_but = new JButton("Calculate");
    JButton clear_but = new JButton("Clear");
    JButton big_but = new JButton("+");
    JButton small_but = new JButton("-");

    JTextArea display = new JTextArea();

    public non_sjf_interface() {

        JPanel container = new JPanel();
        container.setPreferredSize(new Dimension(300, 750));
        container.setBackground(new Color(177, 156, 217));

        JLabel arrival_label = new JLabel("        Arrival time     Burst time");
        arrival_label.setPreferredSize(new Dimension(300, 30));
        arrival_label.setFont(new Font("Arial", Font.PLAIN, 15));
        arrival_label.setOpaque(true);
        arrival_label.setBackground(Color.WHITE);

        container.add(arrival_label);

        for (int i = 1; i < 10; i++) {
            arrival_text[i] = new JTextField();
            burst_text[i] = new JTextField();
            order_label[i] = new JLabel();
            rows[i] = new JPanel(new FlowLayout());

            arrival_text[i].setPreferredSize(new Dimension(70, 30));
            burst_text[i].setPreferredSize(new Dimension(70, 30));

            arrival_text[i].setFont(new Font("Arial", Font.PLAIN, 20));
            burst_text[i].setFont(new Font("Arial", Font.PLAIN, 20));
            order_label[i].setFont(new Font("Arial", Font.PLAIN, 20));

            order_label[i].setText("P" + i + " ");

            rows[i].add(order_label[i]);
            rows[i].add(arrival_text[i]);
            rows[i].add(burst_text[i]);

            container.add(rows[i]);
        }

        display.setEditable(false);
        display.setPreferredSize(new Dimension(1050, 750));
        display.setFont(new Font("Lucida Console", Font.PLAIN, 20));

        calc_but.addActionListener(this);
        clear_but.addActionListener(this);
        big_but.addActionListener(this);
        small_but.addActionListener(this);

        JPanel but_container = new JPanel();

        but_container.add(calc_but);
        but_container.add(clear_but);
        but_container.add(big_but);
        but_container.add(small_but);

        container.add(but_container);

        add(container);
        add(display);

        setLayout(new FlowLayout());
        setResizable(false);
        setSize(1400, 800);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {

        if (e.getSource() == calc_but) {

            ArrayList<process> table = new ArrayList<>();
            int temp_arrival;
            int temp_burst;

            for (int i = 1; i < arrival_text.length; i++) {

                try {
                    temp_arrival = Integer.parseInt(arrival_text[i].getText());
                    temp_burst = Integer.parseInt(burst_text[i].getText());

                    table.add(new process(i, temp_arrival, temp_burst));

                } catch (Exception eee) {
                    break;
                }
            }

            try {
                non_sjf calculator = new non_sjf(table);

                display.setText(calculator.output);

            } catch (Exception eee) {
                System.out.println("smt wrong");
            }

        } else

        if (e.getSource() == clear_but) {
            for (int i = 0; i < 10; i++) {
                arrival_text[i].setText("");
                burst_text[i].setText("");
            }
        } else

        if (e.getSource() == big_but) {
            int temp = display.getFont().getSize();
            display.setFont(new Font("Lucida Console", Font.PLAIN, temp + 2));
        } else

        if (e.getSource() == small_but) {
            int temp = display.getFont().getSize();
            display.setFont(new Font("Lucida Console", Font.PLAIN, temp - 2));
        }

    }
}
