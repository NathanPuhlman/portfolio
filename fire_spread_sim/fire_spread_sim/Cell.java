import java.util.Random;
import java.util.Arrays;
import java.util.ArrayList;
import java.awt.Color;

/**
 * Class for a single cell
 * Simulates foliage density, soil quality, how burned it is, and if it's on fire.
 */
public class Cell implements Cloneable {

	/// Enums
	/**
	 * Keeps track of important events such as:
	 * 		when a fire catches
	 * 		when a fire extinguishes
	 * 		when a burn ends
	 * 		and all other times
	 */
	enum FireState {
		FIRE_STARTED,
		FIRE_ENDED,
		BOOST_SOIL,
		NORMAL
	}


	/// Private constants
	// Colors
	private static final Color WATER_COLOR = Color.BLUE;
	private static final Color FIRE_COLOR_1 = Color.YELLOW;
	private static final Color FIRE_COLOR_2 = Color.RED;
	private static final Color SOIL_RICH_COLOR = new Color(128, 64, 0);
	private static final Color SOIL_POOR_COLOR = Color.WHITE;
	private static final Color FOLIAGE_FULL_COLOR = new Color(0, 128, 0);
	private static final Color BURNED_COLOR = Color.GRAY;
	private static final double ELEVATION_SLOPE_EFFECT = 20.0d;

	// Fire constants
	private static final double CATCH_CHANCE_PER_FIRE = 1;
	private static final double CATCH_CHANCE = 10;
	private static final double MAX_FOLIAGE_DENSITY_BEFORE_CATCH = 0.2d;
	private static final double BURN_RATE = 0.05d;

	// Burned constants
	private static final double MAX_SOIL_BOOST_AFTER_RECOVERY = 0.5d;
	private static final double RECOVERY_RATE = 0.005d;

	// Soil constants
	private static final double MIN_FOLIAGE_DENSITY_BEFORE_SOIL_DECAY = 0.1d;
	private static final double SOIL_DECAY = 0.0001d;
	private static final double MAX_FOLIAGE_DENSITY_BEFORE_SOIL_RESTORE = 0.2d;
	private static final double SOIL_RESTORE = 0.02d;

	// Foliage constants
	private static final double MIN_ELEVATION_BEFORE_GROWTH = 0.7d;
	private static final double MAX_FOLIAGE_DENSITY_BEFORE_GROWTH = 0.1d;
	private static final double MAX_SOIL_QUALITY_BEFORE_GROWTH = 0.5d;
	private static final double MAX_GROWTH = 0.05d;
	private static final double START_GROWTH_RATIO = 0.1d;

	// Used to standardize permutation from neighbors
	private static final int NUM_NEIGHBORS = 8;

	// No need for multiple random variables
	private static Random rand = new Random();


	// Elevation of 0 means ocean, trees can't spread
	private double elevation;
	private double foliageDensity;	// Plant life in this cell, from 0 - 1
	private double soilQuality;		// Quality of the soil in this cell, from 0 - 1
	private boolean onFire;			// Is this cell on fire?
	private double burnAmount;		// Foliage can't spread when burned

	// Used for soil quality boost after recovery from fire
	private double foliageDensityBeforeFire = 0;

	/**
	 * Default constructor
	 */
	public Cell() {
		setOnFire(false);
		setElevation(0);
		setSoilQuality(0);
		setFoliageDensity(0);
		setBurnAmount(0);
	}

	/**
	 * Clone constructor
	 */
	public Cell(Cell cell) {
		elevation = cell.elevation;
		foliageDensity = cell.foliageDensity;
		soilQuality = cell.soilQuality;
		onFire = cell.onFire;
		burnAmount = cell.burnAmount;
		foliageDensityBeforeFire = cell.foliageDensityBeforeFire;
	}

	/**
	 * Construct with given elevation
	 * @param elevation the elevation to use for this cell
	 */
	public Cell(double elevation) {
		setOnFire(false);
		setElevation(elevation);
		setSoilQuality(0);
		setFoliageDensity(0);
		setBurnAmount(0);
	}

