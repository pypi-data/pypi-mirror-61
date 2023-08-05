#pragma once
#include "pyxieObject.h"
namespace pyxie {
	class pyxieCamera;
	class pyxieShowcase;
	class pyxieRenderTarget;

	class Backyard : public pyxieObject {
		static Backyard* instance;
	public:
		static void New() { if(!instance) instance = new Backyard; }
		static void Delete();

		static Backyard& Instance();
		~Backyard();
		
		void RenderRequest(pyxieCamera* camera, pyxieShowcase* showcase, pyxieRenderTarget* offscreen, bool clearColor, bool clearDepth, const float* color);
		void Render();
		
		void UpdateImageRequest(void* tex);
		void UpdateCaptureRequest(const char* image);

		void UpdateCapturing();
	};
}
