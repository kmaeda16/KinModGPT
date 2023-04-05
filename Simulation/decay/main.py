import tellurium as te
import pandas as pd
from matplotlib import pyplot as plt
import roadrunner as rr



# Use the following two lines if plots do not show up.
import matplotlib
matplotlib.use('TkAgg')



def main():
    model_name = 'decay'
    sbml_model = readSBMLModel("../../Conversion/4. KinModGPT_text-davinci-003/Results/{}/{}_SBML_model.xml".format(model_name,model_name))
    r = rr.RoadRunner(sbml_model)
    
    print('======= Parameters =======')
    for name, val in zip(r.getGlobalParameterIds(),r.getGlobalParameterValues()):
        print('{}\t=\t{:e}'.format(name,val))
    print('==========================')
        
    df_result = simulation(r,tstart=0,tend=5,npoints=101)

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



if __name__ == '__main__':
    main()
