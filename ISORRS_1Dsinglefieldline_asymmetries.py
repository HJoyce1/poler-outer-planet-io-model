# outer loop to run through asymmetry parameters
def bulk_outflow(planet_name,dt,its,rs,lshell,FAC_flag,CF_flag,plots,saves,run_name):
    # ---------------------------------Imports-------------------------------------
    import numpy as np
    import matplotlib.pyplot as pl
    import ISORRS_dipolefield as dipolefield
    import ISORRS_equations_WIP as iseq
    import ISORRS_planet_WIP as planet
    import ISORRS_plotting_tools as ispl
    from matplotlib.ticker import FormatStrFormatter #need this for plotting extra significant figures on axes (ie FACs)
    # import inputs
    # ---------------------------------Start Main-------------------------------------
    # main folder to save plots and data to
    # MAC
    folder = '/Users/hannah/OneDrive - Lancaster University/ISORRS/2023/april/asym_runs/'
    # WINDOWS
    #folder = 'C:/Users/Knowhow/OneDrive - Lancaster University/ISORRS/2023/march/asym_runs/'
    
    # section to define inputs for this run ie what asymmetry to explore and what local time
    asymmetry = 'Density'
    local_time = 'Dusk'
    #-------------------------------Wrapper for Asymmetries--------------------------
    
    # create empty arrays for results
    AllTPS = []
    AllTMS = []
    AllTPSi = []

