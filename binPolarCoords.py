
import math
# code to calculate bin polar coordinates. 
#takes: x and z coords of bin and x and z coords of projectile
# returns bins distance and theta to travel to projectile

def binPolarCoords(x_bin, z_bin, x_projectile, z_projectile):

	if  x_bin > x_projectile and z_bin > z_projectile:
		theta_projectile = math.atan(abs(x_projectile - x_bin)/abs(z_projectile - z_bin))
		distance_projectile = abs(x_projectile - x_bin) / math.sin(theta_projectile)
		theta_projectile = math.degrees(theta_projectile)
		print 'quad 1'
		return theta_projectile, distance_projectile


	elif x_bin > x_projectile and z_projectile > z_bin:
		theta_projectile = 1.570796 + math.atan(abs(z_bin - z_projectile)/abs(x_projectile - x_bin))
		distance_projectile = abs(x_projectile - x_bin) / math.cos(theta_projectile-1.570796)
		theta_projectile = math.degrees(theta_projectile)
		print 'quad 2'

		return theta_projectile, distance_projectile


	elif x_projectile > x_bin and z_projectile > z_bin:
		theta_projectile = 3.141583 + math.atan(abs(x_projectile - x_bin)/abs(z_projectile - z_bin))
		distance_projectile = abs(x_projectile - x_bin) / math.sin(theta_projectile - 3.141583)
		theta_projectile = math.degrees(theta_projectile)
		print 'quad 3'

		return theta_projectile, distance_projectile



	elif x_projectile > x_bin and z_bin > z_projectile:
		theta_projectile = 4.712389 + math.atan2(abs(z_projectile - z_bin), abs(x_projectile - x_bin))
		distance_projectile = abs(x_projectile - x_bin) / math.cos(theta_projectile - 4.712389)
		theta_projectile = math.degrees(theta_projectile)
		print 'quad 4'

		return theta_projectile, distance_projectile



if __name__ == '__main__':
	theta1, dist1 = binPolarCoords(0,0,-50,-25)
	print "theta1 equals %d and dist1 equals %d" % (theta1, dist1)

	theta2, dist2 = binPolarCoords(0,0,-45,45)
	print "theta2 equals %d and dist2 equals %d" % (theta2, dist2)
	
	theta3, dist3 = binPolarCoords(0,0,60,60)
	print "theta3 equals %d and dist3 equals %d" % (theta3, dist3)

	theta4, dist4 = binPolarCoords(0,0,60,-45)
	print "theta4 equals %d and dist4 equals %d" % (theta4, dist4)
	


