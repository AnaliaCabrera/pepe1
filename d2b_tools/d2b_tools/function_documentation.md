##Guide about the organization of the program.
There are two bigger files, one of them is the base program named: 'measurements_reader.py' and the other is a several test that we use to probe small section of the first one  named: test_measurements_reader.py

#'measurements_reader.py'
First this have inside the data of **DEFAUL_CALIBRATION**, this come from the last know calibration. 

Then came several function:

**pixel_per_detector_generator(all_counts, pixel_amount)**
	
	Reads all the counts in a shot and returns a series of lists, each list of pixel_amount length

    :param all_counts: All the counts of the measurement per shot (128 detectors * 128 pixels per detector)
    :param pixel_amount: The number of pixels per detector (all detectors have the same number of pixels). ATENTION, in this place this parameter should not be variable

	The function consist in a *iterator*. We have a for that go from 0 to all_counts(128detector*128 pixels) whit step of pixel_amount (this is 128 pixels).
	
	*This code assume that the count information is written is shown in the following diagram:*

						16384   \/<<<<<<<^        <<<^
						^       \/       ^           ^
						^       \/       ^           ^
						   .                   .
						   .                   .
						   .                   .
						^       \/       ^   ....    ^
						^       \/       ^           ^
						^<<<<<<<\/       ^<<<        0

	*The first number is the count reading of the lowest pixel of the rightmost detector.
	The last number is the highest reading of the leftmost detector.*
	
	So we need to invert the odd detector, this is the same that invert all of pixels in a detector that are not even.
	Then the return of this function any time that we call it wive us a new number of pixels starting of the final + 1 than the last one.

*def get_metadata(segment_header_separator, segment)*

	
	