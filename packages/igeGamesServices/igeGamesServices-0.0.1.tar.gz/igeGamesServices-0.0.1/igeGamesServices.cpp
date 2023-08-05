#include "igeGamesServices.h"
#include "igeGamesServices_doc_en.h"

PyObject* gamesServices_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	gamesServices_obj* self = NULL;

	self = (gamesServices_obj*)type->tp_alloc(type, 0);
	self->gamesServices = new GamesServices();

	return (PyObject*)self;
}

void gamesServices_dealloc(gamesServices_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* gamesServices_str(gamesServices_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "Social GamesServices object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* gamesServices_Init(gamesServices_obj* self)
{
	self->gamesServices->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesServices_Release(gamesServices_obj* self)
{
	self->gamesServices->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesServices_SignIn(gamesServices_obj* self)
{
	self->gamesServices->signIn();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesServices_SignOut(gamesServices_obj* self)
{
	self->gamesServices->signOut();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesServices_IsSignedIn(gamesServices_obj* self)
{
	return PyLong_FromLong(self->gamesServices->isSignedIn());
}

static PyObject* gamesServices_ShowLeaderboard(gamesServices_obj* self, PyObject* args)
{
	const char* leaderboardId = "";
	if (!PyArg_ParseTuple(args, "|s", &leaderboardId))
		return NULL;
	self->gamesServices->showLeaderboard(leaderboardId);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesServices_SubmitScoreLeaderboard(gamesServices_obj* self, PyObject* args)
{
	const char* leaderboardId = "";
	int value = 0;
	if (!PyArg_ParseTuple(args, "si", &leaderboardId, &value))
		return NULL;
	self->gamesServices->submitScoreLeaderboard(leaderboardId, value);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesServices_ShowAchievement(gamesServices_obj* self)
{
	self->gamesServices->showAchievement();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesServices_UnlockAchievement(gamesServices_obj* self, PyObject* args)
{
	const char* achievementId = "";
	if (!PyArg_ParseTuple(args, "s", &achievementId))
		return NULL;
	self->gamesServices->unlockAchievement(achievementId);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesServices_IncrementAchievement(gamesServices_obj* self, PyObject* args)
{
	const char* achievementId = "";
	int value = 0;
	if (!PyArg_ParseTuple(args, "si", &achievementId, &value))
		return NULL;
	self->gamesServices->incrementAchievement(achievementId, value);

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef gamesServices_methods[] = {
	{ "init", (PyCFunction)gamesServices_Init, METH_NOARGS, socialGamesServicesInit_doc },
	{ "release", (PyCFunction)gamesServices_Release, METH_NOARGS, socialGamesServicesRelease_doc },
	{ "signIn", (PyCFunction)gamesServices_SignIn, METH_NOARGS, socialGamesServicesSignIn_doc },
	{ "signOut", (PyCFunction)gamesServices_SignOut, METH_NOARGS, socialGamesServicesSignOut_doc },
	{ "isSignedIn", (PyCFunction)gamesServices_IsSignedIn, METH_NOARGS, socialGamesServicesIsSignedIn_doc },
	{ "showLeaderboard", (PyCFunction)gamesServices_ShowLeaderboard, METH_VARARGS, socialGamesServicesShowLeaderboard_doc },
	{ "submitScoreLeaderboard", (PyCFunction)gamesServices_SubmitScoreLeaderboard, METH_VARARGS, socialGamesServicesSubmitScoreLeaderboard_doc },
	{ "showAchievement", (PyCFunction)gamesServices_ShowAchievement, METH_NOARGS, socialGamesServicesShowAchievement_doc },
	{ "unlockAchievement", (PyCFunction)gamesServices_UnlockAchievement, METH_VARARGS, socialGamesServicesUnlockAchievement_doc },
	{ "incrementAchievement", (PyCFunction)gamesServices_IncrementAchievement, METH_VARARGS, socialGamesServicesIncrementAchievement_doc },
	{ NULL,	NULL }
};

PyGetSetDef gamesServices_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject GamesServicesType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeGamesServices",								/* tp_name */
	sizeof(gamesServices_obj),						/* tp_basicsize */
	0,												/* tp_itemsize */
	(destructor)gamesServices_dealloc,				/* tp_dealloc */
	0,												/* tp_print */
	0,												/* tp_getattr */
	0,												/* tp_setattr */
	0,												/* tp_reserved */
	0,												/* tp_repr */
	0,												/* tp_as_number */
	0,												/* tp_as_sequence */
	0,												/* tp_as_mapping */
	0,												/* tp_hash */
	0,												/* tp_call */
	(reprfunc)gamesServices_str,					/* tp_str */
	0,												/* tp_getattro */
	0,												/* tp_setattro */
	0,												/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,								/* tp_flags */
	0,												/* tp_doc */
	0,												/* tp_traverse */
	0,												/* tp_clear */
	0,												/* tp_richcompare */
	0,												/* tp_weaklistoffset */
	0,												/* tp_iter */
	0,												/* tp_iternext */
	gamesServices_methods,							/* tp_methods */
	0,												/* tp_members */
	gamesServices_getsets,							/* tp_getset */
	0,												/* tp_base */
	0,												/* tp_dict */
	0,												/* tp_descr_get */
	0,												/* tp_descr_set */
	0,												/* tp_dictoffset */
	0,												/* tp_init */
	0,												/* tp_alloc */
	gamesServices_new,								/* tp_new */
	0,												/* tp_free */
};

static PyModuleDef gamesServices_module = {
	PyModuleDef_HEAD_INIT,
	"igeGamesServices",							// Module name to use with Python import statements
	"GamesServices Module.",					// Module description
	0,
	gamesServices_methods						// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeGamesServices() {
	PyObject* module = PyModule_Create(&gamesServices_module);

	if (PyType_Ready(&GamesServicesType) < 0) return NULL;

	Py_INCREF(&GamesServicesType);
	PyModule_AddObject(module, "GamesServices", (PyObject*)&GamesServicesType);

	return module;
}