# if statements to define variables based on what local time and asymmetry type want to look at 
    # --------  TEMPERATURE ---------
    if asymmetry == 'Temperature' and local_time == 'Dawn':
        # set range of temperatures to iterate over
        temps = np.arange(500,1700,100)
        # set static variables
        den_H3_plus = 1e11
        den_H_plus = 5e10
        width = 1.04
        j = 3.7e-11
        colat = 16.6
        # data needed for console printout
        value = temps
        unit = '(K)'
        
    elif asymmetry == 'Temperature' and local_time == 'Dusk':
        # set range of temperatures to iterate over
        #temps = np.arange(500,1700,100)
        temps = np.arange(600,1100,100)
        # set static variables
        den_H3_plus = 3e15
        den_H_plus = 8e14
        width = 1
        j = 1e-11
        colat = 14.7
        # data needed for console printout
        value = temps
        unit = '(K)'
    
    # ---------- WIDTH -----------    
    elif asymmetry == 'Width' and local_time == 'Dawn':
        # set range of widths to iterate over
        widths = np.arange(0.25,5.25,0.25)
        # set static variables
        den_H3_plus = 1e11
        den_H_plus = 5e10
        b_temp = 950
        colat = 16.6
        j = 3.7e-11
        # data needed for console printout
        value = widths
        unit = '(Degrees)'
          
    elif asymmetry == 'Width' and local_time == 'Dusk':
        # set range of widths to iterate over
        widths = np.arange(0.25,5.25,0.25)
        # set static variables
        den_H3_plus = 1e11
        den_H_plus = 5e10
        b_temp = 850
        colat = 14.7
        j = 1e-11
        # data needed for console printout
        value = widths
        unit = '(Degrees)'
        
    # ------------ NUMBER DENSITY --------
    elif asymmetry == 'Density' and local_time == 'Dawn':
        # set range of densities to iterate over
        densi_H3_plus = np.array([1e9, 5e9, 1e10, 5e10, 1e11])
        densi_H_plus = np.array([1e8, 5e8, 1e9, 5e9, 1e10])
        dens_H3_plus = densi_H3_plus.astype(int)
        dens_H_plus = densi_H_plus.astype(int)
        #den_H3_plus = [1e9, 5e9, 1e10, 5e10, 1e11]
        #dens_H3_plus = np.logspace(1e9,1e11,num=5,dtype=int)
        #den_H_plus = [1e8, 5e8, 1e9, 5e9, 1e10]
        #dens_H_plus = np.logspace(1e8,1e10,num=5,dtype=int)
        # set static variables
        b_temp = 900
        width = 10
        colat = 19
        j = 3.7e-11
        # data needed for console printout
        value = dens_H_plus
        value_2 = dens_H3_plus
        unit = '(m^-3)'
        
    elif asymmetry == 'Density' and local_time == 'Dusk':
        densi_H3_plus = np.array([1e15, 25e14, 5e15, 75e14, 1e16])
        densi_H_plus = np.array([5e14, 75e13,1e15, 25e14, 5e15])
        dens_H3_plus = densi_H3_plus.astype(int)
        dens_H_plus = densi_H_plus.astype(int)
        b_temp = 700
        width = 1
        colat = 45
        j = 1e-11
        value = dens_H_plus
        value_2 = dens_H3_plus
        unit = '(m^-3)'
   
    # ------------ FIELD-ALIGNED CURRENT STRENGTH ----------     
    elif asymmetry == 'FACs' and local_time == 'Dawn':
        # set range of current strengths to iterate over
        FACS = np.arange(0.25,5.25,0.25)
        # set static variables
        den_H3_plus = 1e11
        den_H_plus = 5e10
        b_temp = 950
        width = 1.04
        colat = 16.6
        # data needed for console printout
        value = FACS
        unit = '(A)'
            
    elif asymmetry == 'FACs' and local_time == 'Dusk':
        # set range of current strengths to iterate over
        FACS = np.arange(0.25,5.25,0.25)
        # set static variables
        den_H3_plus = 1e11
        den_H_plus = 5e10
        b_temp =850
        width = 2.7
        colat = 14.7
        # data needed for console printout
        value = FACS
        unit = '(A)'
            
    else:
        print('invalid selection')
        exit()
        
        
        
    # set to run model over changing variable and printout for each run
    # loop one  - sets how many runs the model will complete
    for h in range(1, len(value)+1):
        number = value[h-1]
        if asymmetry == 'Density':
            number_2 = value_2[h-1] # only needed for density asymmetries
        print('--------------New Run-------------')
        print('Local Time:') 
        print(local_time)
        print('Run Number:')
        run_number = h
        print(h)
        print(asymmetry,unit,':')
        print(number)
        if asymmetry == 'Density':
            print(number_2) # only needed for density asymmetries
    
        # section to ensure looped varible assigned to correct variable in main body of code
        if asymmetry == 'Temperature':
            b_temp = number
        elif asymmetry == 'Width':
            width = number
        elif asymmetry == 'Density':
            den_H_plus = (number)
            den_H3_plus = (number_2)
        else: 
            j = (number)*1e-11
            
        
    # second loop - process to follow after asymmtry variables have been defined
    # this loop handles each individual run, where progressive run progresses onto the next 
    # asymmetry value in the array of the chosen asymmetry
    # it sets up other variables and imports needed data from other modules as well as 
    # providing a printout of the initial state of the model before the numerical method is applied
        if planet_name == 'jupiter' or planet == 'saturn':
        # ---------------------------------Grid set up-------------------------------------    
            inner = 1400000  #lower boundary, 1400km -> 140000m
            numpoints = int(rs*800)
            dz = 75000.0 # grid spacing, 75km -> 75000m
            
            # empty arrays for grid
            z=np.zeros([numpoints,])
            z_ext=np.zeros([numpoints+4,]) # for ghost points
            
            z[0] = inner # set lower boundary
            z_ext[0] = inner - 2*dz # set ghost points
            z_ext[1] = inner - dz
            for k in range(1,numpoints):
                z[k] = z[k-1] + dz # fill z array with values
            for l in range(1,numpoints+3):    
                z_ext[l+1] = z_ext[l] + dz #fill z_ext array with values
            x = np.linspace(0,numpoints-1,numpoints) # linear spaced array depending on number of grid points
            
            # ghost points only
            gb_z = np.linspace(z_ext[0],z_ext[1],2)
            ge_z = np.linspace(z_ext[-2],z_ext[-1],2)
            gb_x = np.linspace(-1,0,2)
            ge_x = np.linspace(numpoints,numpoints+1,2)
            
            ghosts = [gb_z,ge_z,gb_x,ge_x] # combine to read into input module
            
            # -------------------------Physical Constants----------------------------------
            # Constants set-up
            e_charge = 1.60217662*10**-19  # C - electron charge
            m_p = 1.6726219*10**-27 # kg - mass of a proton
            m_e = 9.10938356 * 10**-31  # kg - mass of an electron
            k_b = 1.38064852*10**-23 # m2 kg s-2 K-1  - boltzmann constant
            gamma = 5/3 # specific heat ratio
            
            phys_consts = [m_e,m_p,k_b,e_charge,gamma] # combine to read into inputs (planet) module
            
            # -----------------------READ IN INITIAL CONDITIONS----------------------------
            # choose planet for input module - name of planet no capitals
            if planet_name == 'jupiter':
                consts,A,ions,electrons,neutrals = planet.jupiter(its,phys_consts,z,z_ext,x,ghosts,b_temp,j,den_H_plus,den_H3_plus)
                print('-------Running for Jupiter--------')
            elif planet_name == 'saturn':
                consts,A,ions,electrons,neutrals = planet.saturn(its,phys_consts,z,z_ext,x,ghosts)
                print('-------Running for Saturn--------')       
            else:
                print('Incorrect planet_name input, please use ''jupiter'' or ''saturn''')
                exit()
        
        
            # optional field aligned currents    
            if FAC_flag != 1:
                FAC = np.zeros(np.size(z_ext)) #if testing with/without field aligned currents
                print('Field aligned currents removed')
            else:
                print('Field aligned currents included')
                if planet_name == 'jupiter':
                    # option for RAY2015 current density profile
                    FAC = j * (A[2]/A) #j[h-1]
                elif planet_name == 'saturn':
                    #option to include rudimental upward and downward current
                    FAC = - 0.3 * 1e-11  * (A[2]/A)
                        
         
            # preallocate arrays not used in initial conditions - electric field and flux
            E = np.empty([len(z)+4,its])
            E[:,0] = np.nan # no initial values for electric field
            e_flux = np.empty([len(z)+4,its])
            e_flux[:,0] = np.nan # no initial values for electron flux
            ion1_flux = np.empty([len(z)+4,its])
            ion1_flux[:,0] = np.nan # no initial values for electron flux
            ion2_flux = np.empty([len(z)+4,its])
            ion2_flux[:,0] = np.nan # no initial values for electron flux
            ion_flux_tot = np.empty([len(z)+4,its])
            ion_flux_tot[:,0] = np.nan # no initial values for total ion flux
            
            # unpack constants from dipole module
            radius = consts[0]
            mass_planet= consts[1]
            b0= consts[2]
            rot_period= consts[3]
            dipole_offset= consts[4]
            
            # determine number of ion and neutral species
            num_ionic_species = len(ions)
            num_neutral_species = len(neutrals)
            
            # # create empty arrays for looking at what the iterations are doing
            # ion_its= np.empty([len(z_ext),its,num_ionic_species,])
            # elec_its= np.empty([len(z_ext),its])
            # ion_its_T = np.empty([len(z_ext),its,num_ionic_species,])
            # elec_its_T = np.empty([len(z_ext),its])
            
            # ------ INITIAL DATA PLOT ------
            # plot input data, if using a lot of runs will want to turn plotting off
            if plots ==1:
                ispl.input_plot(ions,electrons,neutrals,z,z_ext,A,radius)  
                pl.savefig(folder+'inputs_plot_%s_%s.pdf' %(planet_name,run_name))
                
            # calculation for centrifugal and gravitational accelleration - from dipolefield
            phi,ag,ac = dipolefield.dipolefield_ISORRS(radius,inner,z[-1],mass_planet,b0,lshell,rot_period,dipole_offset,numpoints)   
               
        
            # optional centrifugal force    
            if CF_flag != 1:
                ac=np.zeros(np.size(ag)) # if testing with/without centrifugal acceleration
                print('Centrifugal force removed')
            else:
                print('Centrifugal force included')
            
            
            # preallocate arrays that are filled but then updated at next step 
            dMdt = np.empty([len(z_ext),num_ionic_species])
            dMdt_tmp = np.empty([len(z_ext),num_neutral_species])
            dEdt = np.empty([len(z_ext),num_ionic_species])
            dEdt_tmp = np.empty([len(z_ext),num_neutral_species])
            dArhou = np.empty([len(z_ext),num_ionic_species])
            dArhou2= np.empty([len(z_ext),num_ionic_species])
            dPdr= np.empty([len(z_ext),num_ionic_species])
            dTdr= np.empty([len(z_ext),num_ionic_species])
            dEngdr= np.empty([len(z_ext),num_ionic_species])
            dkdr= np.empty([len(z_ext),num_ionic_species])
            ion_flux = np.empty([len(z_ext),its,num_ionic_species,])
            
            dMdt_e = np.empty([len(z_ext)])
            dMdt_e_tmp = np.empty([len(z_ext),num_neutral_species])
            dEdt_e = np.empty([len(z_ext)])
            dEdt_e_tmp = np.empty([len(z_ext),num_neutral_species])
            
            
            if saves ==1:
                # create and open file to write in input data
                # this is a .txt file and can be read into the ISORRS_plotting_viwer module to visualise data
                fid = folder+"ISORRS_input_%s_%s_%s.txt" %(planet_name,run_name,run_number)
                f= open(fid,"w+")
                print('Data saved to file: %s ' %fid)
                f.write("-------SETUP------- \n")
                f.write("Planet=%s\n" %(planet_name))
                f.write("Time Step=%s\n" %(dt))
                f.write("Spatial Step=%s\n" %(dz))
                f.write("Iterations=%s\n" %(its))
                f.write("Outer limit =%s\n (RJ)" %(rs))
                f.write("L-Shell=%s\n" %(lshell))
                f.write("Field Aligned Currents removed:1,included:0 =%s\n" %(FAC_flag))
                f.write("Field Aligned Current Strength: %s\n" %(j))
                f.write("Centrifugal Stress  removed:1,included:0 =%s\n" %(CF_flag))
                f.write("Width of Region (degrees): %s\n" %(width))
                f.write("Colatitude Location (latitude): %s\n" %(colat))
                f.write("Initial Ionospheric Temperature (K): %s\n" %(b_temp))
                f.write("Number of Ionic species=%s\n" %(num_ionic_species))
                f.write("Number of Neutral species=%s\n" %(num_neutral_species))
                for s in range(1,num_ionic_species+1):
                    f.write("Ion Species %d: %s\n" %(s,ions[s]["name"]))
                for w in range(1,num_neutral_species+1):
                    f.write("Neutral Species %d: %s\n" %(w,neutrals[w]["name"]))
                f.write("-------VECTORS------- \n")   
                f.write("Current Density: \n")
                for vv in range(0,len(FAC)):
                    f.write('%s,' %(FAC[vv]))
                f.write("\n")    
             
                f.write("Cross Sectional Area of Flux  Tube / A: \n")
                for vw in range(0,len(A)):
                    f.write('%s,' %(A[vw]))
                f.write("\n")
              
                f.write("Spatial Grid: \n")
                for cc in range(0,len(z)):
                     f.write('%s,' %(z[cc]))
                f.write("\n")
                
                f.write("Gravitational Acceleration: \n")
                for aa in range(0,len(ag)):
                    f.write('%s,' %(ag[aa]))
                f.write("\n")
                
                f.write("Centrifugal Acceleration: \n")
                for bb in range(0,len(ac)):
                    f.write('%s,' %(ac[bb]))
                f.write("\n")
                f.write("-------ELECTRONS------- \n") 
                
                f.write("rho (kg/m^3): \n")
                for ee in range(0,len(electrons["rho"][2:-2,0])):
                    f.write('%s,' %(electrons["rho"][2:-2,0][ee]))
                f.write("\n")
                
                f.write("n (/m^3): \n")
                for ff in range(0,len(electrons["n"][2:-2,0])):
                    f.write('%s,' %(electrons["n"][2:-2,0][ff]))
                f.write("\n")
                
                f.write("u (m/s): \n")
                for gg in range(0,len(electrons["u"][2:-2,0])):
                    f.write('%s,' %(electrons["u"][2:-2,0][gg]))
                f.write("\n")
                
                f.write("P (Pa): \n")
                for hh in range(0,len(electrons["P"][2:-2,0])):
                    f.write('%s,' %(electrons["P"][2:-2,0][hh]))
                f.write("\n")  
                
                f.write("T (K): \n")
                for ii in range(0,len(electrons["T"][2:-2,0])):
                    f.write('%s,' %(electrons["T"][2:-2,0][ii]))
                f.write("\n")
                
                f.write("kappa: \n")
                for jj in range(0,len(electrons["kappa"][2:-2,0])):
                    f.write('%s,' %(electrons["kappa"][2:-2,0][jj]))
                f.write("\n")
                
                
                for kk in range(1,num_ionic_species+1):
                    f.write("-------%s------- \n" %ions[kk]["name"]) 
                
                    f.write("rho (kg/m^3): \n")
                    for ee in range(0,len(ions[kk]["rho"][2:-2,0])):
                        f.write('%s,' %(ions[kk]["rho"][2:-2,0][ee]))
                    f.write("\n")
                    
                    f.write("n (/m^3): \n")
                    for ff in range(0,len(ions[kk]["n"][2:-2,0])):
                        f.write('%s,' %(ions[kk]["n"][2:-2,0][ff]))
                    f.write("\n")
                    
                    f.write("u (m/s): \n")
                    for gg in range(0,len(ions[kk]["u"][2:-2,0])):
                        f.write('%s,' %(ions[kk]["u"][2:-2,0][gg]))
                    f.write("\n")
                    
                    f.write("P (Pa): \n")
                    for hh in range(0,len(ions[kk]["P"][2:-2,0])):
                        f.write('%s,' %(ions[kk]["P"][2:-2,0][hh]))
                    f.write("\n")  
                    
                    f.write("T (K): \n")
                    for ii in range(0,len(ions[kk]["T"][2:-2,0])):
                        f.write('%s,' %(ions[kk]["T"][2:-2,0][ii]))
                    f.write("\n")
                    
                    f.write("kappa: \n")
                    for jj in range(0,len(ions[kk]["kappa"][2:-2,0])):
                        f.write('%s,' %(ions[kk]["kappa"][2:-2,0][jj]))
                    f.write("\n")
                
                f.close()
            # ----------------------------------------------------------------------------   
            # third loop - this one runs the iterations themselves with the numerical method
            for i in range(1,its):
            
            # progress bar: 
            # int(32*i/its)*'■' works out the fraction of iterations completed
            # out of the maximum (i/its) multiplies it by 32, turns it into
            # a whole number, then repeats the ■ symbol that many times
            # the if statement means only update every 10th step
                if i%10==0:
                    print('\rIterating [{}{}] iteration {:5d}/{:5d}'.format(
                        int(32*i/its)*'■',(32-int(32*i/its))*' ',i,its),end='')
    
                
                for n in range(1,num_ionic_species+1):
                    for p in range(1,num_neutral_species+1):
                        # calculate momentum exchange rate for each neutral species
                        dMdt_tmp[:,p-1] = iseq.momentum_rate_1species(neutrals[p]["rho"],ions[n]["mass"],neutrals[p]["mass"],neutrals[p]["lambda"], e_charge,ions[n]["rho"][:,i-1],ions[n]["u"][:,i-1])
                        dEdt_tmp[:,p-1] = iseq.energy_rate_1species(ions[n]["rho"][:,i-1],neutrals[p]["rho"],ions[n]["mass"],neutrals[p]["mass"], neutrals[p]["lambda"], e_charge, neutrals[p]["T"],ions[n]["T"][:,i-1],ions[n]["u"][:,i-1],k_b)
                    
                        dMdt_e_tmp[:,p-1] = iseq.momentum_rate_1species(neutrals[p]["rho"],electrons["mass"],neutrals[p]["mass"],neutrals[p]["lambda"], e_charge,electrons["rho"][:,i-1],electrons["u"][:,i-1])
                        dEdt_e_tmp[:,p-1] = iseq.energy_rate_1species(electrons["rho"][:,i-1],neutrals[p]["rho"],electrons["mass"],neutrals[p]["mass"], neutrals[p]["lambda"], e_charge, neutrals[p]["T"],electrons["T"][:,i-1],electrons["u"][:,i-1],k_b)
                    
                    # sum each neutral species for each ionic species to get momentum exchange rate for each ionic species
                    dMdt[:,n-1] = - np.sum(dMdt_tmp, axis=1)
                    dMdt_tmp = np.empty([len(z_ext),num_neutral_species])
                    dEdt[:,n-1] = np.sum(dEdt_tmp, axis=1)
                    dEdt_tmp = np.empty([len(z_ext),num_neutral_species])
                    
                 
                    dMdt_e = - np.sum(dMdt_e_tmp,axis=1)
                    dMdt_e_tmp = np.empty([len(z_ext),num_neutral_species])
                    dEdt_e = np.sum(dEdt_e_tmp,axis=1)
                    dEdt_e_tmp = np.empty([len(z_ext),num_neutral_species])
                        
            
            # numerically calculate differentials - central difference using roll function
            # ions 
                for m in range(1,num_ionic_species+1):
                    dArhou[:,m-1] = (np.roll(A * ions[m]["u"][:,i-1] *ions[m]["rho"][:,i-1],-1) - np.roll(A * ions[m]["u"][:,i-1] *ions[m]["rho"][:,i-1],1))/(2*dz)
                    dArhou[0,m-1] = np.nan
                    dArhou[-1,m-1] = np.nan
                    
                    dArhou2[:,m-1]= (np.roll(A * ions[m]["u"][:,i-1]**2 * ions[m]["rho"][:,i-1],-1)-np.roll(A * ions[m]["u"][:,i-1]**2 * ions[m]["rho"][:,i-1],1))/(2*dz)
                    dArhou2[0,m-1] = np.nan
                    dArhou2[-1,m-1] = np.nan
                 
                    dPdr[:,m-1] = (np.roll(ions[m]["P"][:,i-1],-1)-np.roll(ions[m]["P"][:,i-1],1))/(2*dz)
                    dPdr[0,m-1] = np.nan
                    dPdr[-1,m-1] = np.nan 
                     
                    dTdr[:,m-1] = (np.roll(ions[m]["T"][:,i-1],-1)-np.roll(ions[m]["T"][:,i-1],1))/(2*dz)  
                    dTdr[0,m-1] = np.nan
                    dTdr[-1,m-1] = np.nan 
                    
                    #sign between rho and gamma was +
                    dEngdr[:,m-1]= (np.roll((0.5 * A * ions[m]["u"][:,i-1]**3 * ions[m]["rho"][:,i-1] + gamma/(gamma-1) * A * ions[m]["u"][:,i-1] * ions[m]["P"][:,i-1]),-1)-np.roll((0.5 * A * ions[m]["u"][:,i-1]**3 * ions[m]["rho"][:,i-1] + gamma/(gamma-1) * A * ions[m]["u"][:,i-1] * ions[m]["P"][:,i-1]),1))/(2*dz)
                    dEngdr[0,m-1] = np.nan
                    dEngdr[-1,m-1] = np.nan 
                            
                    dkdr[:,m-1] = (np.roll(ions[m]["kappa"][:,i-1],-1)-np.roll(ions[m]["kappa"][:,i-1],1))/(2*dz)
                    dkdr[0,m-1] = np.nan
                    dkdr[-1,m-1] = np.nan
                
                # second term in electric field equation - differential of electric field sum
                dEdr = (np.roll(iseq.E_second_term(electrons,ions,dMdt,num_ionic_species,i,dMdt_e),-1)-np.roll(iseq.E_second_term(electrons,ions,dMdt,num_ionic_species,i,dMdt_e),1))/(2*dz)
                dEdr[0] = np.nan
                dEdr[-1] = np.nan
                
                # electrons
                dAudr = (np.roll(A*electrons["u"][:,i-1],-1)-np.roll(A*electrons["u"][:,i-1],1))/(2*dz)
                dAudr[0] = np.nan
                dAudr[-1] = np.nan
            
                dTedr = (np.roll(electrons["T"][:,i-1],-1)-np.roll(electrons["T"][:,i-1],1))/(2*dz)  
                dTedr[0] = np.nan
                dTedr[-1] = np.nan    
                
                dPrhou2 = (np.roll(electrons["P"][:,i-1]+electrons["rho"][:,i-1]*electrons["u"][:,i-1]**2,-1)-np.roll(electrons["P"][:,i-1]+electrons["rho"][:,i-1]*electrons["u"][:,i-1]**2,1))/(2*dz)
                '''!!! between P and rho was +'''
                dPrhou2[0] = np.nan
                dPrhou2[-1] = np.nan
                
                dkdr_e = (np.roll(electrons["kappa"][:,i-1],-1)-np.roll(electrons["kappa"][:,i-1],1))/(2*dz) 
                dkdr_e[0] = np.nan
                dkdr_e[-1] = np.nan 
                
                # area differential
                dAdr = (np.roll(A,-1)-np.roll(A,1))/(2*dz)
                dAdr[0] = np.nan
                dAdr[-1] = np.nan
              
                # thermal conductivity temperature differential - negligibile for ions and electrons
                dakTdr =np.zeros(np.size(z_ext))
                dakTedr = np.zeros(np.size(z_ext))
                
                # parallel electric field (ambipolar)
                E[2:-2,i] = iseq.E_parallel_short(e_charge, electrons["n"][2:-2,i-1].T, dPrhou2[2:-2], A[2:-2].T, dAdr[2:-2], electrons["rho"][2:-2,i-1].T, electrons["u"][2:-2,i-1].T) + 1/(e_charge*electrons["n"][2:-2,i-1]) * dEdr[2:-2].T
                E[0:2,i]=iseq.extrap_start(E[2:-2,i])
                E[-2:,i]=iseq.extrap_end(E[2:-2,i])
            
                # updateing values for next step
                # ions
                for l in range(1,num_ionic_species+1):
                    # mass conservation equation
                    ions[l]["rho"][2:-2,i] = iseq.density_dt_ion(dt,A[2:-2],ions[l]["S"][2:-2],ions[l]["rho"][2:-2,i-1],dArhou[2:-2,l-1].T)
                    ions[l]["rho"][0:2,i]= iseq.extrap_start(ions[l]["rho"][2:-2,i])#ions[l]["rho"]#
                    ions[l]["rho"][-2:,i]= iseq.extrap_end(ions[l]["rho"][2:-2,i])
                    ions[l]["n"][2:-2,i] = ions[l]["rho"][2:-2,i] / ions[l]["mass"]
                    ions[l]["n"][0:2,i]= iseq.extrap_start(ions[l]["n"][2:-2,i])#ions[l]["n"][0:2,0]#
                    ions[l]["n"][-2:,i]= iseq.extrap_end(ions[l]["n"][2:-2,i])

                    # momentum conservation equation
                    ions[l]["u"][2:-2,i] = iseq.velocity_dt_ion(dt,A[2:-2],ions[l]["rho"][2:-2,i-1],ions[l]["rho"][2:-2,i],dArhou2[2:-2,l-1].T,dPdr[2:-2,l-1].T,ions[l]["mass"],E[2:-2,i],e_charge,-ag,dMdt[2:-2,l-1],ions[l]["u"][2:-2,i-1],ions[l]["S"][2:-2],ac)
                    ions[l]["u"][0:2,i]= iseq.extrap_start(ions[l]["u"][2:-2,i])#ions[l]["u"][0:2,0]#
                    ions[l]["u"][-2:,i]= iseq.extrap_end(ions[l]["u"][2:-2,i])
                    # energy conservation equation - add [2:-2,l-1] if trying to do dakTdr as =/= 0
                    ions[l]["P"][2:-2,i] = iseq.pressure_dt_ion(dt,A[2:-2],gamma,ions[l]["rho"][2:-2,i-1],ions[l]["rho"][2:-2,i],ions[l]["u"][2:-2,i-1],ions[l]["u"][2:-2,i],ions[l]["mass"], e_charge,E[2:-2,i],-ag,dEdt[2:-2,l-1],dMdt[2:-2,l-1],ions[l]["P"][2:-2,i-1],dEngdr[2:-2,l-1].T, dakTdr[2:-2].T,ions[l]["S"][2:-2],ac)
                    ions[l]["P"][0:2,i]= iseq.extrap_start(ions[l]["P"][2:-2,i])#ions[l]["P"][0:2,0]#i
                    ions[l]["P"][-2:,i]= iseq.extrap_end(ions[l]["P"][2:-2,i])#ions[l]["P"][0:2,0]#ions[l]["P"][-2:,0]
                    ions[l]["T"][2:-2,i] = iseq.plasma_temperature(ions[l]["n"][2:-2,i],k_b,ions[l]["P"][2:-2,i])
                    ions[l]["T"][0,i]=b_temp
                    ions[l]["T"][1,i]=b_temp
                    ions[l]["T"][-2:,i]= iseq.plasma_temperature(ions[l]["n"][-2:,i],k_b,ions[l]["P"][-2:,i])
                    # heat conductivities
                    ions[l]["kappa"][2:-2,i] = iseq.heat_conductivity(ions[l]["T"][2:-2,i],e_charge,ions[l]["mass"],m_p)
                    ions[l]["kappa"][0:2,i]= iseq.extrap_start(ions[l]["kappa"][2:-2,i])#ions[l]["kappa"][0:2,0]#
                    ions[l]["kappa"][-2:,i]= iseq.extrap_end(ions[l]["kappa"][2:-2,i])
                 
                # electrons
                # mass conservation
                electrons["rho"][2:-2,i] = iseq.density_dt_electron(electrons,ions,num_ionic_species,i)
                electrons["rho"][0:2,i]= iseq.extrap_start(electrons["rho"][2:-2,i])#electrons["rho"][0:2,0]#
                electrons["rho"][-2:,i]= iseq.extrap_end(electrons["rho"][2:-2,i])
                electrons["n"][2:-2,i] = electrons["rho"][2:-2,i] / electrons["mass"]
                electrons["n"][0:2,i]= iseq.extrap_start(electrons["n"][2:-2,i])#electrons["n"][0:2,0]#
                electrons["n"][-2:,i]= iseq.extrap_end(electrons["n"][2:-2,i])
                # momentum conservation
                electrons["u"][2:-2,i] = iseq.velocity_dt_electron(electrons,ions,num_ionic_species,i,FAC,e_charge)
                electrons["u"][0:2,i]= iseq.extrap_start(electrons["u"][2:-2,i])#electrons["u"][0:2,0]#
                electrons["u"][-2:,i]= iseq.extrap_end(electrons["u"][2:-2,i])
                # energy conservation
                electrons["T"][2:-2,i] = iseq.temperature_dt_electron(dt,gamma,electrons["mass"],k_b,A[2:-2],electrons["rho"][2:-2,i-1],electrons["u"][2:-2,i-1],electrons["T"][2:-2,i-1],electrons["S"][2:-2],dTedr[2:-2].T,dAudr[2:-2].T,dakTedr[2:-2].T,dEdt_e)
                electrons["T"][0:2,i]= iseq.extrap_start(electrons["T"][2:-2,i])#electrons["T"][0:2,0]#
                electrons["T"][-2:,i]= iseq.extrap_end(electrons["T"][2:-2,i])
                electrons["P"][2:-2,i] = iseq.plasma_pressure(electrons["rho"][2:-2,i]/electrons["mass"], k_b,electrons["T"][2:-2,i])
                electrons["P"][0:2,i]= iseq.extrap_start(electrons["P"][2:-2,i])#electrons["P"][0:2,0]#
                electrons["P"][-2:,i]= iseq.extrap_end(electrons["P"][2:-2,i])
                # heat conductivities
                electrons["kappa"][2:-2,i] = iseq.heat_conductivity_electrons((electrons["T"][2:-2,i]),e_charge,gamma)
                electrons["kappa"][0:2,i]= iseq.extrap_start(electrons["kappa"][2:-2,i])#electrons["kappa"][0:2,0]#
                electrons["kappa"][-2:,i]= iseq.extrap_end(electrons["kappa"][2:-2,i])
                
                '''
                MODIFICATION: I have removed the *A from the flux calculations as flux is u x n and should be displayed as that
                also, flux woulld not increase with the area as physically the outflow rate is consistent and so as the area expands the 
                particles spread out rather than multiply - additionally, as the flux is then later divided by A, this makes A irrelevant 
                to this calculation specifically (A may still have been used to calculate the terms used but is not directly involved)
                as such, /A is also removed from the total particle source (TPS) calculation
                '''
                # calculate electron and ion flux    
                for w in range(1,num_ionic_species+1):
                    ion_flux[2:-2,i,w-1] = ions[w]["n"][2:-2,i]*ions[w]["u"][2:-2,i] #* 1e-4# * A[2:-2] 
                # electron flux
                e_flux[2:-2,i] = iseq.electron_flux_e(electrons,i) #*1e-4#*A[2:-2]
                # total ion flux
                ion_flux_tot[2:-2,i] = np.add(ion_flux[2:-2,i,0],ion_flux[2:-2,i,1]) 
            
            # END OF ITERATIONS LOOP
            #---------------
            
            # --------- END OF RUN PLOTS -------
            # plots 2 figures, variables based on final iteration and results plot with electric field and fluxes
            if plots ==1:
                # outputs
                ispl.output_plots(ions, electrons, neutrals, z, z_ext, A, radius)
                pl.savefig(folder+'outputs_plot_%s_%s.pdf' %(planet_name,run_name))
                # results
                ispl.results_plot(z,z_ext,radius,num_ionic_species,e_charge,E[2:-2,-1],ions,electrons,ac,ag,e_flux,ion_flux,ion_flux_tot) 
                pl.savefig(folder+'overview_results_plot_%s_%s.pdf' %(planet_name,run_name))
                # species plot
            #     ispl.species_plot(z,z_ext,electrons,radius)
            #     pl.savefig(folder+'species_plot_%s_electrons_%s.png' %(planet_name,run_name))
            #     for q in range(1,num_ionic_species+1):
            # #            pl.figure(q+3)
            #         ispl.species_plot(z,z_ext,ions[q],radius)
            #         pl.savefig(folder+'species_plot_%s_%s_%s.png' %(planet_name,ions[q]['name'],run_name))
            
            # calculating total particle source
            ind = np.max(np.where(z<50000000)) +1 # at altitude where flux plateaus
            elef = e_flux[ind,-1] # electron flux at specific point
            ionf = np.empty([num_ionic_species])
            for v in range(1,num_ionic_species+1):
                ionf[v-1] = ion_flux[ind,-1,v-1]#/ A[ind] # ion flux at specific point
            
            arc = width/360 * 2*np.pi*(radius+50000000) # auroral arc of specific deg width
            circ = 2*np.pi*(radius+50000000)*np.sin(np.deg2rad(colat)) # auroral arc centred on colatitude point
            # circ is angle between centre of planet and the arc
            
            # calculate total particle source
            elecTPS = elef*arc*circ*2
            ion1TPS = ionf[0]*arc*circ*2
            ion2TPS = ionf[1]*arc*circ*2 
            TPS = 2*elecTPS
            TPSi = 2*(ion1TPS + ion2TPS)
            print('\n-------------Results--------------')
            print('Total particle source [s^-1]:')
            print(TPS)
            print(TPSi)
            
            # calculate total mass sourcea
            elecTMS = elecTPS * electrons['mass']
            ion1TMS = ion1TPS * ions[1]["mass"]
            ion2TMS = ion2TPS * ions[2]["mass"]
            TMS = (elecTMS+ion1TMS+ion2TMS)
            print('Total Mass Source [kgs^-1]:')
            print(TMS) 
            
            # add results from this loop to the array with all loops
            AllTPS.append(TPS)
            AllTMS.append(TMS)
            AllTPSi.append(TPSi)
            
            # write all output data to file
            # includes variables after final iteration, TPS, TMS, electric field data
            # can be exported into ISORRS_plotting_viewer to visualise data
            if saves ==1:
               fid_2 = folder+"ISORRS_output_%s_%s_%s.txt" %(planet_name,run_name,run_number)
               g = open(fid_2,"w+")
               print('Data saved to file: %s ' %fid_2)
               g.write("-------RESULTS------- \n")
               g.write("Total Electron Particle Source: %s\n" %(TPS))
               g.write("Total Ion Particle Source: %s\n" %(TPSi))
               g.write("Total Mass Source: %s\n" %(TMS))
               g.write("-------SETUP------- \n")
               g.write("Planet=%s\n" %(planet_name))
               g.write("Time Step=%s\n" %(dt))
               g.write("Spatial Step=%s\n" %(dz))
               g.write("Iterations=%s\n" %(its))
               g.write("Outer limit =%s\n (RJ)" %(rs))
               g.write("L-Shell=%s\n" %(lshell))
               g.write("Field Aligned Currents removed:1,included:0 =%s\n" %(FAC_flag))
               g.write("Field Aligned Current Strength: %s\n" %(j))
               g.write("Centrifugal Stress  removed:1,included:0 =%s\n" %(CF_flag))
               g.write("Width of Region (degrees): %s\n" %(width))
               g.write("Colatitude Location (latitude): %s\n" %(colat))
               g.write("Initial Ionospheric Temperature (K): %s\n" %(b_temp))
               g.write("Number of Ionic species=%s\n" %(num_ionic_species))
               g.write("Number of Neutral species=%s\n" %(num_neutral_species))
               for s in range(1,num_ionic_species+1):
                   g.write("Ion Species %d: %s\n" %(s,ions[s]["name"]))
               for w in range(1,num_neutral_species+1):
                   g.write("Neutral Species %d: %s\n" %(w,neutrals[w]["name"])) 
                   
               g.write("-------VECTORS------- \n")   
               g.write("Current Density: \n")
               for vv in range(0,len(FAC)):
                   g.write('%s,' %(FAC[vv]))
               g.write("\n")    
            
               g.write("A: \n")
               for vw in range(0,len(A)):
                   g.write('%s,' %(A[vw]))
               g.write("\n")
             
               g.write("Spatial Grid: \n")
               for cc in range(0,len(z)):
                    g.write('%s,' %(z[cc]))
               g.write("\n")
               
               g.write("Gravitational Acceleration: \n")
               for aa in range(0,len(ag)):
                   g.write('%s' %(ag[aa]))
               g.write("\n")
               
               g.write("Centrifugal Acceleration: \n")
               for bb in range(0,len(ac)):
                   g.write('%s,' %(ac[bb]))
               g.write("\n")
               
               g.write("Electric Field: \n")
               for dd in range(0,len(E[2:-2,-1])):
                   g.write('%s,' %(E[2:-2,-1][dd]))
               g.write("\n")
               
               g.write("-------ELECTRONS------- \n") 
               
               g.write("rho (kg/m^3): \n")
               for ee in range(0,len(electrons["rho"][2:-2,-1])):
                   g.write('%s,' %(electrons["rho"][2:-2,-1][ee]))
               g.write("\n")
               
               g.write("n (/m^3): \n")
               for ff in range(0,len(electrons["n"][2:-2,-1])):
                   g.write('%s,' %(electrons["n"][2:-2,-1][ff]))
               g.write("\n")
               
               g.write("u (m/s): \n")
               for gg in range(0,len(electrons["u"][2:-2,-1])):
                   g.write('%s,' %(electrons["u"][2:-2,-1][gg]))
               g.write("\n")
               
               g.write("P (Pa): \n")
               for hh in range(0,len(electrons["P"][2:-2,-1])):
                   g.write('%s,' %(electrons["P"][2:-2,-1][hh]))
               g.write("\n")  
               
               g.write("T (K): \n")
               for ii in range(0,len(electrons["T"][2:-2,-1])):
                   g.write('%s,' %(electrons["T"][2:-2,-1][ii]))
               g.write("\n")
               
               g.write("kappa: \n")
               for jj in range(0,len(electrons["kappa"][2:-2,-1])):
                   g.write('%s,' %(electrons["kappa"][2:-2,-1][jj]))
               g.write("\n")
               
               
               for kk in range(1,num_ionic_species+1):
                   g.write("-------%s------- \n" %ions[kk]["name"]) 
               
                   g.write("rho (kg/m^3): \n")
                   for ee in range(0,len(ions[kk]["rho"][2:-2,-1])):
                       g.write('%s,' %(ions[kk]["rho"][2:-2,-1][ee]))
                   g.write("\n")
                   
                   g.write("n (/m^3): \n")
                   for ff in range(0,len(ions[kk]["n"][2:-2,-1])):
                       g.write('%s,' %(ions[kk]["n"][2:-2,-1][ff]))
                   g.write("\n")
                   
                   g.write("u (m/s): \n")
                   for gg in range(0,len(ions[kk]["u"][2:-2,-1])):
                       g.write('%s,' %(ions[kk]["u"][2:-2,-1][gg]))
                   g.write("\n")
                   
                   g.write("P (Pa): \n")
                   for hh in range(0,len(ions[kk]["P"][2:-2,-1])):
                       g.write('%s,' %(ions[kk]["P"][2:-2,-1][hh]))
                   g.write("\n")  
                   
                   g.write("T (K): \n")
                   for ii in range(0,len(ions[kk]["T"][2:-2,-1])):
                       g.write('%s,' %(ions[kk]["T"][2:-2,-1][ii]))
                   g.write("\n")
                   
                   g.write("kappa: \n")
                   for jj in range(0,len(ions[kk]["kappa"][2:-2,-1])):
                       g.write('%s,' %(ions[kk]["kappa"][2:-2,-1][jj]))
                   g.write("\n")
               
               g.close()
        
        # end of each run
    
    # ------- AFTER RUNS ARE COMPLETE ----------
    
    fid_3 = folder+"ISORRS_rates_%s_%s.txt" %(planet_name,run_name)
    h = open(fid_3,"w+")
    print('Data saved to file: %s ' %fid_3)
    h.write("-------TPS------- \n")
    h.write('%s,' %AllTPS)
    h.write("\n") 
    h.write("-------TPSi------- \n")
    h.write('%s,' %AllTPSi)
    h.write("\n") 
    h.write("-------TMS------- \n")
    h.write('%s,' %AllTMS)
    h.write("\n") 
    
    # set TPS and TMS data into graphable format
    TPSarr = np.array(AllTPS)
    TPSgraph = np.array(TPSarr/1e24)
    TMSarr = np.array(AllTMS)
    
    TPSiarr = np.array(AllTPSi)
    TPSigraph = np.array(TPSiarr/1e24)
    
    # ------ VISUALISING THE ASYMMETRIES IN PLOTS ------
    # if statements depending on what asymmetry was run for what graph is to be plotted
    # plots a graph of TPS and TMS based on how the asymmetry changed the results
    if asymmetry == 'Temperature':
        fig5,ax5=pl.subplots(2,1,sharex=True,figsize=(10,7))
        pl.subplots_adjust(wspace=0,hspace=0)
        # temperature
        tempsarr = np.array(temps)
        e,f=np.polyfit(tempsarr, TPSgraph, 1)
        tempsfitP=(e*tempsarr+f)
        ax5[0].plot(tempsarr,tempsfitP, color='salmon',linestyle='dashed')
        ax5[0].plot(tempsarr,TPSgraph,'s')
        ax5[0].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax5[0].set_ylabel('Total Particle Source / $10^{24}$ (s$^{-1}$)')
        
        g,h=np.polyfit(tempsarr,TMSarr,1)
        tempsfitM=(g*tempsarr+h)
        ax5[1].plot(tempsarr, tempsfitM, color='salmon',linestyle='dashed')
        ax5[1].plot(tempsarr,TMSarr,'s')
        ax5[1].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax5[1].set_xlabel('Ionospheric Temperature (K)')
        ax5[1].set_ylabel('Total Mass Source (kgs$^{-1}$)')
        
    elif asymmetry == 'Width':
        fig4,ax4=pl.subplots(2,1,sharex=True,figsize=(10,7))
        pl.subplots_adjust(wspace=0,hspace=0)
        # widths
        widthsarr = np.array(widths)
        a,b=np.polyfit(widthsarr, TPSgraph, 1)
        widthsfitP = (a*widthsarr+b)
        ax4[0].plot(widthsarr, widthsfitP, color='green',linestyle='dashed')
        ax4[0].plot(widthsarr,TPSgraph,'o')
        ax4[0].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax4[0].set_ylabel('Total Particle Source / $10^{24}$ (s$^{-1}$)')
    
        c,d = np.polyfit(widthsarr, TMSarr, 1)
        widthsfitM = (c*widthsarr+d)
        ax4[1].plot(widthsarr, widthsfitM,color='lightseagreen',linestyle='dashed')
        ax4[1].plot(widths,AllTMS, 'o')
        ax4[1].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax4[1].set_xlabel('Auroral Width \N{DEGREE SIGN}')
        ax4[1].set_ylabel('Total Mass Source (kgs$^{-1}$)')
        
    elif asymmetry == 'FACs':
        fig6,ax6=pl.subplots(3,1,sharex=True,figsize=(12,12))
        pl.subplots_adjust(wspace=0,hspace=0)
        # FACs
        FACSarr=np.array(FACS)
        k,l=np.polyfit(FACSarr, TPSgraph, 1)
        FACSfitP = (k*FACSarr+l)
        ax6[0].plot(FACSarr, FACSfitP, color='orange',linestyle='dashed')
        ax6[0].plot(FACSarr,TPSgraph,'o')
        ax6[0].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax6[0].yaxis.set_major_formatter(FormatStrFormatter('%.10f'))
        ax6[0].set_ylabel('Total Particle Source / $10^{24}$ (s$^{-1}$)')
        
        o,p=np.polyfit(FACSarr,TPSigraph,1)
        FACSfitPi=(o*FACSarr+p)
        ax6[1].plot(FACSarr, FACSfitPi, color='peachpuff',linestyle='dashed')
        ax6[1].plot(FACSarr,TPSigraph,'o')
        ax6[1].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax6[1].yaxis.set_major_formatter(FormatStrFormatter('%.10f'))
        ax6[1].set_ylabel('Total Ion Particle Source / $10^{24}$ (s$^{-1}$)')
        
        
        m, n = np.polyfit(FACSarr, TMSarr, 1)
        FACSfitM =(m*FACSarr+n)
        ax6[2].plot(FACSarr, FACSfitM,color='sienna',linestyle='dashed')
        ax6[2].plot(FACS,TMSarr,'o')
        ax6[2].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax6[2].yaxis.set_major_formatter(FormatStrFormatter('%.10f'))
        ax6[2].set_ylabel('Total Mass Source (kgs$^{-1}$)')
        ax6[2].set_xlabel('Current Strength / $10^{-7}$ (A)')

    else:
        
        fig7,ax7=pl.subplots(3,1,sharex=True,figsize=(12,12))
        pl.subplots_adjust(wspace=0,hspace=0)
        # Densities
        Harr=(dens_H_plus/1e16)
        H3arr =np.array(dens_H3_plus/1e16)
        k,l=np.polyfit(Harr, TPSgraph, 1)
        p,q=np.polyfit(H3arr,TPSgraph, 1)
        HfitP = (k*Harr+l)
        H3fitP = (p*H3arr+q)
        ax7[0].plot(Harr, HfitP, color='orange',linestyle='dashed')
        ax7[0].plot(Harr,TPSgraph,'s',color='peru',label='$H^+$')
        ax7[0].plot(H3arr, H3fitP, color='teal',linestyle='dashed')
        ax7[0].plot(H3arr,TPSgraph,'^',color='blue',label='$H_3^+$')
        ax7[0].legend(loc='best',bbox_to_anchor=(0.11,0.97))
        ax7[0].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax7[0].yaxis.set_major_formatter(FormatStrFormatter('%.10f'))
        ax7[0].set_ylabel('Total Particle Source / $10^{24}$ (s$^{-1}$)')
    
        r,s=np.polyfit(Harr,TPSigraph,1)
        t,w = np.polyfit(H3arr,TPSigraph,1)
        HfitPi=(r*Harr+s)
        H3fitPi = (t*H3arr+w)
        ax7[1].plot(Harr, HfitPi, color='orange',linestyle='dashed')
        ax7[1].plot(Harr,TPSigraph,'s',color='peru')
        ax7[1].plot(H3arr, H3fitPi, color='teal',linestyle='dashed')
        ax7[1].plot(H3arr,TPSigraph,'^',color='blue')
        ax7[1].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax7[1].yaxis.set_major_formatter(FormatStrFormatter('%.10f'))
        ax7[1].set_ylabel('Total Ion Particle Source / $10^{24}$ (s$^{-1}$)')
        
        
        m, n = np.polyfit(Harr, TMSarr, 1)
        y,z = np.polyfit(H3arr, TMSarr, 1)
        HfitM =(m*Harr+n)
        H3fitM = (y*H3arr+z)
        ax7[2].plot(Harr, HfitM,color='orange',linestyle='dashed')
        ax7[2].plot(Harr,TMSarr,'s',color='peru')
        ax7[2].plot(H3arr, H3fitM,color='teal',linestyle='dashed')
        ax7[2].plot(H3arr,TMSarr,'^',color='blue')
        ax7[2].tick_params(direction='in',bottom=True, top=True, left=True, right=True)
        ax7[2].yaxis.set_major_formatter(FormatStrFormatter('%.10f'))
        ax7[2].set_ylabel('Total Mass Source (kgs$^{-1}$)')
        ax7[2].set_xlabel('Number Density / $10^{-16}$ (m$^{-3}$)')
            
        # save plot data
        pl.savefig(folder+'sources_plot_%s_%s.png' %(planet_name,run_name))
        print('Plots saved to: %s' %folder)
    
    
    # adjust plots for stacking
    pl.subplots_adjust(hspace=0.0,wspace=0.5)
    
    # return variables needed to export
    return b_temp,j,den_H_plus,den_H3_plus

# END OF MODULE
