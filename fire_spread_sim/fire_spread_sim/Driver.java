import javax.swing.JFrame;

/**
 * The driver class for this program
 */
public class Driver {

	// Constants
	private static final int WINDOW_WIDTH = 512;
	private static final int WINDOW_HEIGHT = 512;

	// GUI window
	private JFrame window;

	/**
	 * Program start
	 */
	public Driver() {
		window = new JFrame();
		window.setSize(WINDOW_WIDTH, WINDOW_HEIGHT);
		window.setLocationRelativeTo(null);
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		window.setTitle("FIRE, FIRE, FIRE!!!");
		window.add(new ScreenMatrix());
		window.setVisible(true);
	}

	/**
	 * Program entry
	 */
	public static void main(String[] args) {
		new Driver();
	}
}
