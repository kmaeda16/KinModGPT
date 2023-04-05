import tellurium as te
import pandas as pd
from matplotlib import pyplot as plt
import roadrunner as rr



# Use the following two lines if plots do not show up.
import matplotlib
matplotlib.use('TkAgg')



def main():
    model_name = 'heat_shock_response'
    sbml_model = readSBMLModel("../../Conversion/4. KinModGPT_text-davinci-003/Results/{}/{}_SBML_model.xml".format(model_name,model_name))
    r = rr.RoadRunner(sbml_model)
    
    # Change parameter values and initial concentrations
    setParameters(r)
    
    print('======= Parameters =======')
    for name, val in zip(r.getGlobalParameterIds(),r.getGlobalParameterValues()):
        print('{}\t=\t{:e}'.format(name,val))
    print('==========================')
        
    df_result1 = simulation(r,tstart=-60,tend=0,npoints=121)
    r.kc_Pfold_Punfold *= 2 # heat shock
    r.kp_mRNA_s32_s32  *= 4 # heat shock
    df_result2 = simulation(r,tstart=0,tend=40,npoints=81)
    
    df_result = pd.concat([df_result1, df_result2.iloc[1:,:]], axis=0)
    df_result.to_csv("{}_SBML_result.csv".format(model_name),index=False,float_format="%.6e")

    myplot(df_result,model_name)



def readSBMLModel(path):
    with open(path) as f:
        sbml_model = f.read()
    return(sbml_model)



def simulation(r,tstart=0,tend=10,npoints=50):
    # r = te.loada(ant_model)
    r.integrator.setValue('absolute_tolerance', 1e-30)
    result = r.simulate(tstart, tend, npoints)
    matrix = result[:]
    col = []
    for i, c in enumerate(r.selections):
        c = c.replace('[', '').replace(']', '')
        col.append(c)
        print("{}\t{}".format(i,c))
    df_result = pd.DataFrame(matrix,columns=col)
    return(df_result)



def myplot(df_result,model_name):
    columns = df_result.columns
    time = df_result.iloc[:,0].values.squeeze()
    for i, c in enumerate(columns[1:]):
        y = df_result.iloc[:,i+1].values.squeeze()
        plt.plot(time,y,label=c)
    
    plt.xlabel("Time")
    plt.ylabel("Conc.")
    plt.legend()
    # plt.show()
    plt.savefig("{}_SBML_result.png".format(model_name))



