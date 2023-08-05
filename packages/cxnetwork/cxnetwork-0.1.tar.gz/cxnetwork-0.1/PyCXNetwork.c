#include <stdio.h>
#include "PyCXNetwork.h"
#include <CVNetwork.h>
// #include <numpy/arrayobject.h>


// CVNetwork* PyCXNewNetwork(PyObject* edgesList, CVBool directed){

// 	PyObject *edgesList;
// 	CVInteger edgesCount = PyObject_Length(edgesList);

// 	if (edgesCount <= 0){
// 		PyErr_SetString(PyExc_TypeError, "edges list is empty.");
// 		return NULL;
// 	}
// 	CVSize nodesCount = 0;
// 	CVIndex * fromIndices = calloc(edgesCount,sizeof(CVIndex));
// 	CVIndex * toIndices = calloc(edgesCount,sizeof(CVIndex));

// 	PyObject* iterator = PyObject_GetIter(edgesList);
// 	PyObject* item;

// 	if (iterator == NULL) {
// 		PyErr_SetString(PyExc_TypeError, "Edges list should be a iterable collection of 2-tuples.");
// 		return NULL;
// 	}

// 	while ((item = PyIter_Next(iterator))) {
// 		if(Tup)
// 		Py_DECREF(item);
// 	}

// 	Py_DECREF(iterator);

// 	if (PyErr_Occurred()){
// 			PyErr_SetString(PyExc_TypeError, "an error occurred.");
// 			return NULL;
// 	}else {
// 			/* continue doing useful work */
// 	}


// 	CVNetwork* network = CVNewNetwork(count,CVFalse,directed);
// 	CVNetworkAddNewEdges(network,fromIndices,toIndices,NULL,0);

// 	free(fromIndices);
// 	free(toIndices);
// 	return network;
// }

PyObject * PyCXNewEdgesListFromNetwork(CVNetwork* network){
	PyObject * list = PyList_New(network->edgesCount);
	for (CVIndex edgeIndex = 0; edgeIndex < network->edgesCount; edgeIndex++){
		unsigned int fromIndex = (unsigned int)network->edgeFromList[edgeIndex];
		unsigned int toIndex = (unsigned int)network->edgeToList[edgeIndex];
		PyObject* fromToTuple = Py_BuildValue("(II)",fromIndex,toIndex);
		PyList_SetItem(list,edgeIndex,fromToTuple);
	}
	return list;
}



CVNetwork* PyCXNewNetwork(PyObject* edgesList,CVSize verticesCount, CVBool directed){
	PyObject* edgesSequence = PySequence_Fast(edgesList, "argument must be iterable");
	if (!edgesSequence){
		return NULL;
	}

	CVSize edgesCount = (CVSize)PySequence_Fast_GET_SIZE(edgesSequence);

	if (edgesCount <= 0){
		PyErr_SetString(PyExc_TypeError, "edges list is empty");
		return NULL;
	}

	CVIndex* fromIndices = calloc(edgesCount,sizeof(CVIndex));
	CVIndex* toIndices = calloc(edgesCount,sizeof(CVIndex));
	
	if (!fromIndices||!toIndices){
		free(fromIndices);
		free(toIndices);
		Py_XDECREF(edgesSequence);
		PyErr_SetString(PyExc_MemoryError, "out of memory");
		return NULL;
	}

	for (CVIndex edgeIndex = 0; edgeIndex < edgesCount; edgeIndex++){
		PyObject* edgeItem = PySequence_Fast_GET_ITEM(edgesSequence, edgeIndex);
		unsigned int fromIndex;
		unsigned int toIndex;

		if (
				!edgeItem || 
				!PyArg_ParseTuple(edgeItem,"II",&fromIndex,&toIndex) ||
				fromIndex>=verticesCount ||
				toIndex>=verticesCount
			){
			free(fromIndices);
			free(toIndices);
			Py_XDECREF(edgesSequence);
			PyErr_SetString(PyExc_TypeError, "a problem happened while converting edges list");
			return NULL;
		}
		fromIndices[edgeIndex] = (CVIndex)fromIndex;
		toIndices[edgeIndex] = (CVIndex)toIndex;
	}

	Py_XDECREF(edgesSequence);

	CVNetwork* network = CVNewNetwork(verticesCount,CVFalse,directed);

	if(!CVNetworkAddNewEdges(network,fromIndices,toIndices,NULL,edgesCount)){
		CVNetworkDestroy(network);
		free(fromIndices);
		free(toIndices);
		return NULL;
	}

	free(fromIndices);
	free(toIndices);
	return network;
}


PyObject *PyCXNetworkRewire(PyObject* self, PyObject* args){
	PyObject* pyObject;
	Py_ssize_t verticesCount;
	float rewireProbability;
	if (!PyArg_ParseTuple(args, "Onf", &pyObject, &verticesCount, &rewireProbability)){
		PyErr_SetString(PyExc_AttributeError, "three parameters should be provided");
		return NULL;
	}

	CVNetwork* network = PyCXNewNetwork(pyObject,verticesCount,CVFalse);
	if(!network){
		PyErr_SetString(PyExc_AttributeError, "a problem happened while converting network");
		return NULL;
	}

	CVNetwork* rewiredNetwork = CVNewNetworkFromRandomRewiring(network,rewireProbability);
	if(!rewiredNetwork){
		PyErr_SetString(PyExc_AttributeError, "a problem happened while converting network");
		return NULL;
	}

	// FILE* networkFile = fopen("oioi.xnet","w");
	// CVNetworkWriteToFile(rewiredNetwork,networkFile);
	// fclose(networkFile);

	PyObject* newEdgesList = PyCXNewEdgesListFromNetwork(rewiredNetwork);
	
	CVNetworkDestroy(network);
	CVNetworkDestroy(rewiredNetwork);
	return newEdgesList;
}



PyObject *PyCXRandomSeed(PyObject* self, PyObject* args){
	unsigned int randomSeed;
	if (!PyArg_ParseTuple(args, "I", &randomSeed)){
		PyErr_SetString(PyExc_AttributeError, "one integer parameter need to be provided");
	}
	CVRandomSeed(randomSeed);
	Py_RETURN_NONE;
}

PyObject *PyCXRandomSeedDev(PyObject* self, PyObject* args){
	CVRandomSeedDev();
	Py_RETURN_NONE;
}