	/**
	 * Constructor to set all values
	 */
	public Cell(
			double elevation,
			double foliageDensity,
			double soilQuality,
			boolean onFire,
			double burnAmount) {
		setOnFire(onFire);
		setElevation(elevation);
		setSoilQuality(soilQuality);
		setFoliageDensity(foliageDensity);
		setBurnAmount(burnAmount);
	}

	/**
	 * Get the elevation of this cell
	 * @return the elevation of this cell
	 */
	public double getElevation() { return elevation; }

	/**
	 * Set the elevation for this cell
	 * @param elevation the elevation to set for this cell.
	 * 		Will be bounded by [0, 1]
	 */
	public void setElevation(double elevation) {
		if (elevation < 0)
			elevation = 0;
		if (elevation > 1)
			elevation = 1;
		this.elevation = elevation;
	}

	/**
	 * Get the foliage density of this cell
	 * @return the foliage density of this cell
	 */
	public double getFoliageDensity() { return foliageDensity; }

	/**
	 * Set the foliage density for this cell
	 * @param foliageDensity The foliage density to set for this cell.
	 *		Will be bounded by [0, 1]
	 */
	public void setFoliageDensity(double foliageDensity) {
		if (foliageDensity < 0)
			foliageDensity = 0;
		if (foliageDensity > 1)
			foliageDensity = 1;
		this.foliageDensity = foliageDensity;
	}

	/**
	 * Get the soil quality of this cell
	 * @return the soil quality of this cell
	 */
	public double getSoilQuality() { return soilQuality; }

	/**
	 * Set the soil quality for this cell
	 * @param soilQuality The soil quality to set for this cell.
	 * 		Will be bounded by [0, 1]
	 */
	public void setSoilQuality(double soilQuality) {
		if (soilQuality < 0)
			soilQuality = 0;
		if (soilQuality > 1)
			soilQuality = 1;
		this.soilQuality = soilQuality;
	}

	/**
	 * Get whether this cell is on fire or not
	 * @return true if this cell is on fire, false otherwise
	 */
	public boolean getOnFire() { return onFire; }

	/**
	 * Set whether this cell is on fire or not
	 * @param onFire the state of fire to set this cell to
	 */
	public void setOnFire(boolean onFire) { this.onFire = onFire; }

	/**
	 * Get the burn amount of this cell
	 * @return the burn amount of this cell
	 */
	public double getBurnAmount() { return burnAmount; }

	/**
	 * Set the burn amount for this cell
	 * @param burnAmount The burn amount to set for this cell
	 * 		Will be bounded by [0, 1]
	 */
	public void setBurnAmount(double burnAmount) {
		if (burnAmount < 0)
			burnAmount = 0;
		if (burnAmount > 1)
			burnAmount = 1;
		this.burnAmount = burnAmount;
	}

	/**
	 * Get a formatted string representing the state of this cell
	 * @return the formatted string
	 */
	public String toString() {
		return "Is " + (onFire ? "" : "not") + " on fire"
			+ "\nElevation: " + elevation
			+ "\nSoil Quality: " + soilQuality
			+ "\nFoliage Density: " + foliageDensity
			+ "\nBurn Amount: " + burnAmount;
	}