def setParameters(r):
    # Maeda and Kurata, J Theor Biol, 2011.

    r.D = 0.0118
    G = 2.54e-09
    Ts70 = 700 * G
    TRNAP = 2000 * G
    TPg = 4000 * G
    TPh = 30 * G

    # The original model is a DAE model. So, it is assumed that association and dissociation are so fast.
    factor = 1e+6

    # Kb[1]
    r.ka_s70_RNAP = 1e+9 * factor
    r.kd_s70_RNAP = 1 * factor

    # Kb[2]
    r.ka_Pg_s70_RNAP = 1e+9 * factor
    r.kd_Pg_s70_RNAP = 1 * factor

    # Kb[3]
    r.ka_RNAP_s32 = 1e+9 * factor
    r.kd_RNAP_s32 = 1 * factor

    # Kb[4]
    r.ka_Ph_RNAP_s32 = 1e+9 * factor
    r.kd_Ph_RNAP_s32 = 1 * factor

    # Kb[5]
    r.ka_s32_DnaK = 1e+7 * factor
    r.kd_s32_DnaK = 1 * factor

    # Kb[6]
    r.ka_s32_FtsH = 1e+8 * factor
    r.kd_s32_FtsH = 1 * factor

    # Kb[7]
    r.ka_Punfold_DnaK = 1e+6 * factor
    r.kd_Punfold_DnaK = 1 * factor

    # Kb[8]
    r.ka_D_s70_RNAP = 1e+5 * factor
    r.kd_D_s70_RNAP = 1 * factor

    # Kb[9]
    r.ka_D_RNAP_s32 = 1e+5 * factor
    r.kd_D_RNAP_s32 = 1 * factor

    # Kb[10]
    r.ka_RNAP_D = 1e+6 * factor
    r.kd_RNAP_D = 1 * factor

    # Kb[6]
    r.ka_s32_DnaK_FtsH = 1e+8 * factor
    r.kd_s32_DnaK_FtsH = 1 * factor

    # kx[1]
    r.kc_s32_FtsH = 5
    r.kc_s32_DnaK_FtsH = 5

    # kx[2]
    r.kc_Pfold_Punfold = 75

    # kx[3]
    r.kc_Punfold_DnaK = 15000

    # kp[1-4]
    r.kp_mRNA_s32_s32 = 20
    r.kp_mRNA_FtsH_FtsH = 20
    r.kp_mRNA_DnaK_DnaK = 20
    r.kp_mRNA_Protein_Pfold = 20

    # kpd[1-4]
    r.kdeg_s32 = 0.03
    r.kdeg_RNAP_s32 = 0.03
    r.kdeg_Ph_RNAP_s32 = 0.03
    r.kdeg_s32_DnaK = 0.03
    r.kdeg_s32_FtsH = 0.03
    r.kdeg_D_RNAP_s32 = 0.03
    r.kdeg_s32_DnaK_FtsH = 0.03
    r.kdeg_FtsH = 0.03
    r.kdeg_DnaK = 0.03
    r.kdeg_Punfold_DnaK = 0.03
    r.kdeg_Pfold = 0.03
    r.kdeg_Punfold = 0.03

    # km[1-4]
    r.km_mRNA_s32_Pg_s70_RNAP = 20 * G
    r.K_mRNA_s32_Pg_s70_RNAP = 0.5 * TPg
    r.n_mRNA_s32_Pg_s70_RNAP = 1
    r.km_mRNA_DnaK_Ph_RNAP_s32 = 500 * G
    r.K_mRNA_DnaK_Ph_RNAP_s32 = 0.5 * TPh
    r.n_mRNA_DnaK_Ph_RNAP_s32 = 1
    r.km_mRNA_FtsH_Ph_RNAP_s32 = 20 * G
    r.K_mRNA_FtsH_Ph_RNAP_s32 = 0.5 * TPh
    r.n_mRNA_FtsH_Ph_RNAP_s32 = 1
    r.km_mRNA_Protein = 1500 * G

    # kmd[1-4]
    r.kdeg_mRNA_s32 = 0.5
    r.kdeg_mRNA_DnaK = 0.5
    r.kdeg_mRNA_FtsH = 0.5
    r.kdeg_mRNA_Protein = 0.5

    # kc_Pfold_Punfold := piecewise(75, time < 0, 150)
    # kp_mRNA_s32 := piecewise(20, time < 0, 80)

    # This is the steady state of HSR_MATLAB just before heat shock.
    r.s70 = 6.533850e-10
    r.RNAP = 2.781883e-10
    r.s32 = 5.653328e-11
    r.FtsH = 9.867260e-07
    r.DnaK = 1.011685e-06
    r.Punfold = 2.485938e-05
    r.Pg = 8.597317e-06
    r.Ph = 7.502017e-08
    r.s70_RNAP = 1.817641e-10
    r.Pg_s70_RNAP = 1.562683e-06
    r.RNAP_s32 = 1.572690e-11
    r.Ph_RNAP_s32 = 1.179834e-09
    r.s32_DnaK = 5.719387e-10
    r.s32_FtsH = 5.578285e-09
    r.Punfold_DnaK = 2.514986e-05
    r.D_s70_RNAP = 2.144816e-07
    r.D_RNAP_s32 = 1.855774e-08
    r.RNAP_D = 3.282622e-06
    r.s32_DnaK_FtsH = 5.643468e-08
    r.Pfold = 5.029992e-03
    r.mRNA_s32 = 1.562683e-08
    r.mRNA_DnaK = 3.932781e-08
    r.mRNA_FtsH = 1.573113e-09
    r.mRNA_Protein = 7.620000e-06



if __name__ == '__main__':
    main()
