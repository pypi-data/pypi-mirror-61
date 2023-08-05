# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



import os,sys

__this_dir__=os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

if not __this_dir__ in sys.path:
  sys.path.append(__this_dir__)

__bin_dir__=os.path.abspath(__this_dir__+ "/bin")
if not __bin_dir__ in sys.path:
  sys.path.append(__bin_dir__)



from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _VisusGuiNodesPy
else:
    import _VisusGuiNodesPy

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import weakref

class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _VisusGuiNodesPy.delete_SwigPyIterator

    def value(self):
        return _VisusGuiNodesPy.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _VisusGuiNodesPy.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _VisusGuiNodesPy.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _VisusGuiNodesPy.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _VisusGuiNodesPy.SwigPyIterator_equal(self, x)

    def copy(self):
        return _VisusGuiNodesPy.SwigPyIterator_copy(self)

    def next(self):
        return _VisusGuiNodesPy.SwigPyIterator_next(self)

    def __next__(self):
        return _VisusGuiNodesPy.SwigPyIterator___next__(self)

    def previous(self):
        return _VisusGuiNodesPy.SwigPyIterator_previous(self)

    def advance(self, n):
        return _VisusGuiNodesPy.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _VisusGuiNodesPy.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _VisusGuiNodesPy.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _VisusGuiNodesPy.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _VisusGuiNodesPy.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _VisusGuiNodesPy.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _VisusGuiNodesPy.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _VisusGuiNodesPy:
_VisusGuiNodesPy.SwigPyIterator_swigregister(SwigPyIterator)

SHARED_PTR_DISOWN = _VisusGuiNodesPy.SHARED_PTR_DISOWN
import VisusKernelPy
import VisusDataflowPy
import VisusGuiPy
class GuiNodesModule(VisusKernelPy.VisusModule):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    bAttached = property(_VisusGuiNodesPy.GuiNodesModule_bAttached_get, _VisusGuiNodesPy.GuiNodesModule_bAttached_set)

    @staticmethod
    def attach():
        return _VisusGuiNodesPy.GuiNodesModule_attach()

    @staticmethod
    def detach():
        return _VisusGuiNodesPy.GuiNodesModule_detach()

    def __init__(self):
        _VisusGuiNodesPy.GuiNodesModule_swiginit(self, _VisusGuiNodesPy.new_GuiNodesModule())
    __swig_destroy__ = _VisusGuiNodesPy.delete_GuiNodesModule

# Register GuiNodesModule in _VisusGuiNodesPy:
_VisusGuiNodesPy.GuiNodesModule_swigregister(GuiNodesModule)
cvar = _VisusGuiNodesPy.cvar

def GuiNodesModule_attach():
    return _VisusGuiNodesPy.GuiNodesModule_attach()

def GuiNodesModule_detach():
    return _VisusGuiNodesPy.GuiNodesModule_detach()

class GLCameraNode(VisusDataflowPy.Node):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _VisusGuiNodesPy.GLCameraNode_swiginit(self, _VisusGuiNodesPy.new_GLCameraNode(*args))
    __swig_destroy__ = _VisusGuiNodesPy.delete_GLCameraNode

    def getGLCamera(self):
        return _VisusGuiNodesPy.GLCameraNode_getGLCamera(self)

    def setGLCamera(self, glcamera):
        return _VisusGuiNodesPy.GLCameraNode_setGLCamera(self, glcamera)

    def execute(self, ar):
        return _VisusGuiNodesPy.GLCameraNode_execute(self, ar)

    def write(self, ar):
        return _VisusGuiNodesPy.GLCameraNode_write(self, ar)

    def read(self, ar):
        return _VisusGuiNodesPy.GLCameraNode_read(self, ar)

# Register GLCameraNode in _VisusGuiNodesPy:
_VisusGuiNodesPy.GLCameraNode_swigregister(GLCameraNode)

class IsoContour(VisusGuiPy.GLMesh):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    field = property(_VisusGuiNodesPy.IsoContour_field_get, _VisusGuiNodesPy.IsoContour_field_set)
    second_field = property(_VisusGuiNodesPy.IsoContour_second_field_get, _VisusGuiNodesPy.IsoContour_second_field_set)
    range = property(_VisusGuiNodesPy.IsoContour_range_get, _VisusGuiNodesPy.IsoContour_range_set)
    voxel_used = property(_VisusGuiNodesPy.IsoContour_voxel_used_get, _VisusGuiNodesPy.IsoContour_voxel_used_set)

    def __init__(self):
        _VisusGuiNodesPy.IsoContour_swiginit(self, _VisusGuiNodesPy.new_IsoContour())
    __swig_destroy__ = _VisusGuiNodesPy.delete_IsoContour