	/**
	 * Get a color to display that represents this cell
	 * @param neighbors the neighbors; used to find the slope
	 * @return the color to display
	 */
	public Color getColor(Cell[] neighbors) {

		// Water
		if (elevation == 0)
			return WATER_COLOR;

		double red = 0;
		double green = 0;
		double blue = 0;

		// Fire
		if (onFire) {
			double fireRand = rand.nextDouble();
			red = (double)FIRE_COLOR_1.getRed() / 256 * fireRand
					+ (double)FIRE_COLOR_2.getRed() / 256 * (1d - fireRand);
			green = (double)FIRE_COLOR_1.getGreen() / 256 * fireRand
					+ (double)FIRE_COLOR_2.getGreen() / 256 * (1d - fireRand);
			blue = (double)FIRE_COLOR_1.getBlue() / 256 * fireRand
					+ (double)FIRE_COLOR_2.getBlue() / 256 * (1d - fireRand);
			return new Color((float)red, (float)green, (float)blue);
		}

		// Soil
		red = (double)SOIL_RICH_COLOR.getRed() / 256 * soilQuality
				+ (double)SOIL_POOR_COLOR.getRed() / 256 * (1d - soilQuality);
		green = (double)SOIL_RICH_COLOR.getGreen() / 256 * soilQuality
				+ (double)SOIL_POOR_COLOR.getGreen() / 256 * (1d - soilQuality);
		blue = (double)SOIL_RICH_COLOR.getBlue() / 256 * soilQuality
				+ (double)SOIL_POOR_COLOR.getBlue() / 256 * (1d - soilQuality);

		if (burnAmount > 0) {
			// Burned
			red = (double)BURNED_COLOR.getRed() / 256 * burnAmount
					+ red * (1d - burnAmount);
			green = (double)BURNED_COLOR.getGreen() / 256 * burnAmount
					+ green * (1d - burnAmount);
			blue = (double)BURNED_COLOR.getBlue() / 256 * burnAmount
					+ blue * (1d - burnAmount);
		} else {
			// Foliage
			red = (double)FOLIAGE_FULL_COLOR.getRed() / 256 * foliageDensity
					+ red * (1d - foliageDensity);
			green = (double)FOLIAGE_FULL_COLOR.getGreen() / 256 * foliageDensity
					+ green * (1d - foliageDensity);
			blue = (double)FOLIAGE_FULL_COLOR.getBlue() / 256 * foliageDensity
					+ blue * (1d - foliageDensity);
		}

		// Slope highlight and shadow
		double leftSlope = elevation - neighbors[6].elevation;
		double rightSlope = neighbors[2].elevation - elevation;
		double upSlope = elevation - neighbors[0].elevation;
		double downSlope = neighbors[4].elevation - elevation;
		double slopeH = (leftSlope + rightSlope) * 0.5d;
		double slopeV = (upSlope + downSlope) * 0.5d;
		double slope = (slopeH + slopeV) * 0.5d;
		red = red + slope * ELEVATION_SLOPE_EFFECT;
		green = green + slope * ELEVATION_SLOPE_EFFECT;
		blue = blue + slope * ELEVATION_SLOPE_EFFECT;
		return new Color(
				(float)Math.max(0d, Math.min(1d, red)),
				(float)Math.max(0d, Math.min(1d, green)),
				(float)Math.max(0d, Math.min(1d, blue)));
	}

	/**
	 * Permutates a given cell into a new cell, based on its neighbors.
	 *
	 * @param neighbors an array of cells representing this cells neighbors.
	 * 		It must be arranged starting at the north cell, and going clockwise
	 * 		from there.
	 * @param thisCellOriginal the cell to permutate; typically located at the
	 * 		center of the neighbor cells
	 * @param doLightning whether this cell specifically was hit by lightning
	 * @return the copied and permutated cell
	 */
	public static Cell permutation(
			final Cell[] neighbors,
			final Cell thisCellOriginal,
			final boolean doLightning) {

		// Null checking
		if (thisCellOriginal == null || neighbors == null)
			return thisCellOriginal;
		if (neighbors.length != NUM_NEIGHBORS)
			return thisCellOriginal;
		for (Cell neighbor : neighbors)
			if (neighbor == null)
				return thisCellOriginal;

		// Copy the cell (just in case)
		Cell thisCell = new Cell(thisCellOriginal);

		// Nothing happens at sea level
		if (thisCell.elevation == 0)
			return thisCell;

		// Initialize the fire state this permutation
		FireState fireState = FireState.NORMAL;

		// Permutate onFire and burnAmount, then if either changes, change the fire state
		boolean beforeFire = thisCell.onFire;
		double beforeBurned = thisCell.burnAmount;
		// Fire permutations
		thisCell.setOnFire(onFireNeighborsPermutation(thisCell, neighbors));
		thisCell.setOnFire(onFireSelfPermutation(thisCell, doLightning));
		if (thisCell.onFire != beforeFire) {
			// This cell just caught fire
			if (thisCell.onFire) {
				fireState = FireState.FIRE_STARTED;
				thisCell.foliageDensityBeforeFire = thisCell.foliageDensity;
			}
			// This cell's fire just extinguished
			if (!thisCell.onFire) fireState = FireState.FIRE_ENDED;
		}
		// Burn permutations
		thisCell.setBurnAmount(burnAmountSelfPermutation(thisCell, fireState));
		// This cell just recovered from a fire
		if (thisCell.burnAmount != beforeBurned && thisCell.burnAmount == 0)
			fireState = FireState.BOOST_SOIL;

		// Permutate based on neighbors
		thisCell.setSoilQuality(soilQualityNeighborsPermutation(
				thisCell, neighbors));
		thisCell.setFoliageDensity(foliageDensityNeighborsPermutation(
				thisCell, neighbors));

		// Permutation without need of neighbors
		thisCell.setSoilQuality(soilQualitySelfPermutation(thisCell, fireState));
		thisCell.setFoliageDensity(foliageDensitySelfPermutation(thisCell));

		// The cell has been permutated
		return thisCell;
	}

