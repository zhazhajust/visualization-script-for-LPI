#!/public/home/users/bio001/tools/python-2.7.11/bin/python
import sdf
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from numpy import ma
from matplotlib import colors, ticker, cm
from matplotlib.mlab import bivariate_normal
  
if __name__ == "__main__":
  print ('This is main of module "test2d.py"')
  ######## Constant defined here ########
  pi        =     3.1415926535897932384626
  q0        =     1.602176565e-19 # C
  m0        =     9.10938291e-31  # kg
  v0        =     2.99792458e8    # m/s^2
  kb        =     1.3806488e-23   # J/K
  mu0       =     4.0e-7*pi       # N/A^2
  epsilon0  =     8.8541878176203899e-12 # F/m
  h_planck  =     6.62606957e-34  # J s
  wavelength=     0.8e-6
  frequency =     v0*2*pi/wavelength
  
  exunit    =     m0*v0*frequency/q0
  bxunit    =     m0*frequency/q0
  denunit    =     frequency**2*epsilon0*m0/q0**2
  print 'electric field unit: '+str(exunit)
  print 'magnetic field unit: '+str(bxunit)
  print 'density unit nc: '+str(denunit)
  
  font = {'family' : 'monospace',  
          'color'  : 'black',  
          'weight' : 'normal',  
          'size'   : 20,  
          }  
  
  
  
  ######### Parameter you should set ###########
  start   =  2  # start time
  stop    =  15  # end time
  step    =  1  # the interval or step
  
  youwant = ['electron_en','electron_ekbar','ey','proton_ekbar','proton_en'] #,'electron_ekbar']
  #youwant =  ['bz','ex','ey_averaged','ez','electron_density','carbon_density','photon_density','positron_density','electron_ekbar','photon_ekbar','electron_x_px']
  #youwant field  ex,ey,ez,bx,by,bz,ex_averaged,bx_averaged...
  #youwant Derived electron_density,electron_ekbar...
  #youwant dist_fn electron_x_px, electron_py_pz, electron_theta_en...
  if (os.path.isdir('jpg') == False):
    os.mkdir('jpg')
  ######### Script code drawing figure ################
  for n in range(start,stop+step,step):
    #### header data ####
    print 'ok'
    data = sdf.read("./Data_p_2/"+str(n).zfill(4)+".sdf",dict=True)
    header=data['Header']
    time=header['time']
    print 'ok'
    x  = data['Grid/Grid_mid'].data[0]/1.0e-6
    print 'ok'
    y  = data['Grid/Grid_mid'].data[1]/1.0e-6
    X, Y = np.meshgrid(x, y)
    
    for name in youwant:
      if (name[0:2] == 'ex') or (name[0:2] == 'ey') or (name[0:2] == 'ez'):
                ex = data['Electric Field/'+str.capitalize(name)].data/exunit
	        np.savetxt('./txt/'+name+str(n).zfill(4)+'.txt', ex)
      elif (name[0:2] == 'bx') or (name[0:2] == 'by') or (name[0:2] == 'bz'):
                ex = data['Magnetic Field/'+str.capitalize(name)].data/bxunit
	        np.savetxt('./txt/'+name+str(n).zfill(4)+'.txt', ex)
      elif (name[-7:] == 'density'):
                den = data['Derived/Number_Density/'+name[0:-8]].data/denunit
	        np.savetxt('./txt/'+name+str(n).zfill(4)+'.txt', den)
      elif (name[-5:] == 'ekbar'):
                den = data['Derived/EkBar/'+name[0:-6]].data/(q0*1.0e6)
	        np.savetxt('./txt/'+name+str(n).zfill(4)+'.txt', den)
      elif (name[-4:] == 'x_px'):
                den = data['dist_fn/x_px/'+name[0:-5]].data[:,:,0]
                dist_x  = data['Grid/x_px/'+name[0:-5]].data[0]/1.0e-6
                dist_y  = data['Grid/x_px/'+name[0:-5]].data[1]/(m0*v0)
	        np.savetxt('./txt/'+name+'_data'+str(n).zfill(4)+'.txt', den)
	        np.savetxt('./txt/'+name+'_gridx'+str(n).zfill(4)+'.txt', dist_x)
	        np.savetxt('./txt/'+name+'_gridy'+str(n).zfill(4)+'.txt', dist_y)
      elif (name[-4:] == 'y_py'):
                den = data['dist_fn/y_py/'+name[0:-5]].data[:,:,0]
                dist_x  = data['Grid/y_py/'+name[0:-5]].data[0]/1.0e-6
                dist_y  = data['Grid/y_py/'+name[0:-5]].data[1]/(m0*v0)
	        np.savetxt('./txt/'+name+'_data'+str(n).zfill(4)+'.txt', den)
	        np.savetxt('./txt/'+name+'_gridx'+str(n).zfill(4)+'.txt', dist_x)
	        np.savetxt('./txt/'+name+'_gridy'+str(n).zfill(4)+'.txt', dist_y)
      elif (name[-5:] == 'py_pz'):
                den = data['dist_fn/py_pz/'+name[0:-6]].data[:,:,0]
                dist_x  = data['Grid/py_pz/'+name[0:-6]].data[0]/(m0*v0)
                dist_y  = data['Grid/py_pz/'+name[0:-6]].data[1]/(m0*v0)
	        np.savetxt('./txt/'+name+'_data'+str(n).zfill(4)+'.txt', den)
	        np.savetxt('./txt/'+name+'_gridx'+str(n).zfill(4)+'.txt', dist_x)
	        np.savetxt('./txt/'+name+'_gridy'+str(n).zfill(4)+'.txt', dist_y)
      elif (name[-8:] == 'theta_en'):
                denden = data['dist_fn/theta_en/'+name[0:-9]].data[:,:,0]
                dist_x  = data['Grid/theta_en/'+name[0:-9]].data[0]
                dist_y  = data['Grid/theta_en/'+name[0:-9]].data[1]/(q0*1.0e6)
	        np.savetxt('./txt/'+name+'_data'+str(n).zfill(4)+'.txt', den)
	        np.savetxt('./txt/'+name+'_gridx'+str(n).zfill(4)+'.txt', dist_x)
	        np.savetxt('./txt/'+name+'_gridy'+str(n).zfill(4)+'.txt', dist_y)
      elif (name[-2:] == 'en'):
                den = data['dist_fn/en/'+name[0:-3]].data[:,0,0]
                dist_x  = data['Grid/en/'+name[0:-3]].data[0]/(q0*1.0e6)
	        np.savetxt('./txt/'+name+'_data'+str(n).zfill(4)+'.txt', den)
	        np.savetxt('./txt/'+name+'_gridx'+str(n).zfill(4)+'.txt', dist_x)
    print 'finised '+str(round(100.0*(n-start+step)/(stop-start+step),4))+'%'
  