# Register IsoContour in _VisusGuiNodesPy:
_VisusGuiNodesPy.IsoContour_swigregister(IsoContour)

class MarchingCube(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    data = property(_VisusGuiNodesPy.MarchingCube_data_get, _VisusGuiNodesPy.MarchingCube_data_set)
    isovalue = property(_VisusGuiNodesPy.MarchingCube_isovalue_get, _VisusGuiNodesPy.MarchingCube_isovalue_set)
    enable_vortex_used = property(_VisusGuiNodesPy.MarchingCube_enable_vortex_used_get, _VisusGuiNodesPy.MarchingCube_enable_vortex_used_set)
    vertices_per_batch = property(_VisusGuiNodesPy.MarchingCube_vertices_per_batch_get, _VisusGuiNodesPy.MarchingCube_vertices_per_batch_set)
    aborted = property(_VisusGuiNodesPy.MarchingCube_aborted_get, _VisusGuiNodesPy.MarchingCube_aborted_set)

    def __init__(self, *args):
        _VisusGuiNodesPy.MarchingCube_swiginit(self, _VisusGuiNodesPy.new_MarchingCube(*args))

    def run(self):
        return _VisusGuiNodesPy.MarchingCube_run(self)
    __swig_destroy__ = _VisusGuiNodesPy.delete_MarchingCube

# Register MarchingCube in _VisusGuiNodesPy:
_VisusGuiNodesPy.MarchingCube_swigregister(MarchingCube)

class IsoContourNode(VisusDataflowPy.Node):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _VisusGuiNodesPy.IsoContourNode_swiginit(self, _VisusGuiNodesPy.new_IsoContourNode())
    __swig_destroy__ = _VisusGuiNodesPy.delete_IsoContourNode

    def processInput(self):
        return _VisusGuiNodesPy.IsoContourNode_processInput(self)

    def getLastFieldRange(self):
        return _VisusGuiNodesPy.IsoContourNode_getLastFieldRange(self)

    def setField(self, value):
        return _VisusGuiNodesPy.IsoContourNode_setField(self, value)

    def getIsoValue(self):
        return _VisusGuiNodesPy.IsoContourNode_getIsoValue(self)

    def setIsoValue(self, value):
        return _VisusGuiNodesPy.IsoContourNode_setIsoValue(self, value)

    def execute(self, ar):
        return _VisusGuiNodesPy.IsoContourNode_execute(self, ar)

    def write(self, ar):
        return _VisusGuiNodesPy.IsoContourNode_write(self, ar)

    def read(self, ar):
        return _VisusGuiNodesPy.IsoContourNode_read(self, ar)

# Register IsoContourNode in _VisusGuiNodesPy:
_VisusGuiNodesPy.IsoContourNode_swigregister(IsoContourNode)

class IsoContourRenderNode(VisusDataflowPy.Node, VisusGuiPy.GLObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _VisusGuiNodesPy.IsoContourRenderNode_swiginit(self, _VisusGuiNodesPy.new_IsoContourRenderNode())
    __swig_destroy__ = _VisusGuiNodesPy.delete_IsoContourRenderNode

    def glRender(self, gl):
        return _VisusGuiNodesPy.IsoContourRenderNode_glRender(self, gl)

    def getBounds(self):
        return _VisusGuiNodesPy.IsoContourRenderNode_getBounds(self)

    def getMaterial(self):
        return _VisusGuiNodesPy.IsoContourRenderNode_getMaterial(self)

    def setMaterial(self, new_value):
        return _VisusGuiNodesPy.IsoContourRenderNode_setMaterial(self, new_value)

    def getPalette(self):
        return _VisusGuiNodesPy.IsoContourRenderNode_getPalette(self)

    def setPalette(self, value):
        return _VisusGuiNodesPy.IsoContourRenderNode_setPalette(self, value)

    def getMesh(self):
        return _VisusGuiNodesPy.IsoContourRenderNode_getMesh(self)

    def setMesh(self, value):
        return _VisusGuiNodesPy.IsoContourRenderNode_setMesh(self, value)

    def processInput(self):
        return _VisusGuiNodesPy.IsoContourRenderNode_processInput(self)

    @staticmethod
    def allocShaders():
        return _VisusGuiNodesPy.IsoContourRenderNode_allocShaders()

    @staticmethod
    def releaseShaders():
        return _VisusGuiNodesPy.IsoContourRenderNode_releaseShaders()

    def execute(self, ar):
        return _VisusGuiNodesPy.IsoContourRenderNode_execute(self, ar)

    def write(self, ar):
        return _VisusGuiNodesPy.IsoContourRenderNode_write(self, ar)

    def read(self, ar):
        return _VisusGuiNodesPy.IsoContourRenderNode_read(self, ar)

# Register IsoContourRenderNode in _VisusGuiNodesPy:
_VisusGuiNodesPy.IsoContourRenderNode_swigregister(IsoContourRenderNode)

def IsoContourRenderNode_allocShaders():
    return _VisusGuiNodesPy.IsoContourRenderNode_allocShaders()

def IsoContourRenderNode_releaseShaders():
    return _VisusGuiNodesPy.IsoContourRenderNode_releaseShaders()

class RenderArrayNode(VisusDataflowPy.Node, VisusGuiPy.GLObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    bFastRendering = property(_VisusGuiNodesPy.RenderArrayNode_bFastRendering_get, _VisusGuiNodesPy.RenderArrayNode_bFastRendering_set)
    opacity = property(_VisusGuiNodesPy.RenderArrayNode_opacity_get, _VisusGuiNodesPy.RenderArrayNode_opacity_set)

    def __init__(self):
        _VisusGuiNodesPy.RenderArrayNode_swiginit(self, _VisusGuiNodesPy.new_RenderArrayNode())
    __swig_destroy__ = _VisusGuiNodesPy.delete_RenderArrayNode

    def getData(self):
        return _VisusGuiNodesPy.RenderArrayNode_getData(self)

    def setData(self, *args):
        return _VisusGuiNodesPy.RenderArrayNode_setData(self, *args)

    def getDataDimension(self):
        return _VisusGuiNodesPy.RenderArrayNode_getDataDimension(self)

    def getDataBounds(self):
        return _VisusGuiNodesPy.RenderArrayNode_getDataBounds(self)

    def getBounds(self):
        return _VisusGuiNodesPy.RenderArrayNode_getBounds(self)

    def getLightingMaterial(self):
        return _VisusGuiNodesPy.RenderArrayNode_getLightingMaterial(self)

    def setLightingMaterial(self, value):
        return _VisusGuiNodesPy.RenderArrayNode_setLightingMaterial(self, value)

    def lightingEnabled(self):
        return _VisusGuiNodesPy.RenderArrayNode_lightingEnabled(self)

    def setLightingEnabled(self, value):
        return _VisusGuiNodesPy.RenderArrayNode_setLightingEnabled(self, value)

    def getPalette(self):
        return _VisusGuiNodesPy.RenderArrayNode_getPalette(self)

    def paletteEnabled(self):
        return _VisusGuiNodesPy.RenderArrayNode_paletteEnabled(self)

    def setPaletteEnabled(self, value):
        return _VisusGuiNodesPy.RenderArrayNode_setPaletteEnabled(self, value)

    def useViewDirection(self):
        return _VisusGuiNodesPy.RenderArrayNode_useViewDirection(self)

    def setUseViewDirection(self, value):
        return _VisusGuiNodesPy.RenderArrayNode_setUseViewDirection(self, value)

    def maxNumSlices(self):
        return _VisusGuiNodesPy.RenderArrayNode_maxNumSlices(self)

    def setMaxNumSlices(self, value):
        return _VisusGuiNodesPy.RenderArrayNode_setMaxNumSlices(self, value)

    def minifyFilter(self):
        return _VisusGuiNodesPy.RenderArrayNode_minifyFilter(self)

    def setMinifyFilter(self, value):
        return _VisusGuiNodesPy.RenderArrayNode_setMinifyFilter(self, value)

    def magnifyFilter(self):
        return _VisusGuiNodesPy.RenderArrayNode_magnifyFilter(self)

    def setMagnifyFilter(self, value):
        return _VisusGuiNodesPy.RenderArrayNode_setMagnifyFilter(self, value)

    def glRender(self, gl):
        return _VisusGuiNodesPy.RenderArrayNode_glRender(self, gl)

    def processInput(self):
        return _VisusGuiNodesPy.RenderArrayNode_processInput(self)

    @staticmethod
    def allocShaders():
        return _VisusGuiNodesPy.RenderArrayNode_allocShaders()

    @staticmethod
    def releaseShaders():
        return _VisusGuiNodesPy.RenderArrayNode_releaseShaders()

    def execute(self, ar):
        return _VisusGuiNodesPy.RenderArrayNode_execute(self, ar)

    def write(self, ar):
        return _VisusGuiNodesPy.RenderArrayNode_write(self, ar)

    def read(self, ar):
        return _VisusGuiNodesPy.RenderArrayNode_read(self, ar)

# Register RenderArrayNode in _VisusGuiNodesPy:
_VisusGuiNodesPy.RenderArrayNode_swigregister(RenderArrayNode)

def RenderArrayNode_allocShaders():
    return _VisusGuiNodesPy.RenderArrayNode_allocShaders()

def RenderArrayNode_releaseShaders():
    return _VisusGuiNodesPy.RenderArrayNode_releaseShaders()

class KdRenderArrayNode(VisusDataflowPy.Node, VisusGuiPy.GLObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _VisusGuiNodesPy.KdRenderArrayNode_swiginit(self, _VisusGuiNodesPy.new_KdRenderArrayNode())
    __swig_destroy__ = _VisusGuiNodesPy.delete_KdRenderArrayNode

    def getKdArray(self):
        return _VisusGuiNodesPy.KdRenderArrayNode_getKdArray(self)

    def getBounds(self):
        return _VisusGuiNodesPy.KdRenderArrayNode_getBounds(self)

    def processInput(self):
        return _VisusGuiNodesPy.KdRenderArrayNode_processInput(self)

    def glRender(self, gl):
        return _VisusGuiNodesPy.KdRenderArrayNode_glRender(self, gl)

    @staticmethod
    def allocShaders():
        return _VisusGuiNodesPy.KdRenderArrayNode_allocShaders()

    @staticmethod
    def releaseShaders():
        return _VisusGuiNodesPy.KdRenderArrayNode_releaseShaders()

# Register KdRenderArrayNode in _VisusGuiNodesPy:
_VisusGuiNodesPy.KdRenderArrayNode_swigregister(KdRenderArrayNode)

def KdRenderArrayNode_allocShaders():
    return _VisusGuiNodesPy.KdRenderArrayNode_allocShaders()

def KdRenderArrayNode_releaseShaders():
    return _VisusGuiNodesPy.KdRenderArrayNode_releaseShaders()

class PythonNode(VisusDataflowPy.Node):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    node_bounds = property(_VisusGuiNodesPy.PythonNode_node_bounds_get, _VisusGuiNodesPy.PythonNode_node_bounds_set)

    def __init__(self):
        if self.__class__ == PythonNode:
            _self = None
        else:
            _self = self
        _VisusGuiNodesPy.PythonNode_swiginit(self, _VisusGuiNodesPy.new_PythonNode(_self, ))
    __swig_destroy__ = _VisusGuiNodesPy.delete_PythonNode

    def getOsDependentTypeName(self):
        return _VisusGuiNodesPy.PythonNode_getOsDependentTypeName(self)

    def processInput(self):
        return _VisusGuiNodesPy.PythonNode_processInput(self)

    def getBounds(self):
        return _VisusGuiNodesPy.PythonNode_getBounds(self)

    def setBounds(self, value):
        return _VisusGuiNodesPy.PythonNode_setBounds(self, value)

    def glGetRenderQueue(self):
        return _VisusGuiNodesPy.PythonNode_glGetRenderQueue(self)

    def glSetRenderQueue(self, value):
        return _VisusGuiNodesPy.PythonNode_glSetRenderQueue(self, value)

    def glMousePressEvent(self, map, evt):
        return _VisusGuiNodesPy.PythonNode_glMousePressEvent(self, map, evt)

    def glMouseMoveEvent(self, map, evt):
        return _VisusGuiNodesPy.PythonNode_glMouseMoveEvent(self, map, evt)

    def glMouseReleaseEvent(self, map, evt):
        return _VisusGuiNodesPy.PythonNode_glMouseReleaseEvent(self, map, evt)

    def glWheelEvent(self, map, evt):
        return _VisusGuiNodesPy.PythonNode_glWheelEvent(self, map, evt)

    def glRender(self, gl):
        return _VisusGuiNodesPy.PythonNode_glRender(self, gl)
    def __disown__(self):
        self.this.disown()
        _VisusGuiNodesPy.disown_PythonNode(self)
        return weakref.proxy(self)

# Register PythonNode in _VisusGuiNodesPy:
_VisusGuiNodesPy.PythonNode_swigregister(PythonNode)