	/**
	 * Permutate the fire state of this cell given its neighbors
	 * @param thisCell the cell whose fire state needs to be permutated
	 * @param neighbors the surrounding cells whose fire may spread
	 * @return the new fire state for this cell
	 */
	private static boolean onFireNeighborsPermutation(
			final Cell thisCell,
			final Cell[] neighbors) {

		// Already on fire, cannot catch twice!
		if (thisCell.onFire)
			return true;
		// There must be enough foliage to catch
		if (thisCell.foliageDensity < MAX_FOLIAGE_DENSITY_BEFORE_CATCH)
			return false;

		// Find the intensity of the surrounding fires
		// Down wind fires have a lower effect
		// Up wind fires have a greater effect
		// All other fires have a medium effect
		double fireIntensity = 0;
		for (Cell neighbor : neighbors)
			if (neighbor.onFire)
				fireIntensity += CATCH_CHANCE_PER_FIRE;

		// Find the new fire state
		fireIntensity = Math.max(0f, fireIntensity);
		if (fireIntensity == 0 || thisCell.foliageDensity == 0)
			return false;
		else {
			double catchChance = CATCH_CHANCE
					/ (fireIntensity * thisCell.foliageDensity);
			if (Math.round(catchChance) == 0)
				return true;
			if (Math.round(rand.nextDouble() * catchChance) == 0)
				return true;
		}

		// Low intensity or low foliage
		return false;
	}

	/**
	 * Permutate the fire state of this cell without neighbors
	 * @param thisCell the cell whose fire state needs to be permutated
	 * @param doLightning has this cell specifically been hit by lightning?
	 * @return the new fire state for this cell
	 */
	private static boolean onFireSelfPermutation(
			final Cell thisCell,
			final boolean doLightning) {

		// If this cell was selected to be hit by lightning, catch fire
		if (doLightning && thisCell.foliageDensity != 0)
			return true;
		// No other case for spontaneous combustion
		if (!thisCell.onFire)
			return false;
		// Foliage just ran out
		if (thisCell.foliageDensity == 0)
			return false;
		// Keep on burnin'
		return true;
	}

	/**
	 * Permutate the burn amount of this cell without neighbors
	 * @param thisCell the cell whose burn amount needs to be permutated
	 * @param fireState the firestate of this cell to check when a fire ends
	 * @return the new burn amount for this cell
	 */
	private static double burnAmountSelfPermutation(
			final Cell thisCell,
			final FireState fireState) {

		// Recovering from fire
		if (thisCell.burnAmount > 0)
			return thisCell.burnAmount - RECOVERY_RATE;
		// Start recovery from fire
		if (fireState == FireState.FIRE_ENDED)
			return thisCell.foliageDensityBeforeFire;
		// Not recovering from fire
		return 0d;
	}

