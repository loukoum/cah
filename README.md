This is a hashing function I made using cellular automata in python3. It uses the binary form of the input as a space with two states for each cell (1 or 0). It starts by creating a N * N grid by evolving a N linear space N times (where N is the hash size in bits) and then it evolves this grid by one generation using Conway's GoL rules. The bit b0...bN of the hash is calculated by XORing every i cell of each row of the grid where i [0...255]. The linear space evolution rules are:

	1. The leftmost cell always has value of 1
	2. The rightmost cell has value x0 XOR x1 ... XOR x255 where x is the value of cellN of the previous generation
	3. All other cells evolve acording to their neighborhood which consists of the cell plus its left and right neighbors
	4. The next(evolved) value of cell b from neighborhood abc is:
		1. 000 -> 1
		2. 001 -> 0
		3. 010 -> 0
		4. 011 -> 1
		5. 100 -> 0
		6. 101 -> 1
		7. 110 -> 1
		8. 111 -> 0

The output is a N bit(default is 256b) hex string.
To run it, use: "python3 cah.py input salt iterations" where:

	- input: the input to hashed
	- salt: the salt
	- iterations: the number of hashing iterations

This project is not meant to create a secure hashing function but to show a practical way of using cellular automata. If you find any practical use of this please let me know!
