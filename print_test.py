joy = -0.9

if joy > 0 or joy<0:
	angle = 45+45*joy
elif joy ==0:
	angle = 0

print(angle)
