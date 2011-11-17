"""
A set of functions to simulate the BOLD signal.
"""

def hrf(self, name):
	"""
	Returns a HRF using 'cannonical' parameters.
	"""
	
	if name == 'gamma':
		hr = [] # the returned hrf
		x = range(20)
		a1 = 6
		a2 = 12
		b1 = .9
		b1 = b2
		c = .35
		d1 = a1*b1
		d2 = a2*b2	
		f = lambda x: (x/d1)^a1 * exp( (d1-x)/ b1) - c * (x/d2)^a2 * exp( (d2-x)/ b2)
		[hr.append(f(x)) for ii in x]
	else:
		raise ValueError('name had an unknown value: {0}'.format(name))

	return hr


def glm(self):
	"""
	Caluates a voxel by voxel glm, regressing self.a.dm onto self.dataset.

	Returns: 
	1. The follwing model statistics for each voxel stored in .fa.[]
		B: the regression constant, Beta
		t: t-values for each voxel
		p: probability value
		F: the F-value
		
	2. The residuals for each sample are also stored in .a.residuals
	"""

	
def glm_contrast(self,contrast=[1,1,-1,0]):
	"""
	Exectues the statistical contrast specified, only works with datasets 
	after a glm has been run.
	"""


def filterByT(self,fraction):
	"""
	The top 'fraction' (0.01 -.99) of voxels (features) based on 
	t-values are selected.  
	- If .a.contrast is not specified an all versus baseline 
		[-1, 1 ...] will be employed by default.

	Returns:
	1. A (reduced) Dataset is returned (with attributes intact, as possible anyway).
	"""

def filterByInfo(self):


def filterBySD(self):


def genSimpleBOLD(self,numVoxels,noise=True):
	"""
	Creates a simple BOLD dataset with the number of voxels (a.k.a features) 
	specified at invocation.
	
	Simple here means the cannonical hrf is employed, the added noise is white,
	and the voxels are (as) evenly (as possible) divided between the 
	number of conditions in self.sa.labels.

	Requires that .sa.labels and/or .a.dm are defined, but if possible 
	are created as necessary.
	"""
	

def dummyLocations(self):
	"""
	In .fa.locations, create a list of dummy locations 
	(triplet tuples, starting with (0,0,0) ending with (N-1,N-1,N-1) 
	where N is the number of feature/voxels in self.samples).
	
	This will allow for easy compability when filtering 
	Brainvoyager vtc and roi data (and other real fMRI data sources).  
	"""
	

	locations = []
	[locations.append((loc,loc,loc)) for loc in range(self.shape[1])]
	self.fa.['locations'] = locations
	
	
def randLabels(self, num):
	"""
	Adds a randomly ordered list of N='num' conditions to self.sa.['labels'].
	It is the same length as the number of rows (samples) in self.dataset.
	"""
	from numpy.random import shuffle
	

	condList = []
	for cond in range(0,num):
		condList = condList + [cond] * self.shape[0]
	 
	self.sa.['labels'] = shuffle(cond)


def labelsToDm(self):
	"""
	Creates a desgin matrix from self.sa.labels and stores it in self.a.dm, 
	as well as creating self.a.condNames.  The Design matrix entries are {1,0}.
	"""
	from numpy import zeros,asarray


	labels = asarray(self.sa.labels)
	uniqueLabels = set(labels) 
		# set() sorts by default
	dm = zeros(self.shape(0),len(uniqueLabels))

	for ii, lab in enumerate(uniqueLabels):
		dm[labels == lab,ii] = 1 

	self.a.['dm'] = dm
	self.a.['condNames'] = uniqueLabels


def dmTolabels(self):
	"""
	Uses the design matrix attr (self.a.dm) to generate a labels list 
	(self.sa.labels); labels will be integers matching column counts
	in the design matrix, staring with 0.
	"""
	from numpy import asarray


	dm = asarray(self.a.dm)
	labels = [None] * self.shape[0] # none init
	for cond in range(dm.shape[1]):
		col = dm[...,cond]
		[labels.insert(ii,cond) for ii, ele in enumerate(col) if ele > 0]
		
	self.sa['labels'] = labels



