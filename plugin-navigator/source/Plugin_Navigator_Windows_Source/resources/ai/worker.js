// Local WebLLM worker for Plugin Navigator.
// The WebLLM runtime is bundled into the Windows executable by build_windows.py.
import { WebWorkerMLCEngineHandler } from './webllm.js';

const handler = new WebWorkerMLCEngineHandler();
self.onmessage = message => handler.onmessage(message);
