# code to filter and fit curve 

# get 20 values, filter and fit curve. stop when limit is reached. 

 def fit_curve(x_vals, y_vals, limit)
	x_vals_filtered = []
	y_vals_filtered = []
 	for i in range(1,x_vals.size):
    	if abs(x_vals[i] - x_vals[i-1]) > 10 and abs(y_vals[i] - y_vals[i-1]) > 10:
        	x_vals_filtered.append(x_vals[i])
        	y_vals_filtered.append(y_vals[i])

    curve = np.poly1d(np.polyfit(x_vals_filtered, y_vals_filtered, 2))
    xp = np.linspace(200, limit, 100)
	for i in xp:
		if curve(i) < 10:
			print 'stopped'
			break




