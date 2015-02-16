def main():

	def zero():
		print("k")
	def one():
		print("kk")
		
	first = {	0x0 : zero,
				0x1 : one,
			}
	first[0]()
	
if __name__ == "__main__":
	main()