This program is a simulation for fire spread.
It simulates terrain, foliage spread, and fire spread.

Terrain:
	- Created from perlin noise (I did not create the implementation for this)
	- Does not change per frame

Foliage Spread:
	- Only spreads if:
		- The soil quality is good enough
		- The surrounding foliage density is enough
		- The elevation is in the correct range
		- The burn amount is 0
	- Soil quality:
		- increases if there's enough surrounding foliage
		- decreases otherwise

Fire Spread:
	- Only spreads if there's enough foliage
	- After fire burns out:
		- Foliage is reduced to 0
		- Burn amount is set to previous foliage density
		- Burn amount will reduce every frame
	- After burn amount is reduced to 0, the soil gets a boost
	- Randomly, lightning will strike a single cell on a frame, and if the cell has
		enough foliage, it will catch on fire

Parameters:
	-All parameters pertaining to individual cells are in the Cell.java source file as
		constants.
	-All parameters pertaining to everything else (perlin noise, lightning, matrix
		size, etc) are in the ScreenMatrix.java source file as constants (aside from
		window size, which is in Driver.java)
