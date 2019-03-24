from Cocoa import *
from Foundation import NSObject
from qtpy import QtCore, QtWidgets, QtGui


class NSSegmentedControlTarget(NSObject):

    def setTarget_(self, target):
        self.target = target

    def triggered_(self, sender):
        self.target.triggerAction()


class Style(object):
    automatic = 0
    rounded = 1
    texturedRounded = 2
    roundedRect = 3
    texturedSquare = 4
    capsule = 5
    smallSquare = 6
    separated = 7

    def __contains__(self, item):
        return item in range(0, 8)


class MacSegmentedControl(QtWidgets.QMacCocoaViewContainer):
    """
    This class wraps a Cocoa NSSegmentedControl for PyQt. Different styles can be
    chosen depnding on the button location, for instance the toolbar or the main window.
    """

    currentChanged = QtCore.Signal(int)

    def __init__(self, parent=None, labels=None):
        super(self.__class__, self).__init__(0, parent)

        self.Style = Style()

        self.pool = NSAutoreleasePool.alloc().init()

        # Set up segmented control buttons
        self._segmented = NSSegmentedControl.alloc().init()
        self._segmented.setSegmentStyle_(self.Style.automatic)
        self._segmented.setAutoresizesSubviews_(True)
        if labels is not None:
            n = len(labels)
            self._segmented.setSegmentCount_(n)
            for i, text in enumerate(labels):
                self._segmented.setLabel_forSegment_(text, i)
            self._segmented.setSelectedSegment_(0)

        # Set up correct size
        intrinic_size = self._segmented.intrinsicContentSize()
        self.resize(intrinic_size.width, intrinic_size.height + 10)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # Emit signal when selected item changes
        # This is done in a very round-about way: the target action when clicking the button
        # must belong to a subclass of NSObject (NSSegmentedControlTarget in this case). This
        # action in turn calls `triggerAction` which emits the `currentChanged` signal.
        self.proxy_ = NSSegmentedControlTarget.alloc().init()
        self.proxy_.setTarget_(self)
        self._segmented.setTarget_(self.proxy_)
        selector = objc.selector(self.proxy_.triggered_, signature=b'v@:@')
        self._segmented.setAction_(selector)

        self.setCocoaView(self._segmented.__c_void_p__().value)

        # Release references
        self._segmented.release()
        self.pool.release()

    def sizeHint(self):
        intrinic_size = self._segmented.intrinsicContentSize()
        return QtCore.QSize(intrinic_size.width, intrinic_size.height + 10)

    def triggerAction(self):
        i = self._segmented.selectedSegment()
        self.currentChanged.emit(i)

    def style(self):
        return self._segmented.segmentStyle()

    def setStyle(self, i):
        """
        Sets the style of the underlying NSSegmentedControl.

        0 (automatic): The appearance of the segmented control is automatically determined based on
            the type of window in which the control is displayed and the position within the window.
            This will not work when using SegmentedControl in QWidgets but requires a native Cocoa
            window.

        1 (rounded): The control is displayed using the rounded style.

        2 (texturedRounded): The control is displayed using the textured rounded style. In
            macOS 10.7 and later, this style uses the artwork defined for
            NSSegmentedControl.Style.texturedSquare, so you should specify
            NSSegmentedControl.Style.texturedSquare instead.

        3 (roundedRect): The control is displayed using the round rect style.

        4 (texturedSquare): The control is displayed using the textured square style.

        5 (capsule): The control is displayed using the capsule style. In macOS 10.7 and later, this
            style uses the artwork defined for NSSegmentedControl.Style.texturedSquare, so you
            should specify NSSegmentedControl.Style.texturedSquare instead.

        6 (smallSquare): The control is displayed using the small square style.

        7 (separated): The segments in the control are displayed very close to each other but not
            touching. For example, Safari in macOS 10.10 and later uses this style for the previous
            and next page segmented control.
        """
        assert i in self.Style
        self._segmented.setSegmentStyle_(i)

    def segmentCount(self):
        return self._segmented.segmentCount(n)

    def setSegmentCount(self, n):
        return self._segmented.setSegmentCount_(n)

    def selectedSegment(self):
        return self._segmented.selectedSegment()

    def setSelectedSegment(self, i):
        assert i < segmentCount
        self._segmented.setSelectedSegment_(i)
        self.currentChanged.emit(i)

    def getSegmentLabel(self, i):
        assert i < segmentCount
        return self._segmented.labelForSegment_(i)

    def setSegmentLabel(self, i, text):
        assert i < segmentCount
        return self._segmented.setLabel_forSegment_(text, i)


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    ti = MacSegmentedControl(labels=['Test1', 'Test2', 'Test3'])

    w = QtWidgets.QMainWindow()
    w.setCentralWidget(ti)
    w.show()

    app.exec_()
