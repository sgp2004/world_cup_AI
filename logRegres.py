'''
Created on Oct 27, 2010
Logistic Regression Working Module
@author: Peter
'''
from numpy import *


def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def stocGradAscent1(dataMatrix, classLabels, numIter=500):
    m,n = shape(dataMatrix)
    weights = ones(n)   #initialize to all ones
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001    #apha decreases with iteration, does not
            randIndex = int(random.uniform(0,len(dataIndex)))#go to 0 because of the constant
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    return prob
    #if prob > 0.5: return 1.0
    #else: return 0.0

def colicTest(k,cmax):
    frTrain = open('world_cup_train.txt'); frTest = open('world_cup_test.txt')
    frPretell = open('world_cup_pretell.txt')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(12):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[12]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 1000)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(12):
            lineArr.append(float(currLine[i]))
        prob = classifyVector(array(lineArr), trainWeights)
        real_prob = float(currLine[12])
        date = (currLine[len(currLine)-1])
        rate = 0.3
        if (prob>real_prob and prob-real_prob<rate) or (prob<=real_prob and real_prob-prob<rate):
            pass
        else:
            print("prob error, %f ,%f, %s" %(prob,real_prob,date))
            errorCount += 1

    errorRate = (float(errorCount)/numTestVec)
    print("the error rate of this test is: %f" % errorRate)
    print("%d, %d" %(k,cmax-1))
    if(k == cmax-1):
        for line in frPretell.readlines():
            numTestVec += 1.0
            currLine = line.strip().split('\t')
            lineArr =[]
            for i in range(12):
                lineArr.append(float(currLine[i]))
            prob = classifyVector(array(lineArr), trainWeights)
            date = (currLine[len(currLine)-1])
            print("%s, %f" %(date,prob))
    return errorRate

def multiTest():
    numTests = 30; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTest(k,numTests)
    print("after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests)))

if __name__ == '__main__':
    multiTest()

