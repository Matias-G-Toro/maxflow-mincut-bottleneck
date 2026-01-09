test:
	@python3 -m unittest test_flow.py

demo:
	@python3 main.py demo

benchmark:
	@python3 main.py benchmark

clean:
	@rm -f bench_*.csv demo_data.csv *.png
