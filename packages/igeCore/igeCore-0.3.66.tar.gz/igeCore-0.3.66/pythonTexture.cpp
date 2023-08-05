#include "pyxie.h"
#include "pythonResource.h"
#include "pyxieResourceCreator.h"
#include "pyxieResourceManager.h"
#include "Backyard.h"
#include "pyVectorMath.h"
#include "pythonTexture_doc_en.h"
#include "numpy/ndarrayobject.h"
#include "bitmapHelper.h"

namespace pyxie
{
	PyObject *texture_new(PyTypeObject *type, PyObject *args, PyObject *kw) {

		static char* kwlist[] = { "name","width","height","format","depth","stencil","pixel", NULL };

		char* name;
		int width = 0;
		int height = 0;
		int format = GL_RGBA;
		int depth = 0;
		int stencil =0;
		PyObject* pixel = nullptr;

		if (!PyArg_ParseTupleAndKeywords(args, kw, "s|iiippO", kwlist,
			&name, &width, &height, &format, &depth, &stencil, &pixel)) return NULL;

		if (!(format == GL_RED || format == GL_RGB || format == GL_RGBA)) {
			PyErr_SetString(PyExc_TypeError, "format value is invalid.");
			return NULL;
		}

		texture_obj* self = NULL;

		char* pix = nullptr;
		if (pixel) {
			if (pixel->ob_type->tp_name && strcmp(pixel->ob_type->tp_name, "numpy.ndarray") == 0) {
				PyArrayObject_fields* ndarray = (PyArrayObject_fields*)pixel;
				height = *ndarray->dimensions;
				width = *ndarray->strides / ndarray->nd;
				switch (ndarray->nd) {
				case 1: format = GL_RED; break;
//				case 2: format = GL_RED; break;
				case 3: format = GL_RGB; break;
				case 4: format = GL_RGBA; break;
				}
				pix = ndarray->data;
			}
			else if (PyBytes_Check(pixel)) {
				pix = PyBytes_AsString(pixel);
			}
		}

		self = (texture_obj*)type->tp_alloc(type, 0);

		if (width == 0 || height == 0)
			self->colortexture = pyxieResourceCreator::Instance().NewTexture(name);
		else
			self->colortexture = pyxieResourceCreator::Instance().NewTexture(name, pix, width, height, format);

		self->depth = depth;
		self->stencil = stencil;
		self->renderTarget = nullptr;

		return (PyObject *)self;
	}

	void  texture_dealloc(texture_obj*self)
	{
		self->colortexture->DecReference();
		if(self->renderTarget) self->renderTarget->DecReference();
		Py_TYPE(self)->tp_free(self);
	}

	PyObject * texture_str(texture_obj *self)
	{
		char buf[64];
		pyxie_snprintf(buf, 64, "texture object");
		return _PyUnicode_FromASCII(buf, strlen(buf));
	}

