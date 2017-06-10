


def rawDepthToMeters(depthValue):
  if (depthValue < 2047):
    depth = (1.0 / ((depthValue) * -0.0030711016 + 3.3309495161))
    print 'depth value is %f' % depth
    return depth
  
  return 0

def depthToWorld( x,  y,  depthValue):
  fx_d = 1.0 / 5.9421434211923247e+02
  fy_d = 1.0 / 5.9104053696870778e+02
  cx_d = 3.3930780975300314e+02
  cy_d = 2.4273913761751615e+02
  depth =  rawDepthToMeters(depthValue)#depthLookUp[depthValue];//rawDepthToMeters(depthValue);
  x_result = ((x - cx_d) * depth * fx_d)
  y_result = ((y - cy_d) * depth * fy_d)
  z_result = depth
  return x_result, y_result, z_result



if __name__ == '__main__':
  data = [504, 374, 732.815,
  501, 370, 847.02698,
  499, 367, 829.65326,
  500, 364, 821.87213,
  497, 359, 823.26245,
  495, 350, 817.00494,
  488, 343, 819.89667,
  475, 343, 832.99707,
  465, 339, 848.711] 
  data_row = data[0:3]
  x_result, y_result, z_result = depthToWorld(data_row[1], data_row[0], data_row[2])
  print "x location is %f" % x_result
  print "y location is %f" % y_result
  print "z location is %f" % z_result



