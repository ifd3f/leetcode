soln: soln.cpp util.hpp input.hpp
	g++ -o $@ soln.cpp

input.hpp: preprocess.py input
	./preprocess.py

clean:
	rm -f input.hpp soln
