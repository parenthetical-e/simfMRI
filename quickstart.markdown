# A HOWTO #

 0. Install and dependencies
 1. A Really Simple Example
 2. A Simple Subclass Example
 3. An Example Using the Command Line
 4. Running the Rescorla-Wagner Code

## Install and dependencies ##


## A Really Simple Example. ##

Let's just get to it.  Start iPython.

Every experiment is in a class by itself.  Each though is based off of a common template.  Here is a Simple example, a 1 condition (with 60 trials) simulation run 1000 iterations.  Each iteration returns a results dictionary which is added a to list (called res).
		
	res = [simfMRI.exps.examples.Simple(60).run(str(ii)) 
			for ii in range(1000)]

So what happened?  Let's walk through Simple (and its template).

	class Simple(Exp):
		""" Run <n> one condition experiments. Return a list of results. """
		def __init__(self,n):
			try: Exp.__init__(self)
			except AttributeError: pass
		
			self.trials = np.array([0,]*n + [1,]*n)
			np.random.shuffle(self.trials)

		def model_1(self):
			""" A very simple example model. """

			from simfMRI.dm import construct

			self.create_dm('boxcar',True)
			self.create_bold(self.dm[:,1],False)

			self.dm = self.normalize_f(self.dm)
			self.bold = self.normalize_f(self.bold)

			self.fit()

The template class is Exp (found in simfMRI.template). 

[TODO] Discuss the template and its relevant attributes.  The move onto .run() and what it does, finally move onto model\_1() and the model\_N magic.

...

Then we needed to make some simulated trials. Let's say the experiment we want to model had only one condition, excluding the baseline, with 60 trials.  Further let's assume that there are equal numbers of experimental and baseline trials and that the experimental conditions were randomly interspersed.

To store these results to disk, I recommend using the hdf format.  It is fast, widely supported, and allows for slicing without loading the whole file into memory. We'll fittingly call it "simple.hdf5".  

	simfMRI.io.write_HDF(results,'simple.hdf5')

The structure of the results is mirrored in the hdf5 file.  To learn this structure, just play with a results object for a bit.  It should be straight forward.

To plot a histogram of each of the predictor's t-values, do:

	simfMRI.analysis.plot.hist_t(results)

Check out the other plot methods too.

And that is it... See the next section for a more practical example. There we'll define some new models.

## A TwoCond Example ##

TODO

## An Example Using the Command Line ##

TODO

## Running the Rescorla-Wagner Code ##

TODO

