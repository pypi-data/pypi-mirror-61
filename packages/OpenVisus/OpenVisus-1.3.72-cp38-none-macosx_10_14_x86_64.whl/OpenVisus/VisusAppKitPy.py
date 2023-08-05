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
    from . import _VisusAppKitPy
else:
    import _VisusAppKitPy

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
    __swig_destroy__ = _VisusAppKitPy.delete_SwigPyIterator

    def value(self):
        return _VisusAppKitPy.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _VisusAppKitPy.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _VisusAppKitPy.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _VisusAppKitPy.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _VisusAppKitPy.SwigPyIterator_equal(self, x)

    def copy(self):
        return _VisusAppKitPy.SwigPyIterator_copy(self)

    def next(self):
        return _VisusAppKitPy.SwigPyIterator_next(self)

    def __next__(self):
        return _VisusAppKitPy.SwigPyIterator___next__(self)

    def previous(self):
        return _VisusAppKitPy.SwigPyIterator_previous(self)

    def advance(self, n):
        return _VisusAppKitPy.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _VisusAppKitPy.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _VisusAppKitPy.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _VisusAppKitPy.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _VisusAppKitPy.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _VisusAppKitPy.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _VisusAppKitPy.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _VisusAppKitPy:
_VisusAppKitPy.SwigPyIterator_swigregister(SwigPyIterator)

SHARED_PTR_DISOWN = _VisusAppKitPy.SHARED_PTR_DISOWN
import VisusKernelPy
import VisusDataflowPy
import VisusDbPy
import VisusNodesPy
import VisusGuiPy
import VisusGuiNodesPy
class AppKitModule(VisusKernelPy.VisusModule):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    bAttached = property(_VisusAppKitPy.AppKitModule_bAttached_get, _VisusAppKitPy.AppKitModule_bAttached_set)

    @staticmethod
    def attach():
        return _VisusAppKitPy.AppKitModule_attach()

    @staticmethod
    def detach():
        return _VisusAppKitPy.AppKitModule_detach()

    def __init__(self):
        _VisusAppKitPy.AppKitModule_swiginit(self, _VisusAppKitPy.new_AppKitModule())
    __swig_destroy__ = _VisusAppKitPy.delete_AppKitModule

# Register AppKitModule in _VisusAppKitPy:
_VisusAppKitPy.AppKitModule_swigregister(AppKitModule)
cvar = _VisusAppKitPy.cvar

def AppKitModule_attach():
    return _VisusAppKitPy.AppKitModule_attach()

def AppKitModule_detach():
    return _VisusAppKitPy.AppKitModule_detach()

