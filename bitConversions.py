def unsigned(number, bits):
	number = int(number)
	bits = int(bits)
	limit = 2**bits
	while number > (limit - 1):
		number = number - limit
	while number < 0:
		number = number + limit
	return number