	static PyObject* texture_setImage(texture_obj* self, PyObject* args, PyObject* kwargs){
		static char* kwlist[] = { "image","x","y","width","height", NULL };

		self->subImage = NULL;
		self->x = 0;
		self->y = 0;
		self->w = -1;
		self->h = -1;
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|iiii", kwlist,
			&(self->subImage), &(self->x), &(self->y), &(self->w), &(self->h))) return NULL;

		Backyard::Instance().UpdateImageRequest(self);

		Py_INCREF(Py_None);
		return Py_None;
	}


	static PyObject* texture_setCheckeredImage(texture_obj* self, PyObject* args, PyObject* kwargs)
	{
		static char* kwlist[] = { "r","g","b","a", NULL };
		float r = 1.0f;
		float g = 0;
		float b = 0;
		float a = 1.0f;
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|ffff", kwlist, &r, &g, &b, &a)) return NULL;

		int w = self->colortexture->GetTextureWidth();
		int h = self->colortexture->GetTextureHeight();

		int format = self->colortexture->GetFormat();
		PyObject* obj = createCheckeredTexture((uint8_t)(r * 255.0f), (uint8_t)(g * 255.0f), (uint8_t)(b * 255.0f), (uint8_t)(a * 255.0f), w, h, format);

		self->subImage = obj;
		self->x = 0;
		self->y = 0;
		self->w = -1;
		self->h = -1;
		Backyard::Instance().UpdateImageRequest(self);

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* texture_setText(texture_obj* self, PyObject* args, PyObject* kwargs)
	{
		if (self->colortexture->GetFormat() != GL_RED) {
			PyErr_SetString(PyExc_TypeError, "The setText method is currently only for GL_RED textures.");
			return NULL;
		}

		static char* kwlist[] = { "word","font","size","startX","startY", NULL };
		char* word;
		char* font;
		int size;
		int startX;
		int startY;
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ssi|ii", kwlist, &word, &font, &size, &startX, &startY)) return NULL;

		int w = self->colortexture->GetTextureWidth();
		int h = self->colortexture->GetTextureHeight();
		int format = self->colortexture->GetFormat();

		PyObject* obj = createTextImage(word, font, size, w,h);

		self->subImage = obj;
		self->x = 0;
		self->y = 0;
		self->w = -1;
		self->h = -1;
		Backyard::Instance().UpdateImageRequest(self);

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* texture_clear(texture_obj* self, PyObject* args, PyObject* kwargs)
	{
		static char* kwlist[] = { "r","g","b","a", NULL };
		float r = 0;
		float g = 0;
		float b = 0;
		float a = 0;
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|ffff", kwlist, &r, &g, &b, &a)) return NULL;

		int w = self->colortexture->GetTextureWidth();
		int h = self->colortexture->GetTextureHeight();

		int format = self->colortexture->GetFormat();
		PyObject* obj = createColorTexture((uint8_t)(r*255.0f), (uint8_t)(g * 255.0f), (uint8_t)(b * 255.0f), (uint8_t)(a * 255.0f), w, h, format);

		self->subImage = obj;
		self->x = 0;
		self->y = 0;
		self->w = -1;
		self->h = -1;
		Backyard::Instance().UpdateImageRequest(self);

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* texture_captureScreenshot(texture_obj* self, PyObject* args, PyObject* kwargs)
	{
		const char* name;
		if (!PyArg_ParseTuple(args, "s", &name)) return NULL;

		Backyard::Instance().UpdateCaptureRequest(name);
		
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyMethodDef texture_methods[] = {
		{ "setImage", (PyCFunction)texture_setImage, METH_VARARGS | METH_KEYWORDS,setImage_doc },
		{ "setCheckeredImage", (PyCFunction)texture_setCheckeredImage, METH_VARARGS | METH_KEYWORDS,setCheckeredImage_doc },
		{ "setText", (PyCFunction)texture_setText, METH_VARARGS | METH_KEYWORDS,setText_doc },
		{ "clear", (PyCFunction)texture_clear, METH_VARARGS | METH_KEYWORDS,clear_doc },
		{ "captureScreenshot", (PyCFunction)texture_captureScreenshot, METH_VARARGS | METH_KEYWORDS,captureScreenshot_doc },
		{ NULL,	NULL }
	};

	PyGetSetDef texture_getsets[] = {
		{ NULL, NULL }
	};

	PyTypeObject TextureType = {
		PyVarObject_HEAD_INIT(NULL, 0)
		"igeCore.texture",					/* tp_name */
		sizeof(texture_obj),                /* tp_basicsize */
		0,                                  /* tp_itemsize */
		(destructor)texture_dealloc,		/* tp_dealloc */
		0,                                  /* tp_print */
		0,							        /* tp_getattr */
		0,                                  /* tp_setattr */
		0,                                  /* tp_reserved */
		0,                                  /* tp_repr */
		0,					                /* tp_as_number */
		0,                                  /* tp_as_sequence */
		0,                                  /* tp_as_mapping */
		0,                                  /* tp_hash */
		0,                                  /* tp_call */
		(reprfunc)texture_str,               /* tp_str */
		0,                                  /* tp_getattro */
		0,                                  /* tp_setattro */
		0,                                  /* tp_as_buffer */
		Py_TPFLAGS_DEFAULT,					/* tp_flags */
		texture_doc,						/* tp_doc */
		0,									/* tp_traverse */
		0,                                  /* tp_clear */
		0,                                  /* tp_richcompare */
		0,                                  /* tp_weaklistoffset */
		0,									/* tp_iter */
		0,									/* tp_iternext */
		texture_methods,						/* tp_methods */
		0,                                  /* tp_members */
		texture_getsets,                     /* tp_getset */
		0,                                  /* tp_base */
		0,                                  /* tp_dict */
		0,                                  /* tp_descr_get */
		0,                                  /* tp_descr_set */
		0,                                  /* tp_dictoffset */
		0,                                  /* tp_init */
		0,                                  /* tp_alloc */
		texture_new,							/* tp_new */
		0,									/* tp_free */
	};

}