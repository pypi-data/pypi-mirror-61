#include "pyxie.h"
#include "Window.h"
#include <python.h>
#include <thread>
#include <mutex>

#include "pyxieApplication.h"
#include "pyxieFios.h"
#include "pyxieTouchManager.h"
#include "pyxieResourceManager.h"
#include "pyxieRenderContext.h"
#include "pyxieShader.h"
#include "pyxieSystemInfo.h"
#include "Backyard.h"

std::shared_ptr<pyxie::pyxieApplication> gApp;

class TestApp : public pyxie::pyxieApplication
{
public:
	TestApp() {
		
		pyxie::pyxieFios::Instance().SetRoot();
	}
	~TestApp() {}

	bool onInit(DeviceHandle dh) {
		if (pyxieApplication::onInit(dh) == false) {
			return false;
		}			
		pyxie::Backyard::New();
		return true;
	}

	void onShutdown() {
		pyxie::Backyard::Delete();
		pyxieApplication::onShutdown();
	}

	bool onUpdate(){
		return pyxieApplication::onUpdate();
	}

	void onRender(){
		pyxie::Backyard::Instance().Render();
	}
};

PyMODINIT_FUNC _PyInit__igeCore();

PyMODINIT_FUNC PyInit__igeCore() {
	gApp = std::make_shared<TestApp>();
	gApp->createAppWindow();
	
	return _PyInit__igeCore();
}

