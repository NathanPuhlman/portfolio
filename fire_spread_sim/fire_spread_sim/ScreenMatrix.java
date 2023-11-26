import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import javax.swing.JPanel;
import javax.swing.Timer;

/**
 * The class containing the main code in this program
 * Will permutate a matrix of cells and display them
 */
class ScreenMatrix extends JPanel implements ActionListener {

	// Constants
	private static Random rand = new Random();
	private static final int MATRIX_WIDTH = 200;
	private static final int MATRIX_HEIGHT = 200;
	private static final int NOISE_SCALE_X = MATRIX_WIDTH;
	private static final int NOISE_SCALE_Y = MATRIX_HEIGHT;
	private static final double NOISE_ELEVATION_OFFSET = 0.0;
	private static final int PIXEL_SIZE = 5;
	private static final int LIGHTNING_CHANCE = 100;
	private static final int LIGHTNING_FRAMES = 5;
	private static final double MIN_ELEVATION_BEFORE_FOLIAGE_START = 0.01;
	private static final int[] X_OFFSETS = new int[]{0, 1, 1, 1, 0, -1, -1, -1};
	private static final int[] Y_OFFSETS = new int[]{-1, -1, 0, 1, 1, 1, 0, -1};

	// Global variables
	private Timer timer = new Timer(1, this);
	private Cell[][] matrix = new Cell[MATRIX_WIDTH][MATRIX_HEIGHT];
	private long noiseSeed = rand.nextLong();
	private int lightningTimer = 0;
	
	/**
	 * The constructor for this class. Used to initialize the program
	 */
	public ScreenMatrix() {

		// Initialize every cell
		for(int x = 0; x < MATRIX_WIDTH; x++) {
			for(int y = 0; y < MATRIX_WIDTH; y++) {
				// Cell state
				// Elevation is generated with perlin noise
				double elevation = (double)Math.max(0.0, OpenSimplex2S.noise2(
							noiseSeed,
							(double)x / (double)NOISE_SCALE_X,
							(double)y / (double)NOISE_SCALE_Y) * 1.0
								+ NOISE_ELEVATION_OFFSET);
				double foliageDensity = 0.0;
				if (elevation > 0.0
						&& elevation < MIN_ELEVATION_BEFORE_FOLIAGE_START)
					foliageDensity = 1.0;
				double soilQuality = 1.0;
				boolean onFire = false;
				double burnAmount = 0.0;

				// Initialize the cell
				matrix[x][y] = new Cell(
						elevation,
						foliageDensity,
						soilQuality,
						onFire,
						burnAmount);
			}
		}
		
		// Start the timer
		timer.start();
	}
	
	/**
	 * Run a frame of the program.
	 * Permutates all the cells in the matrix and displays them.
	 */
	@Override
	public void actionPerformed(ActionEvent e) {

		// Initialization for this frame
		Cell[][] workingMatrix = new Cell[MATRIX_WIDTH][MATRIX_HEIGHT];
		boolean doLightning = rand.nextInt(LIGHTNING_CHANCE) == 0;
		int lightningX = rand.nextInt(workingMatrix.length);
		int lightningY = rand.nextInt(workingMatrix[0].length);
		if (doLightning) lightningTimer = LIGHTNING_FRAMES;
		int noFoliageCounter = 0;
		
		// Permutate all cells
		for(int x = 0; x < MATRIX_WIDTH; x++) {
			for(int y = 0; y < MATRIX_HEIGHT; y++) {
				// Make neighbors array
				Cell defaultCell = new Cell();
				Cell[] neighbors = new Cell[8];
				
				for(int i = 0; i < neighbors.length; i++) {
					int thisX = x + X_OFFSETS[i];
					int thisY = y + Y_OFFSETS[i];
					if (thisX > 0 && thisX < MATRIX_WIDTH - 1
							&& thisY > 0 && thisY < MATRIX_HEIGHT - 1)
						neighbors[i] = matrix[thisX][thisY];
					else
						neighbors[i] = defaultCell;
				}
				
				// Permutate this cell
				workingMatrix[x][y] = Cell.permutation(
						neighbors,
						matrix[x][y],
						doLightning && x == lightningX && y == lightningY);
				if (workingMatrix[x][y].getFoliageDensity() == 0)
					noFoliageCounter++;
			}
		}
		
		matrix = workingMatrix;
		// Draw cells
		repaint();

		if (noFoliageCounter == MATRIX_WIDTH * MATRIX_HEIGHT)
			System.out.println("Ran out of foliage! "
					+ "You need to restart the program");
	}
	
	/**
	 * Display all the cells in the matrix
	 */
	public void paintComponent(Graphics g) {
		Graphics2D g2d = (Graphics2D)g;
		super.paintComponent(g);
		
		// Draw all cells in the matrix
		for(int x = 2; x < MATRIX_WIDTH - 2; x++) {
			for(int y = 2; y < MATRIX_HEIGHT - 2; y++) {
				// Make neighbors array
				Cell defaultCell = new Cell(matrix[x][y].getElevation());
				Cell[] neighbors = new Cell[8];
				
				for(int i = 0; i < neighbors.length; i++) {
					int thisX = x + X_OFFSETS[i];
					int thisY = y + Y_OFFSETS[i];
					if (thisX > 0 && thisX < MATRIX_WIDTH - 1
							&& thisY > 0 && thisY < MATRIX_HEIGHT - 1)
						neighbors[i] = matrix[thisX][thisY];
					else
						neighbors[i] = defaultCell;
				}
				
				// Draw this cell
				Color thisColor = matrix[x][y].getColor(neighbors);
				if (lightningTimer % 2 == 1)
					thisColor = thisColor.brighter();
				g2d.setColor(thisColor);
				g2d.fillRect(x * PIXEL_SIZE, y * PIXEL_SIZE,
						PIXEL_SIZE, PIXEL_SIZE);
			}
		}
		
		lightningTimer--;
	}
}
