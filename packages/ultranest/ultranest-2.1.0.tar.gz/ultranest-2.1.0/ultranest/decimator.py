"""Decimator zooms into relevant prior regions."""

from __future__ import print_function
from __future__ import division

import numpy as np

def zoom(cube_edge_lo, cube_edge_hi, j, u, i, D):
	cube_edge_lo = cube_edge_lo.copy()
	cube_edge_hi = cube_edge_hi.copy()
	
	oldwidths = cube_edge_hi - cube_edge_lo
	ndim = len(cube_edge_lo)
	
	for k in range(ndim):
		if k == j:
			width = oldwidths[k] / D
		else:
			width = oldwidths[k]
		
		ktop = u[i[0],k]
		klo = ktop - width / 2.
		khi = ktop + width / 2.
		if klo < 0:
			klo = 0.0
			khi = max(width, ktop + width / 2.)
		elif khi > 1:
			khi = 1.0
			klo = min(1 - width, ktop - width / 2.)
		print("new range:", klo, khi, ktop)
		# set new range
		if khi != klo:
			cube_edge_lo[k] = klo
			cube_edge_hi[k] = khi
	return cube_edge_lo, cube_edge_hi


def try_zooms(cube_edge_lo, cube_edge_hi, u, i, M, D):
	ndim = len(cube_edge_lo)
	oldwidths = cube_edge_hi - cube_edge_lo
	
	edges = []
	vols = []
	
	for j in range(ndim):
		cube_edge_lo_j = cube_edge_lo.copy()
		cube_edge_hi_j = cube_edge_hi.copy()
		
		
		for k in range(ndim):
			if k == j:
				# make a inner box where the top 10% are inside
				kinsides = u[i[:M],k]
				width = max(oldwidths[k] / D, 
					kinsides.max() - kinsides.min())
			else:
				width = oldwidths[k]
			
			ktop = u[i[0],k]
			klo = ktop - width / 2.
			khi = ktop + width / 2.
			if klo < 0:
				klo = 0.0
				khi = max(width, ktop + width / 2.)
			elif khi > 1:
				khi = 1.0
				klo = min(1 - width, ktop - width / 2.)
			#print("new range:", klo, khi, ktop)
			# set new range
			if khi != klo:
				cube_edge_lo_j[k] = klo
				cube_edge_hi_j[k] = khi
		
		edges.append((cube_edge_lo_j, cube_edge_hi_j))
		vols.append(np.log(cube_edge_hi_j - cube_edge_lo_j).sum())
	
	# select the axis that makes the smallest inner box
	j = np.argmin(vols)
	print("selecting axis:", j)
	for k in range(ndim):
		print("new range: ", edges[j][0][k], edges[j][1][k])
	return j, edges[j]


def decimate(ndim, prior_transform, loglikelihood, N=1000, D=10):
	cube_edge_lo = np.zeros(ndim)
	cube_edge_hi = np.ones(ndim)
	
	u = np.random.uniform(cube_edge_lo, cube_edge_hi, size=(N, ndim))
	v = prior_transform(u)
	L = loglikelihood(v)
	nevals = N
	
	M = int(N // D)
	while True:
		print("decimate iteration: L=%.1g-%.1g[%d]" % (L.min(), L.max(), N), cube_edge_lo, cube_edge_hi)
		# get top M
		i = np.argsort(L)[::-1]
		#utop = u[i[:M],:]
		# find the axis with the largest size reduction
		#toplo, tophi = utop.min(axis=0), utop.max(axis=0)
		oldwidths = cube_edge_hi - cube_edge_lo
		#top_widths = tophi - toplo
		#shrinkage = top_widths / oldwidths
		#print("widths:", toplo, tophi, top_widths)
		#j = np.argmin(shrinkage)
		#print("selecting axis:", j)
		Vprev = np.log(oldwidths).sum()
		# get the new range of that parameter
		#cube_edge_lo, cube_edge_hi = zoom(cube_edge_lo, cube_edge_hi, j, u, i, D)
		j, (cube_edge_lo, cube_edge_hi) = try_zooms(cube_edge_lo, cube_edge_hi, u, i, M, D)
		newwidths = cube_edge_hi - cube_edge_lo
		if newwidths[j] > oldwidths[j] / 1.1:
			print("all further divisions are minor", newwidths[j] / oldwidths[j])
			return cube_edge_lo, cube_edge_hi
		
		mask_inside = np.logical_and(u >= cube_edge_lo.reshape((1, -1)),
			u <= cube_edge_hi.reshape((1, -1))).all(axis=1)
		print("inside:", mask_inside.sum())
		# compute mass ratio
		V = np.log(cube_edge_hi - cube_edge_lo).sum()
		if mask_inside.all():
			print("all inside; stopping")
			return cube_edge_lo, cube_edge_hi
		Lmean_outside = np.max(L[~mask_inside])
		Lmean_inside = np.max(L[mask_inside])
		
		# verify that the inner volume is much more important
		if not (Lmean_inside + V > Lmean_outside + Vprev + np.log(10000)):
			print("likelihood is flattening; stopping (%d evals, lnV=%.1f)" % (nevals, V))
			return cube_edge_lo, cube_edge_hi
		
		# add new particles
		K = N - mask_inside.sum()
		
		unext = np.random.uniform(cube_edge_lo, cube_edge_hi, size=(K, ndim))
		vnext = prior_transform(unext)
		Lnext = loglikelihood(vnext)
		nevals += K
		
		u = np.vstack((u[mask_inside,:], unext))
		v = np.vstack((v[mask_inside,:], vnext))
		L = np.hstack((L[mask_inside], Lnext))
	
	
	