class ViewerPreferences(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    default_panels = property(_VisusAppKitPy.ViewerPreferences_default_panels_get, _VisusAppKitPy.ViewerPreferences_default_panels_set)
    default_show_logos = property(_VisusAppKitPy.ViewerPreferences_default_show_logos_get, _VisusAppKitPy.ViewerPreferences_default_show_logos_set)
    title = property(_VisusAppKitPy.ViewerPreferences_title_get, _VisusAppKitPy.ViewerPreferences_title_set)
    panels = property(_VisusAppKitPy.ViewerPreferences_panels_get, _VisusAppKitPy.ViewerPreferences_panels_set)
    bHideTitleBar = property(_VisusAppKitPy.ViewerPreferences_bHideTitleBar_get, _VisusAppKitPy.ViewerPreferences_bHideTitleBar_set)
    bHideMenus = property(_VisusAppKitPy.ViewerPreferences_bHideMenus_get, _VisusAppKitPy.ViewerPreferences_bHideMenus_set)
    bRightHanded = property(_VisusAppKitPy.ViewerPreferences_bRightHanded_get, _VisusAppKitPy.ViewerPreferences_bRightHanded_set)
    screen_bounds = property(_VisusAppKitPy.ViewerPreferences_screen_bounds_get, _VisusAppKitPy.ViewerPreferences_screen_bounds_set)
    show_logos = property(_VisusAppKitPy.ViewerPreferences_show_logos_get, _VisusAppKitPy.ViewerPreferences_show_logos_set)

    def __init__(self):
        _VisusAppKitPy.ViewerPreferences_swiginit(self, _VisusAppKitPy.new_ViewerPreferences())

    def write(self, ar):
        return _VisusAppKitPy.ViewerPreferences_write(self, ar)

    def read(self, ar):
        return _VisusAppKitPy.ViewerPreferences_read(self, ar)
    __swig_destroy__ = _VisusAppKitPy.delete_ViewerPreferences

# Register ViewerPreferences in _VisusAppKitPy:
_VisusAppKitPy.ViewerPreferences_swigregister(ViewerPreferences)

class ViewerAutoRefresh(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    enabled = property(_VisusAppKitPy.ViewerAutoRefresh_enabled_get, _VisusAppKitPy.ViewerAutoRefresh_enabled_set)
    msec = property(_VisusAppKitPy.ViewerAutoRefresh_msec_get, _VisusAppKitPy.ViewerAutoRefresh_msec_set)

    def __init__(self):
        _VisusAppKitPy.ViewerAutoRefresh_swiginit(self, _VisusAppKitPy.new_ViewerAutoRefresh())
    __swig_destroy__ = _VisusAppKitPy.delete_ViewerAutoRefresh

# Register ViewerAutoRefresh in _VisusAppKitPy:
_VisusAppKitPy.ViewerAutoRefresh_swigregister(ViewerAutoRefresh)

class ViewerToolBarTab(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    name = property(_VisusAppKitPy.ViewerToolBarTab_name_get, _VisusAppKitPy.ViewerToolBarTab_name_set)

    def __init__(self, name_):
        _VisusAppKitPy.ViewerToolBarTab_swiginit(self, _VisusAppKitPy.new_ViewerToolBarTab(name_))
    __swig_destroy__ = _VisusAppKitPy.delete_ViewerToolBarTab

    @staticmethod
    def createButton(*args):
        return _VisusAppKitPy.ViewerToolBarTab_createButton(*args)

    def addAction(self, action):
        return _VisusAppKitPy.ViewerToolBarTab_addAction(self, action)

    def addMenu(self, icon, name, menu):
        return _VisusAppKitPy.ViewerToolBarTab_addMenu(self, icon, name, menu)

    def addBlueMenu(self, icon, name, menu):
        return _VisusAppKitPy.ViewerToolBarTab_addBlueMenu(self, icon, name, menu)

# Register ViewerToolBarTab in _VisusAppKitPy:
_VisusAppKitPy.ViewerToolBarTab_swigregister(ViewerToolBarTab)

def ViewerToolBarTab_createButton(*args):
    return _VisusAppKitPy.ViewerToolBarTab_createButton(*args)

class ViewerToolBar(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    file_menu = property(_VisusAppKitPy.ViewerToolBar_file_menu_get, _VisusAppKitPy.ViewerToolBar_file_menu_set)
    bookmarks_button = property(_VisusAppKitPy.ViewerToolBar_bookmarks_button_get, _VisusAppKitPy.ViewerToolBar_bookmarks_button_set)
    tabs = property(_VisusAppKitPy.ViewerToolBar_tabs_get, _VisusAppKitPy.ViewerToolBar_tabs_set)

    def __init__(self):
        _VisusAppKitPy.ViewerToolBar_swiginit(self, _VisusAppKitPy.new_ViewerToolBar())

    def addTab(self, tab, name):
        return _VisusAppKitPy.ViewerToolBar_addTab(self, tab, name)
    __swig_destroy__ = _VisusAppKitPy.delete_ViewerToolBar

# Register ViewerToolBar in _VisusAppKitPy:
_VisusAppKitPy.ViewerToolBar_swigregister(ViewerToolBar)

class ViewerLogo(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    filename = property(_VisusAppKitPy.ViewerLogo_filename_get, _VisusAppKitPy.ViewerLogo_filename_set)
    pos = property(_VisusAppKitPy.ViewerLogo_pos_get, _VisusAppKitPy.ViewerLogo_pos_set)
    opacity = property(_VisusAppKitPy.ViewerLogo_opacity_get, _VisusAppKitPy.ViewerLogo_opacity_set)
    border = property(_VisusAppKitPy.ViewerLogo_border_get, _VisusAppKitPy.ViewerLogo_border_set)
    tex = property(_VisusAppKitPy.ViewerLogo_tex_get, _VisusAppKitPy.ViewerLogo_tex_set)

    def __init__(self):
        _VisusAppKitPy.ViewerLogo_swiginit(self, _VisusAppKitPy.new_ViewerLogo())
    __swig_destroy__ = _VisusAppKitPy.delete_ViewerLogo

# Register ViewerLogo in _VisusAppKitPy:
_VisusAppKitPy.ViewerLogo_swigregister(ViewerLogo)

class Viewer(VisusDataflowPy.DataflowListener):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _VisusAppKitPy.Viewer_swiginit(self, _VisusAppKitPy.new_Viewer(*args))
    __swig_destroy__ = _VisusAppKitPy.delete_Viewer

    def getTypeName(self):
        return _VisusAppKitPy.Viewer_getTypeName(self)

    def configureFromCommandLine(self, args):
        return _VisusAppKitPy.Viewer_configureFromCommandLine(self, args)

    def c_ptr(self):
        return _VisusAppKitPy.Viewer_c_ptr(self)

    def printInfo(self, msg):
        return _VisusAppKitPy.Viewer_printInfo(self, msg)

    def showLicences(self):
        return _VisusAppKitPy.Viewer_showLicences(self)

    def getDataflow(self):
        return _VisusAppKitPy.Viewer_getDataflow(self)

    def getGLCanvas(self):
        return _VisusAppKitPy.Viewer_getGLCanvas(self)

    def getGLCamera(self):
        return _VisusAppKitPy.Viewer_getGLCamera(self)

    def getTreeView(self):
        return _VisusAppKitPy.Viewer_getTreeView(self)

    def getFrameView(self):
        return _VisusAppKitPy.Viewer_getFrameView(self)

    def getLog(self):
        return _VisusAppKitPy.Viewer_getLog(self)

    def addDockWidget(self, *args):
        return _VisusAppKitPy.Viewer_addDockWidget(self, *args)

    def showNodeContextMenu(self, node):
        return _VisusAppKitPy.Viewer_showNodeContextMenu(self, node)

    def showPopupWidget(self, widget):
        return _VisusAppKitPy.Viewer_showPopupWidget(self, widget)

    def openFile(self, filename, parent=None):
        return _VisusAppKitPy.Viewer_openFile(self, filename, parent)

    def openUrl(self, url, parent=None):
        return _VisusAppKitPy.Viewer_openUrl(self, url, parent)

    def saveFile(self, filename, bSaveHistory=False):
        return _VisusAppKitPy.Viewer_saveFile(self, filename, bSaveHistory)

    def postRedisplay(self):
        return _VisusAppKitPy.Viewer_postRedisplay(self)

    def playFile(self, filename):
        return _VisusAppKitPy.Viewer_playFile(self, filename)

    def takeSnapshot(self, *args):
        return _VisusAppKitPy.Viewer_takeSnapshot(self, *args)

    def editNode(self, node=None):
        return _VisusAppKitPy.Viewer_editNode(self, node)

    def beginFreeTransform(self, *args):
        return _VisusAppKitPy.Viewer_beginFreeTransform(self, *args)

    def endFreeTransform(self):
        return _VisusAppKitPy.Viewer_endFreeTransform(self)

    def refreshActions(self):
        return _VisusAppKitPy.Viewer_refreshActions(self)

    def idle(self):
        return _VisusAppKitPy.Viewer_idle(self)

    def modelChanged(self):
        return _VisusAppKitPy.Viewer_modelChanged(self)

    def enableSaveSession(self):
        return _VisusAppKitPy.Viewer_enableSaveSession(self)

    def dataflowBeforeProcessInput(self, node):
        return _VisusAppKitPy.Viewer_dataflowBeforeProcessInput(self, node)

    def dataflowAfterProcessInput(self, node):
        return _VisusAppKitPy.Viewer_dataflowAfterProcessInput(self, node)

    def getRoot(self):
        return _VisusAppKitPy.Viewer_getRoot(self)

    def getUUID(self, node):
        return _VisusAppKitPy.Viewer_getUUID(self, node)

    def getNodes(self):
        return _VisusAppKitPy.Viewer_getNodes(self)

    def findNodeByUUID(self, uuid):
        return _VisusAppKitPy.Viewer_findNodeByUUID(self, uuid)

    def findPick(self, node, screen_point, bRecursive, distance=None):
        return _VisusAppKitPy.Viewer_findPick(self, node, screen_point, bRecursive, distance)

    def getBounds(self, node, bRecursive=False):
        return _VisusAppKitPy.Viewer_getBounds(self, node, bRecursive)

    def getWorldDimension(self):
        return _VisusAppKitPy.Viewer_getWorldDimension(self)

    def getWorldBox(self):
        return _VisusAppKitPy.Viewer_getWorldBox(self)

    def computeNodeToNode(self, dst, src):
        return _VisusAppKitPy.Viewer_computeNodeToNode(self, dst, src)

    def computeQueryBounds(self, query_node):
        return _VisusAppKitPy.Viewer_computeQueryBounds(self, query_node)

    def computeNodeToScreen(self, frustum, node):
        return _VisusAppKitPy.Viewer_computeNodeToScreen(self, frustum, node)

    def attachGLCamera(self, value):
        return _VisusAppKitPy.Viewer_attachGLCamera(self, value)

    def detachGLCamera(self):
        return _VisusAppKitPy.Viewer_detachGLCamera(self)

    def glGetRenderQueue(self, node):
        return _VisusAppKitPy.Viewer_glGetRenderQueue(self, node)

    def glCameraChangeEvent(self):
        return _VisusAppKitPy.Viewer_glCameraChangeEvent(self)

    def glCanvasResizeEvent(self, evt):
        return _VisusAppKitPy.Viewer_glCanvasResizeEvent(self, evt)

    def glCanvasMousePressEvent(self, evt):
        return _VisusAppKitPy.Viewer_glCanvasMousePressEvent(self, evt)

    def glCanvasMouseMoveEvent(self, evt):
        return _VisusAppKitPy.Viewer_glCanvasMouseMoveEvent(self, evt)

    def glCanvasMouseReleaseEvent(self, evt):
        return _VisusAppKitPy.Viewer_glCanvasMouseReleaseEvent(self, evt)

    def glCanvasWheelEvent(self, evt):
        return _VisusAppKitPy.Viewer_glCanvasWheelEvent(self, evt)

    def keyPressEvent(self, evt):
        return _VisusAppKitPy.Viewer_keyPressEvent(self, evt)

    def glRender(self, gl):
        return _VisusAppKitPy.Viewer_glRender(self, gl)

    def glRenderNodes(self, gl):
        return _VisusAppKitPy.Viewer_glRenderNodes(self, gl)

    def glRenderSelection(self, gl):
        return _VisusAppKitPy.Viewer_glRenderSelection(self, gl)

    def glRenderGestures(self, gl):
        return _VisusAppKitPy.Viewer_glRenderGestures(self, gl)

    def glRenderLogos(self, gl):
        return _VisusAppKitPy.Viewer_glRenderLogos(self, gl)

    def clearAll(self):
        return _VisusAppKitPy.Viewer_clearAll(self)

    def dropProcessing(self):
        return _VisusAppKitPy.Viewer_dropProcessing(self)

    def getAutoRefresh(self):
        return _VisusAppKitPy.Viewer_getAutoRefresh(self)

    def setAutoRefresh(self, value):
        return _VisusAppKitPy.Viewer_setAutoRefresh(self, value)

    def getSelection(self):
        return _VisusAppKitPy.Viewer_getSelection(self)

    def setSelection(self, node):
        return _VisusAppKitPy.Viewer_setSelection(self, node)

    def dropSelection(self):
        return _VisusAppKitPy.Viewer_dropSelection(self)

    def setMinimal(self):
        return _VisusAppKitPy.Viewer_setMinimal(self)

    def setNodeName(self, node, value):
        return _VisusAppKitPy.Viewer_setNodeName(self, node, value)

    def setNodeVisible(self, node, value):
        return _VisusAppKitPy.Viewer_setNodeVisible(self, node, value)

    def addNode(self, *args):
        return _VisusAppKitPy.Viewer_addNode(self, *args)

    def removeNode(self, node):
        return _VisusAppKitPy.Viewer_removeNode(self, node)

    def moveNode(self, dst, src, index=-1):
        return _VisusAppKitPy.Viewer_moveNode(self, dst, src, index)

    def connectNodes(self, *args):
        return _VisusAppKitPy.Viewer_connectNodes(self, *args)

    def disconnectNodes(self, _from, oport_name, iport_name, to):
        return _VisusAppKitPy.Viewer_disconnectNodes(self, _from, oport_name, iport_name, to)

    def autoConnectNodes(self):
        return _VisusAppKitPy.Viewer_autoConnectNodes(self)

    def isMouseDragging(self):
        return _VisusAppKitPy.Viewer_isMouseDragging(self)

    def setMouseDragging(self, value):
        return _VisusAppKitPy.Viewer_setMouseDragging(self, value)

    def scheduleMouseDragging(self, value, msec):
        return _VisusAppKitPy.Viewer_scheduleMouseDragging(self, value, msec)

    def reloadVisusConfig(self, bChooseAFile=False):
        return _VisusAppKitPy.Viewer_reloadVisusConfig(self, bChooseAFile)

    def setPreferences(self, value):
        return _VisusAppKitPy.Viewer_setPreferences(self, value)

    def open(self, url, parent=None):
        return _VisusAppKitPy.Viewer_open(self, url, parent)

    def save(self, filename, bSaveHistory=False):
        return _VisusAppKitPy.Viewer_save(self, filename, bSaveHistory)

    def setDataflow(self, dataflow):
        return _VisusAppKitPy.Viewer_setDataflow(self, dataflow)

    def refreshNode(self, node=None):
        return _VisusAppKitPy.Viewer_refreshNode(self, node)

    def refreshAll(self):
        return _VisusAppKitPy.Viewer_refreshAll(self)

    def guessGLCameraPosition(self, ref_=-1):
        return _VisusAppKitPy.Viewer_guessGLCameraPosition(self, ref_)

    def mirrorGLCamera(self, ref=0):
        return _VisusAppKitPy.Viewer_mirrorGLCamera(self, ref)

    def addWorld(self, uuid):
        return _VisusAppKitPy.Viewer_addWorld(self, uuid)

    def addDataset(self, uuid, parent, url):
        return _VisusAppKitPy.Viewer_addDataset(self, uuid, parent, url)

    def addGLCamera(self, *args):
        return _VisusAppKitPy.Viewer_addGLCamera(self, *args)

    def addVolume(self, *args):
        return _VisusAppKitPy.Viewer_addVolume(self, *args)

    def addSlice(self, *args):
        return _VisusAppKitPy.Viewer_addSlice(self, *args)

    def setFieldName(self, value):
        return _VisusAppKitPy.Viewer_setFieldName(self, value)

    def addKdQuery(self, *args):
        return _VisusAppKitPy.Viewer_addKdQuery(self, *args)

    def addIsoContour(self, *args):
        return _VisusAppKitPy.Viewer_addIsoContour(self, *args)

    def addScripting(self, uuid, parent):
        return _VisusAppKitPy.Viewer_addScripting(self, uuid, parent)

    def setScriptingCode(self, value):
        return _VisusAppKitPy.Viewer_setScriptingCode(self, value)

    def addCpuTransferFunction(self, uuid, parent):
        return _VisusAppKitPy.Viewer_addCpuTransferFunction(self, uuid, parent)

    def addStatistics(self, uuid, parent):
        return _VisusAppKitPy.Viewer_addStatistics(self, uuid, parent)

    def addRender(self, *args):
        return _VisusAppKitPy.Viewer_addRender(self, *args)

    def addKdRender(self, *args):
        return _VisusAppKitPy.Viewer_addKdRender(self, *args)

    def addOSPRay(self, *args):
        return _VisusAppKitPy.Viewer_addOSPRay(self, *args)

    def addGroup(self, *args):
        return _VisusAppKitPy.Viewer_addGroup(self, *args)

    def addModelView(self, uuid, parent, insert=False):
        return _VisusAppKitPy.Viewer_addModelView(self, uuid, parent, insert)

    def addPalette(self, uuid, parent, palette):
        return _VisusAppKitPy.Viewer_addPalette(self, uuid, parent, palette)

    def execute(self, ar):
        return _VisusAppKitPy.Viewer_execute(self, ar)

    def write(self, ar):
        return _VisusAppKitPy.Viewer_write(self, ar)

    def read(self, ar):
        return _VisusAppKitPy.Viewer_read(self, ar)

    def addNetRcv(self, port):
        return _VisusAppKitPy.Viewer_addNetRcv(self, port)

    def addNetSnd(self, *args):
        return _VisusAppKitPy.Viewer_addNetSnd(self, *args)

    def postFlushMessages(self):
        return _VisusAppKitPy.Viewer_postFlushMessages(self)

# Register Viewer in _VisusAppKitPy:
_VisusAppKitPy.Viewer_swigregister(Viewer)



