soln: soln.cpp util.hpp input.hpp
	g++ -Wall -Werror -o $@ soln.cpp

input.hpp: preprocess.py input
	./preprocess.py

clean:
	rm -f input.hpp soln