	/**
	 * Permutate the soil quality of this cell given its neighbors
	 * @param thisCell the cell whose soil quality needs to be permutated
	 * @param neighbors the surrounding cells whose foliage may restor/decay this
	 * 		cell's soil quality
	 * @return the new soil quality for this cell
	 */
	private static double soilQualityNeighborsPermutation(
			final Cell thisCell,
			final Cell[] neighbors) {

		// Get average surrounding foliage density
		double totalFoliage = 0;
		for (Cell neighbor : neighbors)
			totalFoliage += neighbor.foliageDensity;
		double averageFoliage = totalFoliage / NUM_NEIGHBORS;

		// If there isn't enough surrounding foliage, this soil will decay
		if (averageFoliage < MIN_FOLIAGE_DENSITY_BEFORE_SOIL_DECAY)
			return thisCell.soilQuality - SOIL_DECAY;
		// If there's enough surrounding foliage, this soil will restore
		if (averageFoliage >= MAX_FOLIAGE_DENSITY_BEFORE_SOIL_RESTORE)
			return thisCell.soilQuality + SOIL_RESTORE;
		// This soil will not change
		return thisCell.soilQuality;
	}

	/**
	 * Permutate the foliage density of this cell given its neighbors
	 * @param thisCell the cell whose foliage density needs to be permutated
	 * @param neighbors the surrounding cells whose foliage may spread
	 * @return the new foliage density for this cell
	 */
	private static double foliageDensityNeighborsPermutation(
			final Cell thisCell,
			final Cell[] neighbors) {

		// Get average surrounding foliage density
		double totalFoliage = 0;
		for (Cell neighbor : neighbors)
			totalFoliage += neighbor.foliageDensity;
		double averageFoliage = totalFoliage / NUM_NEIGHBORS;

		// Can foliage from neighbor cells spread?
		if (thisCell.foliageDensity == 0
				&& thisCell.elevation < MIN_ELEVATION_BEFORE_GROWTH
				&& thisCell.soilQuality > MAX_SOIL_QUALITY_BEFORE_GROWTH
				&& thisCell.burnAmount == 0
				&& averageFoliage > MAX_FOLIAGE_DENSITY_BEFORE_GROWTH)
			return averageFoliage * START_GROWTH_RATIO;

		// Foliage doesn't spread
		return thisCell.foliageDensity;
	}

	/**
	 * Permutate the soil quality of this cell without neighbors
	 * @param thisCell the cell whose soil quality needs to be permutated
	 * @param fireState this cell's firestate; used to boost the soil after recovery
	 * 		from fire
	 * @return the new soil quality for this cell
	 */
	private static double soilQualitySelfPermutation(
			final Cell thisCell,
			final FireState fireState) {

		// If the cell just recovered, give a boost to the soil
		if (fireState == FireState.BOOST_SOIL)
			return thisCell.soilQuality
					+ MAX_SOIL_BOOST_AFTER_RECOVERY
					* thisCell.foliageDensityBeforeFire;

		// If there isn't enough foliage, this soil will decay
		if (thisCell.foliageDensity < MIN_FOLIAGE_DENSITY_BEFORE_SOIL_DECAY)
			return thisCell.soilQuality - SOIL_DECAY;
		// If there's enough foliage, this soil will restore
		if (thisCell.foliageDensity >= MAX_FOLIAGE_DENSITY_BEFORE_SOIL_RESTORE)
			return thisCell.soilQuality + SOIL_RESTORE;
		// This soil will not change
		return thisCell.soilQuality;
	}

	/**
	 * Permutate the foliage density of this cell without neighbors
	 * @param thisCell the cell whose foliage density needs to be permutated
	 * @return the new foliage density for this cell
	 */
	private static double foliageDensitySelfPermutation(final Cell thisCell) {

		// Foliage cannot spontaneously appear
		if (thisCell.foliageDensity == 0)
			return 0;

		// This cell is burning
		if (thisCell.onFire)
			return thisCell.foliageDensity - BURN_RATE;

		// This cell can grow
		// If the soil is good enough, the foliage will grow
		// If the soil is too poor, the foiliage will die
		if (thisCell.burnAmount == 0)
			return thisCell.foliageDensity +
					(thisCell.soilQuality - MAX_SOIL_QUALITY_BEFORE_GROWTH)
					* rand.nextDouble() * MAX_GROWTH;

		// This cell is burnt
		return 0;
	}
}
