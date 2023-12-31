import subprocess
import time

import numpy as np

from MiddleWare.NeuralNet import  mse_prime
import numpy as np

def convert_matrix(m):
    max_field=21888242871839275222246405745257275088548364400416034343698204186575808495617
    m = np.array(m)
    return np.where(m<0,max_field+m,m),np.where(m>0,0,1)

def args_parser(args):
    res=""
    for arg in range(len(args)):
        entry=args[arg]
        if isinstance(entry, (list, np.ndarray)):
            for i in range(len(entry)):
                row_i=entry[i]
                if isinstance(row_i, (list, np.ndarray)):
                    for j in range(len(row_i)):
                        val = row_i[j]
                        res += str(val) + " "
                else:
                    res += str(row_i) + " "
        else:
            res += str(args[arg]) + " "
    res=res[:-1]
    return res

def proof_generation(Y):
    zokrates= 'zokrates'
    batchsize=10
    np.random.seed(0)
    precision=10000
    ac=6
    fe=9
    bias = np.random.randn(ac, ) *precision
    weights = np.random.randn(ac, fe)*precision
    weights = np.array([[int(x) for x in y] for y in weights])
    bias = np.array([int(x) for x in bias])
    w=weights
    weights,weights_sign=convert_matrix(weights)
    b=bias
    bias,bias_sign=convert_matrix(bias)
    x_train=np.random.randn(batchsize, fe)*precision
    x_train = np.array([[int(x) for x in y] for y in x_train])
    x=x_train
    x_train,x_train_sign=convert_matrix(x_train)
    learning_rate=10
    Y_test=[]

    for y in Y:
        Y_test.append(int(y))

    out=None
    Y = []
    for X in x:
        #rand_int=np.random.random_integers(1,ac)
        rand_int = np.random.randint(1, ac)
        y_true = np.zeros(shape=(ac,))
        y_true[rand_int - 1] = precision
        Y.append(rand_int)
        out_layer = (np.dot(w, X) / precision).astype(int)
        out_layer = np.add(out_layer, b)
        error = mse_prime(y_true, out_layer).astype(int)
        w = w - (np.outer(error, X) / precision / learning_rate).astype(int)
        b = b - (error / learning_rate).astype(int)
    #,bias,bias_sign,x,x_sign,1,learning_rate,precision
    out=out_layer
    converted_W = convert_matrix(w)[0]
    converted_B = convert_matrix(b)[0]
    args=[weights,weights_sign,bias,bias_sign,x_train,x_train_sign,Y_test,learning_rate,precision,converted_W,converted_B]

    verification_base = "/home/iman/projects/kara/blockchain_based_Federated_learning/federatedlearning/codes/Devices/Verification/SAVED_VERIFYER_10/"
    out_path=verification_base+"out"
    abi_path=verification_base+"abi.json"
    witness_path=verification_base+"witness_Device_1"

    ##################################################
    #zokrates_compute_witness=[zokrates,"compute-witness","-a"]
    zokrates_compute_witness = [zokrates, "compute-witness", "-o",witness_path,'-i',out_path,'-s',abi_path,"-a"]

    zokrates_compute_witness.extend(args_parser(args).split(" "))



    t1=time.time()
    g= subprocess.run(zokrates_compute_witness, capture_output=True)
    t2=time.time()
    print(f"Computing witness for {batchsize} samples took {t2-t1} seconds")


    zokrates_generate_proof=[zokrates,"generate-proof"]
    t1=time.time()
    g= subprocess.run(zokrates_generate_proof, capture_output=True)
    t2=time.time()
    print(f"Generating proof for {batchsize} samples took {t2-t1} seconds")

    zokrates_export_verifier=[zokrates,"export-verifier"]
    t1=time.time()
    g= subprocess.run(zokrates_export_verifier, capture_output=True)
    t2=time.time()
    print(f"Exporting Verifier for {batchsize} samples took {t2-t1} seconds")
    conv = convert_matrix(out)
    print(conv)