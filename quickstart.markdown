# A HOWTO #

 1. A Really Simple Example
 2. A Simple Subclass Example
 3. An Example Using the Command Line
 4. Running the Rescorla-Wagner Code

## A Really Simple Example. ##

Let's just get to it.  Start iPython.

First we need to make some simulated trials. Let's say the experiment we want to model had only one condition, excluding the baseline, with 60 trials.  Further let's assume that there are equal numbers of experimental and baseline trials and that the experimental conditions were randomly interspersed.

First we need numpy.
	
	import numpy as np

Now make 60 baseline (0) and experimental trials (1) then randomize their order.

	trials = np.array([0,]*60 + [1,]*60)
	np.random.shuffle(trials) 
		## done in place

Now import the simfMRI module and create an instance using the simulated trials we just made.  We have no data for parametric models (so data = {}, an empty dictionary, and both the ISI and TR are 2 seconds).

	# ERfMRI is a class, so we need to
	# make an experimental instance (called expi).
	from simfMRI import base.ERfMRI
	
	expi = ERfMRI(trials=trials,data={},TR=2,ISI=2)

Then just run the experiment.
	
	results = expi.run('test')

Or if you want to run 100 iterations with different simulated trial structure for each, do:

(Note: there are other ways to do this, see 2. and 3. below.)

	import numpy as np
	from simfMRI import base.ERfMRI

	trials = np.array([0,]*60 + [1,]*60)	
	
	# Were going to make a list of results.
	results = []
	
	for i in range(100):
		np.random.shuffle(trials)
		expi = ERfMRI(trials=trials,data={},TR=2,ISI=2)
		results.append(expi.run(i))
			## The loop counter is used to 
			## give each iteration a unique name

Store these results to disk in one big hdf5 file named "example_results.hdf5".  

	simfMRI.io.write_HDF('example_results.hdf5',results)

The structure of the results dictionary is exactly mirrored in the hdf5 file.  To learn this structure, just play with a results object for a bit.  It should be straight forward.

To plot a histogram of each of the predictor's t-values, do:

	simfMRI.plot.hist_t(results)

Check out the other plot methods too.

And that is it... err, no...  

See the next section for a more practical example.

## A Simple Subclass Example ##

TODO

## An Example Using the Command Line ##

TODO

## Running the Rescorla-Wagner Code ##

TODO

