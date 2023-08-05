#include "PyCXNetwork.h"

char rewirefunc_docs[] = "Rewire network.";
char randomSeedfunc_docs[] = "Rewire network.";
char randomSeedDevfunc_docs[] = "Rewire network.";

PyMethodDef cxnetwork_funcs[] = {
	{
		"rewire",
		(PyCFunction)PyCXNetworkRewire,
		METH_VARARGS,
		rewirefunc_docs
	},
	{
		"setRandomSeed",
		(PyCFunction)PyCXRandomSeed,
		METH_VARARGS,
		randomSeedfunc_docs
	},
	{
		"randomSeedDev",
		(PyCFunction)PyCXRandomSeedDev,
		METH_VARARGS,
		randomSeedDevfunc_docs
	},
	{
		NULL
	}
};

char cxnetworkmod_docs[] = "This is CXNetwork module.";

PyModuleDef cxnetwork_mod = {
		PyModuleDef_HEAD_INIT,
		"cxnetwork",
		cxnetworkmod_docs,
		-1,
		cxnetwork_funcs,
		NULL,
		NULL,
		NULL,
		NULL};

PyMODINIT_FUNC PyInit_cxnetwork(void)
{
	return PyModule_Create(&cxnetwork_mod);
}
